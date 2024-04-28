from flask import Flask, request, session, redirect, url_for
from config import get_config
from PluginController import PluginController
import os, argparse

config_instance = get_config()
app = Flask(__name__,static_folder='res')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
controller_instance = PluginController(config_instance)
plugin_folder = os.path.join(os.path.dirname(__file__), 'plugins')  # Path to the plugins folder
data_folder = os.path.join(os.path.dirname(__file__), 'data')  # Path to the plugins folder

controller_instance.load_translations(os.path.join(data_folder, 'translations.json'))
controller_instance.add_folder(plugin_folder)
controller_instance.on_update()

# Simple authentication check
def authenticate(username, password):
    return username == 'admin' and password == 'tower'

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    page = request.args.get('page', config_instance.get('defaultpage', 'default'))
    plugin = request.args.get('plugin', config_instance.get('defaultplugin', 'vitals'))
    action = request.args.get('action', '')

    app_params = {
        'page': page,
        'plugin': plugin,
        'action': action
    }
    return controller_instance.on_web_page(app_params)
    #return "Request processed"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid username or password"
    return """
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    """

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

def parse_args():
    parser = argparse.ArgumentParser(description="Run Flask app with custom configurations")
    parser.add_argument("--port", type=int, default=5000, help="Port number to run the app (default: 8080)")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    parser.add_argument("--no-debug", action="store_true", help="Disable debug mode")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    # Run the Flask app with specified configurations
    app.run(port=args.port, debug=not args.no_debug, use_reloader=not args.no_reload)