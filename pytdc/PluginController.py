import os
import sys
from pathlib import Path
from Plugin import Plugin  # Importing Plugin class from Plugin.py
import importlib.util

class PluginController:
    def __init__(self, config):
        self.plugins = {}
        self.config = config
        self.translations = {}
    def load_translations(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.translations = json.load(file)
        except FileNotFoundError:
            print("Error: File not found.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format.")

    def load_plugin(self, plugin_folder):
        plugin_name = os.path.basename(plugin_folder)
        try:
            module_path = os.path.join(plugin_folder, f'{plugin_name}.py')
            spec = importlib.util.spec_from_file_location(plugin_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            plugin_class = getattr(module, plugin_name.capitalize())  # Assuming the class name is capitalized
            plugin_instance = plugin_class(self.config)
            return plugin_instance
        except FileNotFoundError:
            print(f"Plugin {plugin_name} not found.")
            return None
        except AttributeError:
            print(f"Class {plugin_name.capitalize()} not found in {plugin_name}.py.")
            return None
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {e}")
            return None

    def add_folder(self, plugin_folder):
        if os.path.isdir(plugin_folder):
            for root, dirs, files in os.walk(plugin_folder):
                for dir_name in dirs:
                    if dir_name != '__pycache__':
                        plugin_instance = self.load_plugin(os.path.join(root, dir_name))
                        if plugin_instance:
                            self.plugins[dir_name.lower()] = plugin_instance
                            plugin_instance.set_translations(self.translations)
                            print(f"Loaded plugin {dir_name}")

    def on_web_page(self, app):
        plugin = app['plugin']
        theme = self.config['theme']

        if plugin.lower() not in self.plugins:
            plugin = "network"
            page = "hosts"

        output = self.plugins[plugin.lower()].show_page(app)
        theme_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"themes/{theme}")
        template = YTemplate(os.path.join(theme_folder, "main.tpl"))
        vars = self.config['vars']
        vars['content'] = f"<div id='content'>{output}</div>"
        menu_entries = self.gen_menu()
        vars['navigationmenu'] = menu_entries
        template.setFromArray(vars)
        print(template.parse())

    def on_command(self, options):
        plugin_name = options.get('p', '').lower()
        
        if plugin_name in self.plugins:
            self.plugins[plugin_name].on_command(options)
        else:
            print("Error: Plugin not found")

    def on_update(self):
        for plugin_name, plugin in self.plugins.items():
            plugin.on_update()

    def on_long_update(self):
        for plugin_name, plugin in self.plugins.items():
            plugin.on_long_update()

    def gen_menu(self):
        menu = {}
        for plugin_name, plugin in self.plugins.items():
            plugin_menus = plugin.get_menus() or {}
            for menu_name, menu_details in plugin_menus.items():
                menu.setdefault(menu_name, []).extend(menu_details)
        output = "\n<nav id='navbar' class='navbar navbar-expand-lg bg-dark'>\n"
        output += "  <div class=\"collapse navbar-collapse\" id=\"navbarSupportedContent\">\n"
        output += "    <ul class=\"navbar-nav mr-auto\">\n"
        for menu_id, menu_details in menu.items():
            link = menu_details.get('url', '#') if 'url' in menu_details else ''
            if 'plugin' in menu_details:
                query = {'plugin': menu_details['plugin']}
                query['page'] = menu_details.get('page', '')
                link = f"?{'&'.join([f'{k}={v}' for k, v in query.items()])}"
            label = get_translation(menu_details.get('text', menu_id))
            if 'children' in menu_details and menu_details['children']:
                output += '<li class="nav-item dropdown">'
                output += f"  <a class=\"nav-link nav-link-primary dropdown-toggle\" role='button' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false' href=\"{link}\">{label}</a>\n"
                output += '<div class="dropdown-menu" aria-labelledby="navbarDropdown">' 
                for child_menu_id, child_menu_details in menu_details['children'].items():
                    child_link = child_menu_details.get('url', '')
                    if 'plugin' in child_menu_details:
                        query = {'plugin': child_menu_details['plugin']}
                        query['page'] = child_menu_details.get('page', '')
                        if 'action' in child_menu_details:
                            query['action'] = child_menu_details['action']
                        child_link = f"?{'&'.join([f'{k}={v}' for k, v in query.items()])}"
                    child_label = get_translation(child_menu_details.get('text', ''))
                    output += f"    <a class=\"dropdown-item\" href=\"{child_link}\">{child_label}</a>\n"
                output += "</div>"
            else:
                output += "<li class='nav-item'>\n"
                output += f"  <a class=\"nav-link\" href=\"{link}\">{label}</a>\n"
            output += "</li>\n"
        output += "    </ul>\n  </div>\n</nav>"
        return output

    def show_widget(self, plugin, widget):
        return self.plugins.get(plugin.lower(), "").show_widget(widget)

