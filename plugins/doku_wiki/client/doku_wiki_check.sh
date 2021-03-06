#!/bin/sh
# Output: 
# <<<check_dokuwiki>>>
# 2000-01-01FooBar2
#
current=$(cat /var/www/<path>/VERSION)
echo "<<<check_dokuwiki>>>"
echo  "$current" | sed 's/ //g'
