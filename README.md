
# Home Assistant | Kasta Integration
This custom HACS integration allows you to integrate your Kasta Smart Living lighting system into Home Assistant. Alongside this integration, you also need to run [this python server](https://example.com) which hooks into an android phone running the Kasta app via the ADB Bridge to control these devices over bluetooth.

Please note that due to the lack of API, this integration relies on a mobile device constantly running the Kasta application.

## Step 1: Setting up your android device
- Follow [this](https://developer.android.com/studio/debug/dev-options) guide to enable developer options on your android device
- Enable USB debugging from the developer options menu
- Enable Always Awake whilst Debugging from the developer options menu

## Step 2: Setting up the python server
- Clone down the [HA-Kasta-Integration-Server](https://github.com/FitztianPlays/HA-Kasta-Integration-Server) repository, and open a terminal in the directory.
- Configure the project by editing the `config.py` file.
	- Port: Port of the python web server
	- Host: Bind address of the web server
	- HA Instance URL: The url to your home assistant instance
	- HA Bearer Token: An authentication token to allow the server to push updates to your lights
- Plug your android device into this machine
- Run `./adb start-server` in the terminal we opened before to connect to the phone
	- You may have to allow the machine to connect to the phone by hitting allow
- Run the `main.py` file, either directly using python, or through an instance manager like [pm2](https://pm2.keymetrics.io/docs/usage/quick-start/). Just ensure the server is always running when home assistant is, or the integration won't work.

> Notice: Ensure that you don't accidentally expose this web server to the internet, as it doesn't have built in authentication. 

## Step 3: Home Assistant Integration

Once you have the python server running, just setup this integration using the host and port specified in step 2, and all your lights will be auto-discovered and added as light entities with the same name and id as what you have specified on the [Kasta App](https://play.google.com/store/apps/details?id=com.haneco.ble).
