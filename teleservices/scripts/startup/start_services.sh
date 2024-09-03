#!/bin/bash

prefix="✨ start_services.sh ·"

echo "$prefix  Restarting services : rsyslog, cron."
# new way to start rsyslog since bookworm
/usr/sbin/rsyslogd && echo -n " rsyslog started! ✅..." || echo -n " rsyslog failed to start! ❌..."

service cron start && echo " cron started! ✅" || echo " cron failed to start! ❌"
echo "$prefix  Restarting services : rsyslog, cron done! ✅"

echo "$prefix Starting hobo... 🚀"
service hobo start && echo " hobo service has been started ! ✅" || echo " hobo service starting failed! ❌"

echo -n "$prefix Starting combo... 🚀"
service combo start && echo " combo service has been started ! ✅" || echo " combo service starting failed! ❌"

echo -n "$prefix Starting authentic2-multitenant... 🚀"
service authentic2-multitenant start && echo " authentic2-multitenant service has been started ! ✅" || echo " authentic2-multitenant service starting failed! ❌"

echo -n "$prefix Starting chrono... 🚀"
service chrono start && echo " chrono service has been started ! ✅" || echo " chrono service starting failed! ❌"

echo -n "$prefix Starting passerelle... 🚀"
service passerelle start && echo " passerelle service has been started ! ✅" || echo " passerelle service starting failed! ❌"

echo -n "$prefix Starting wcs... 🚀"
service wcs start && echo " wcs service has been started ! ✅" || echo " wcs service starting failed! ❌"

echo -n "$prefix Bijoe... 🚀"
service bijoe update && echo -n " bijoe service has been updated ! ✅..." || echo -n " Updating failed! ❌"
service bijoe start && echo " bijoe service has been started ! ✅" || echo " bijoe service starting failed! ❌"

echo -n "$prefix Starting nginx... 🚀"
service nginx start && echo " done! ✅" || echo " nginx service starting failed! ❌"

echo -n "$prefix Starting supervisor... 🚀"
service supervisor start && echo " supervisor service has been started ! ✅" || echo " supervisor service starting failed! ❌"