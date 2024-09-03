#!/bin/bash

prefix="✨ run.sh ·"
echo "$prefix 🏁 Starting script 🏁"

# Fix problem causing scripts still run by " init.d " not work working properly
# https://dev.entrouvert.org/issues/41958
# https://dev.entrouvert.org/issues/41960
export LANG=C.UTF-8

printenv >>/etc/environment # set env variables for cron jobs

echo -n "$prefix cleaning some pid/sock files that can be generated at image creation (if they exist)."
for file in /var/run/{authentic2-multitenant/authentic2-multitenant,chrono/chrono,fargo/fargo,hobo/hobo,combo/combo,nginx,rsyslogd,supervisord,wcs,passerelle/passerelle,bijoe/bijoe}.{pid,sock}; do
  test -e $file && (rm $file || echo "deletion of $file failed! ❌")
done
echo "$prefix cleaning some pid/sock files that can be generated at image creation (if they exist) done! ✅"

echo "$prefix  Launching fix_permissions.sh..."
test -e /opt/publik/scripts/startup/fix_permissions.sh && ( /opt/publik/scripts/startup/fix_permissions.sh && echo " done! ✅" || echo " failed! ❌" ) || echo " skipped! 🚫"

echo -m "$prefix 🐒Monkey-patching mails via '/var/lib/authentic2/locale/fr/LC_MESSAGES/mail-translation.py'..."
python3 /var/lib/authentic2/locale/fr/LC_MESSAGES/mail-translation.py && echo " done! ✅" || echo " failed! ❌"

echo -n "$prefix INFRA-5052 - Database update..."
test -e /var/lib/wcs/configure-wcs.py && (python3 /var/lib/wcs/configure-wcs.py && echo " done! ✅" || echo " failed! ❌") || echo " skipped! 🚫"

echo -n "$prefix linking iMio wcs_scripts_teleservices..."
if [ -d /opt/publik/wcs-scripts/wcs_scripts_teleservices ]; then
  ln -sfn /opt/publik/wcs-scripts/wcs_scripts_teleservices /var/lib/wcs/scripts && echo " done! ✅" || echo " failed! ❌"
else
  ln -sfn /opt/publik/wcs-scripts /var/lib/wcs/scripts && echo " done! ✅" || echo " failed! ❌"
fi

HOSTNAME=$(hostname)
echo -n "$prefix exec run-hook.sh..."
test -f /opt/publik/hooks/$HOSTNAME/run-hook.sh && ( /opt/publik/hooks/$HOSTNAME/run-hook.sh && echo " done! ✅" || echo "$prefix exec run-hook.sh... failed! ❌") || echo " skipped! 🚫"

echo "$prefix  Launching fix_wcs_utf8.sh..."
test -e /opt/publik/scripts/startup/fix_wcs_utf8.sh && ( /opt/publik/scripts/startup/fix_wcs_utf8.sh && echo " done! ✅" || echo " failed! ❌" ) || echo " skipped! 🚫"

echo "$prefix  Launching cron_monkey_patch.sh..."
test -e /opt/publik/scripts/startup/cron_monkey_patch.sh && ( /opt/publik/scripts/startup/cron_monkey_patch.sh && echo " done! ✅" || echo " failed! ❌" ) || echo " skipped! 🚫"

echo "$prefix  Launching start_services.sh..."
test -e /opt/publik/scripts/startup/start_services.sh && ( /opt/publik/scripts/startup/start_services.sh && echo " done! ✅" || echo " failed! ❌" ) || echo " skipped! 🚫"

echo "$prefix  Launching create_modelezip.sh..."
test -e /opt/publik/scripts/startup/create_modelezip.sh && ( /opt/publik/scripts/startup/create_modelezip.sh && echo " done! ✅" || echo " failed! ❌" ) || echo " skipped! 🚫"

echo "$prefix  Launching cooks.sh..."
test -e /opt/publik/scripts/startup/cooks.sh && ( /opt/publik/scripts/startup/cooks.sh && echo " done! ✅" || echo " failed! ❌" ) || echo " skipped! 🚫"

echo "$prefix  Launching translation_monkey_patch.sh..."
test -e /opt/publik/scripts/startup/translation_monkey_patch.sh && ( /opt/publik/scripts/startup/translation_monkey_patch.sh && echo " done! ✅" || echo " failed! ❌" ) || echo " skipped! 🚫"

echo -n "$prefix Running /etc/hobo/init.sh..."
if [ -f /etc/hobo/init.sh ]; then
  /etc/hobo/init.sh && echo " done! ✅" || echo " failed! ❌"
else
  echo " skipped! 🚫"
fi
echo -n "$prefix Executing run-finish-hook.sh..."
test -f /opt/publik/hooks/$HOSTNAME/run-finish-hook.sh && ( /opt/publik/hooks/$HOSTNAME/run-finish-hook.sh && echo " done! ✅" || echo " failed! ❌") || echo " skipped! 🚫"

echo "$prefix 🏁 Script finished 🏁"
echo "$prefix 🏁 Starting syslog tail 🏁"
tail -f /var/log/syslog
