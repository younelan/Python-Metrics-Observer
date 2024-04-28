#Control Tower

This is for Server Control Tower, a simple metrics collection tool

##Usage

./pytdc -c [plugin] -a [action]   - call tdc with plugin and run specified action
./pytdc --update - run data collection on all plugins

##Cron
rather than running pytdc manually, it is suggested to run the plugin in cron like this:
*/2 * * * * /var/www/html/server-control/backend/tdc --update >/dev/null 2>&1

for now, collected data is stored in data folder

##config.json

To configure pytdc, you use data/config.json

```
{
        "ping-subnets": ["192.168.1.0/24"],
        "connection-name": "The Internet",
        "ping-address": "8.8.8.8",
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

##requirements
install flask

```

- **ping-subnets** : comma separated list of subnets for nmap, used by the Network Plugin
- **ping-address** : address to check if we are connected, used by the Vitals Plugin
- **credentials** : list of credentials, reserved for future plugins to store credentials for hosts (used by unreleased nokia router plugin). Put here as an example of storing credentials for now

adjust to your network
