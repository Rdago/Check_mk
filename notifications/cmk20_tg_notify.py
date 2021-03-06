#!/usr/bin/env python3
# Telegram cmk2.0


import os, re, sys
from urllib.request import urlopen
import urllib.parse
import ssl
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_notification_context():
    context = {}
    for (var, value) in os.environ.items():
        if var.startswith("NOTIFY_"):
            context[var[7:]] = value
    return context

tmpl_host_text = """*Check_MK: $HOSTNAME$ - $EVENT_TXT$*
```
Host:     $HOSTNAME$
Alias:    $HOSTALIAS$
Address:  $HOSTADDRESS$
Event:    $EVENT_TXT$
Output:   $HOSTOUTPUT$

$LONGHOSTOUTPUT$```"""

tmpl_service_text = """*Check_MK: $HOSTNAME$/$SERVICEDESC$ $EVENT_TXT$*
```
Host:     $HOSTNAME$
Alias:    $HOSTALIAS$
Address:  $HOSTADDRESS$
Service:  $SERVICEDESC$
Event:    $EVENT_TXT$
Output:   $SERVICEOUTPUT$

$LONGSERVICEOUTPUT$```"""

def substitute_context(template, context):
    # First replace all known variables
    for varname, value in context.items():
        template = template.replace('$'+varname+'$', value)

    # Remove the rest of the variables and make them empty
    template = re.sub("\$[A-Z_][A-Z_0-9]*\$", "", template)
    return template

def construct_message_text(context):
    notification_type = context["NOTIFICATIONTYPE"]
    if notification_type in [ "PROBLEM", "RECOVERY" ]:
        txt_info = "$PREVIOUS@HARDSHORTSTATE$ -> $@SHORTSTATE$"
    elif notification_type.startswith("FLAP"):
        if "START" in notification_type:
            txt_info = "Started Flapping"
        else:
            txt_info = "Stopped Flapping ($@SHORTSTATE$)"
    elif notification_type.startswith("DOWNTIME"):
        what = notification_type[8:].title()
        txt_info = "Downtime " + what + " ($@SHORTSTATE$)"
    elif notification_type == "ACKNOWLEDGEMENT":
        txt_info = "Acknowledged ($@SHORTSTATE$)"
    elif notification_type == "CUSTOM":
        txt_info = "Custom Notification ($@SHORTSTATE$)"
    else:
        txt_info = notification_type # Should neven happen

    txt_info = substitute_context(txt_info.replace("@", context["WHAT"]), context)

    context["EVENT_TXT"] = txt_info

    if context['WHAT'] == 'HOST':
        tmpl_text = tmpl_host_text
    else:
        tmpl_text = tmpl_service_text
        
    return substitute_context(tmpl_text, context)

def send_telegram_message(token, chat_id, text):
    url = 'https://api.telegram.org/bot%s/sendMessage' % (token)
    data = urllib.parse.urlencode({'chat_id':chat_id, 'text':text, 'parse_mode':'Markdown'}).encode("utf-8")
    urlopen(url, data=data, context=ctx).read()

#### CHANGE THESE ####
tg_token = '00000:XXXXXXXXXXXXXXXXXXXXXXXXX'
chat_id = '0000000'

context = fetch_notification_context()
text = construct_message_text(context)
send_telegram_message(tg_token, chat_id, text)

