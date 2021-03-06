#!/usr/bin/env python3

from .agent_based_api.v1 import *
from urllib.request import urlopen

def discover_check_dokuwiki(section):
    yield Service()

def getLastestDokuwiki():
    link = "http://update.dokuwiki.org/check/"
    f = urlopen(link)
    for i in f:
        latest = i.decode('utf-8')
        break

    return latest.split(":")[-1].strip(" ").replace(" ","").replace(".\n","")


def check_dokuwiki(params,section):
    for line in section:
        sum="CRIT: Version Outdatet. Aktuell: " + getLastestDokuwiki() + " installiert: " + line[0]
        s=State.CRIT
        if line[0] == getLastestDokuwiki() :
            s=State.OK
            sum="OK: Version aktuell. Aktuell: " + line[0]
    yield Result(state=s, summary=sum)


register.check_plugin(
    name = "check_dokuwiki",
    service_name = "check_dokuwiki",
    discovery_function = discover_check_dokuwiki,
    check_function = check_dokuwiki,
)
