import json
import subprocess

class Plugin:
    def __init__(self, config):
        self.config = config
        self.data = {}
        self.translations = {}
        self.handler = None
        self.controller = None
        
    def set_controller(self, controller):
        self.controller = controller
    def set_translations(self, translations):
        self.translations = translations

    def run_command(self, command):
        try:
            result = subprocess.check_output(command, shell=True, text=True)
            return result.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error executing command '{command}': {e}")
            return None
                
    def get_translation(self,i18nstr, lang=""):
        if not lang:
            try:
                lang = self.config['lang']
            except:
                lang = "en" 
        # try:
        #     retval = self.translations[lang][i18nstr]
        # except:
        #     retval = i18nstr
        try:
            retval = self.translations[lang][i18nstr]
        except:
            retval = i18nstr
        return retval

    def store(self, collection, fname=None):
        json_data = json.dumps(collection)
        if fname:
            cfg = f"data/{fname}"
        else:
            classname = type(self).__name__
            cfg = f"data/{classname}"
        with open(cfg, 'w') as f:
            f.write(json_data)

    def debug(self, level, output):
        debuglevel = self.config.get('debug', 0)
        if level <= debuglevel:
            print(output)

    def set_config(self, config):
        self.config = config

    def init(self):
        pass

    def set_handler(self, plugin_handler):
        self.handler = plugin_handler

    def set_data(self, data):
        self.data = data

    def get_menus(self):
        return None

    def on_update(self):
        return False

    def on_command(self, options):
        action = options.get('a', '')
        plugin = options.get('p', '')
        print(f"<<<Undefined command {plugin}::{action}>>")

    def on_long_update(self):
        return False

    def show_page(self, params):
        return ""

    def show_widget(self, params):
        return ""

# def get_translation(i18nstr, lang=""):
    
#     # Use the provided language or default to English
#     lang = lang or config.get('lang', 'en')
#     # Get translation or return the original string
#     return translations.get(lang, {}).get(i18nstr, i18nstr)

