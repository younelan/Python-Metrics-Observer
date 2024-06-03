# Python Metrics Tracker 

This is a simple metrics collection tool

## Usage

**./pytrack -c [plugin] -a [action]**   - call tdc with plugin and run specified action
**./pytrack --update** - run data collection on all plugins
**python3 web.py** - Run the simple gui

## Cron
Rather than running pytrack manually, it is suggested to run the plugin in cron like this:
```
*/2 * * * * /var/www/html/server-control/backend/tdc --update >/dev/null 2>&1
```

for now, collected data is stored in data folder

## config.json

To configure pytrack, you use data/config.json

```
{
        "ping-subnets": ["192.168.1.0/24"],
        "connection-name": "The Internet",
        "ping-address": "8.8.8.8",
        "lang": "fr",
        "credentials": {
                "router": {
                        "type":"nokia",
                        "user":"admin",
                        "pass":"admin",
                        "host":"192.168.1.1",
                        "port": 22
                }
        }
}


```
- **language** : Either "fr" or "en" unless you create a translation
- **ping-subnets** : comma separated list of subnets for nmap, used by the Network Plugin
- **ping-address** : address to check if we are connected, used by the Vitals Plugin
- **credentials** : list of credentials, reserved for future plugins to store credentials for hosts (used by unreleased nokia router plugin). Put here as an example of storing credentials for now

adjust to your network


## web ui
There is an experimental web ui, run it with the following:

**python3 web.py**

Though the menus don't work, from the web browser, you can call http://localhost:5000/?plugin=vitals&action=default

## Web UI requirements
pip install flask

