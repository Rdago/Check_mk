#!/bin/bash

# Get Hue-Data from the Phillips Hue Gateway
hue=$(curl -s http://<IP>/api/<Username>)

# Piggiback Data to HUE-GW
echo "<<<<HUE-GW>>>>"
echo "<<<local>>>"

# Get all lights and create Checks for each one
for i in $(echo $hue | jq -r '.lights | keys | .[]'); do
        name=$(echo $hue | jq -r ".lights.\"${i}\".name" | sed 's/\s//g' |sed 's/ü/ue/g')
        power=$(echo $hue | jq -r ".lights.\"${i}\".state.on" | sed 's/true/1/g' | sed 's/false/0/g')
        bri=$(echo $hue | jq -r ".lights.\"$i\".state.bri")

        echo "0 $name Power=$power;;;0;1 OK!"
        echo "0 $name Brightness=$bri;;;0;255 OK!"
done

for i in $(echo $hue | jq -r '.config | keys | .[]'); do

        if [[ $i == "zigbeechannel" ]] || [[ $i == "modelid" ]] || [[ $i == "swversion" ]] || [[ $i == "apiversion" ]]
        then
           name=$(echo ${i} |sed 's/\s//g')
           myvalue=$(echo $hue | jq  ".config.${i}")
           echo "0 $name - $myvalue"
        fi
done

echo "<<<<>>>>"
