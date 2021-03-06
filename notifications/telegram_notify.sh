#!/bin/bash
# Telegram Benachrichtigung

env | grep NOTIFY_ | sort > $OMD_ROOT/tmp/foobar.out

TELEGRAM_BOT_TOKEN=<token>
CHAT_ID=<Chat-ID>
MESSAGE="*Check_MK: $NOTIFY_HOSTNAME - $NOTIFY_NOTIFICATIONTYPE *\nHOST: $NOTIFY_HOSTNAME \nEvent: $NOTIFY_NOTIFICATIONTYPE\nState: $NOTIFY_LASTSERVICESTATE\nOutput>

curl -X POST \
     -H 'Content-Type: application/json' \
     -d "{\"chat_id\": \"${CHAT_ID}\",\"parse_mode\":\"Markdown\", \"text\": \"${MESSAGE}\"" \
       https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage $>/dev/null

exit 0
