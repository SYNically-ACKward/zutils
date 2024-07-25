# zutils

# Miscellaneous Utility Scripts for Zscaler

## ZPA/discover_acs.py
Requests ClientID, Client Secret and Customer ID as user input via interactive menu and outputs a list of tenant App Connectors with key information to plan software upgrades / migrations. 

Information output includes: App Connector Name, App Connector ID, App Connector Private IP Address, Runtime OS Version, App Connector Description

Requirements: `pip install requests`
Usage: Navigate to the directory in which you downloaded the script and run `python discover_acs.py`

## Misc/traffic_gen.sh

Shell script that can simulate user-like traffic from a Linux VM or Container. The shell script leverages cURL and wget as well as randomly selected User Agents, websites, and session durations to provide variable output. 

Requirements: cURL, wget

Usage: Ensure a text file named `websites.txt` is present in the same directory as the shell script. Run `sudo chmod +x traffic_gen.sh` to give execute permissions to the script and run `./traffic_gen.sh` to kick off the traffic generation. 
