#!/bin/sh

latest=$(wget -q https://download.dokuwiki.org/ -O - | grep -A4 'href="src/dokuwiki/dokuwiki-stable.tgz"' | sed 's/&quot;/"/g'  | grep -ohE "[[:digit:]]{4}-[[:digit:]]{2}-[[:digit:]]{2}[ a-zA-Z\"]*")
current=$(cat /var/www/html/web/VERSION)

if [ "$latest" == "$current" ]
then
        echo "0 dokuwiki-version - OK: Dokuwiki ist auch neuesten Stand: $current"
else
        echo "1 dokuwiki-version - WARN: Dokuwiki update verfügbar: $latest"
fi
