#!/bin/sh

# Get Power Status from Shelly-API
kuche=$(curl -s -u <user>:<password> http://<ip>/status | jq '.relays[].ison' | sed 's/true/1/g'  | sed 's/false/0/g')
sz=$(curl -s -u <user>:<password> http://<ip>/status | jq '.relays[].ison'  | sed 's/true/1/g'  | sed 's/false/0/g')

# Piggiback information for Host "Shelly-Kueche"
echo "<<<<Shelly-Kueche>>>>"
echo "<<<local>>>"
echo "0 SHELLY-Kueche Anschaltverhalten=$kuche ok"
echo "<<<<>>>>"


# Piggiback information for Host "Shelly-SZ"
echo "<<<<Shelly-SZ>>>>"
echo "<<<local>>>"
echo "0 SHELLY-Schlafzimmer Anschaltverhalten=$sz ok"
echo "<<<<>>>>"


