#!/bin/bash

export LANG=C.UTF-8
printenv >>/etc/environment # set env variables for cron jobs
log_prefix="✨ run.sh ·"
monkey_prefix="🐒Monkey-patching"
echo "$prefix cleaning some pid/sock files that can be generated at image creation (if they exist)."
for file in /var/run/{authentic2-multitenant/authentic2-multitenant,chrono/chrono,fargo/fargo,hobo/hobo,combo/combo,nginx,rsyslogd,supervisord,wcs,passerelle/passerelle,bijoe/bijoe}.{pid,sock}; do
  test -e $file && rm $file
done

echo "$prefix updating some Entr'Ouvert services folders user:group via chown."
chown authentic-multitenant:authentic-multitenant /var/lib/authentic2-multitenant/tenants -R
chown hobo:hobo /var/lib/hobo/tenants -R
chown bijoe:bijoe /var/lib/bijoe/tenants -R
chown chrono:chrono /var/lib/chrono/tenants -R
chown combo:combo /var/lib/combo/tenants -R
chown fargo:fargo /var/lib/fargo/tenants -R
chown passerelle:passerelle /var/lib/passerelle/tenants -R
chown wcs:wcs /var/lib/wcs -R

echo "$prefix verifying uploads & attachments permission folders."
[ -d /var/lib/wcs/tenants/*/attachments ] && chown -R wcs:wcs /var/lib/wcs/tenants/*/attachments/
[ -d /var/lib/wcs/tenants/*/uploads ] && chown -R wcs:wcs var/lib/wcs/tenants/*/uploads/

echo "$prefix $monkey_prefix mails via '/var/lib/authentic2/locale/fr/LC_MESSAGES/mail-translation.py'."
python3 /var/lib/authentic2/locale/fr/LC_MESSAGES/mail-translation.py

echo "$prefix INFRA-5052 - Database update"
test -e /var/lib/wcs/configure-wcs.py && python3 /var/lib/wcs/configure-wcs.py

echo "$prefix linking iMio wcs_scripts_teleservices."
if [ -d /opt/publik/wcs-scripts/wcs_scripts_teleservices ]; then
  ln -sfn /opt/publik/wcs-scripts/wcs_scripts_teleservices /var/lib/wcs/scripts
else
  ln -sfn /opt/publik/wcs-scripts /var/lib/wcs/scripts
fi

HOSTNAME=$(hostname)
test -f /opt/publik/hooks/$HOSTNAME/run-hook.sh && echo "$prefix exec run-hook.sh" && /opt/publik/hooks/$HOSTNAME/run-hook.sh

echo "$prefix  Check if UTF8 is well configured (wcs cron jobs)."
if ! grep -q 'LANG=C.UTF-8' /etc/cron.d/wcs; then
  sed -i '2i LANG=C.UTF-8' /etc/cron.d/wcs
  if [ $? -eq 0 ]; then
    echo " --- LANG=C.UTF-8 has been added to /etc/cron.d/wcs ..."
  else
    echo " --- I encoutered a problem with the sed command ..."
  fi
else
  echo " --- the /etc/cron.d/wcs file is well configured with the LANG=C.UTF-8 option ! :-)"
fi

echo "$prefix  Restarting services : rsyslob, cron."
service rsyslog start
service cron start

# should be commented or explained soon
if [ x$1 != xfromgit ] || [ ! -d /opt/publik/combo ]; then
  service combo start
fi
if [ x$1 != xfromgit ] || [ ! -d /opt/publik/authentic ]; then
  test -e /var/lib/authentic2-multitenant/tenants/configure.py && python3 /var/lib/authentic2-multitenant/tenants/configure.py
  service authentic2-multitenant start
fi
if [ x$1 != xfromgit ] || [ ! -d /opt/publik/wcs ]; then
  service wcs start
fi
if [ x$1 != xfromgit ] || [ ! -d /opt/publik/passerelle ]; then
  service passerelle start
fi

# Monkey patching chrono uwsgi.ini (cron jobs)
cur_brick="chrono"
uwsgi_ini_path="/etc/chrono/uwsgi.ini"
echo "$prefix $monkey_prefix $cur_brick $uwsgi_init_path (cron jobs)"
declare -A chrono_crons=(
  ["cancel_events"]="-11 -6"
  ["send_email_notifications"]="-11 -6"
  ["update_event_recurrences"]="-11 -6"
  ["clearsessions"]="4 6"
  ["send_booking_reminders"]="16 24"
  ["sync_desks_timeperiod_exceptions"]="23 33"
  ["anonymize_bookings"]="32 43"
  ["update_shared_custody_holiday_rules"]="47 53"
  ["sync_desks_timeperiod_exceptions_from_settings"]="43 59"
)
declare -a chrono_used_minutes=()
for cron_def in "${!chrono_crons[@]}"; do
  IFS=' ' read -r -a range <<<"${chrono_crons[$cron_def]}"
  while :; do
    minute=$((RANDOM % (range[1] - range[0] + 1) + range[0]))
    if [[ ! " ${chrono_used_minutes[@]} " =~ " ${minute} " ]]; then
      break
    fi
  done
  chrono_used_minutes+=("$minute")
  original_line=$(grep "$cron_def" $uwsgi_ini_path)
  sed -i "/$cron_def/ s/minute=[^,]*,/minute=$minute,/" $uwsgi_ini_path
  modified_line=$(grep "$cron_def" $uwsgi_ini_path)
  echo "✨ $cron_def ($cur_brick) · Original line: $original_line"
  echo "🔁 $cron_def ($cur_brick) · Modified line: $modified_line"
done

# Monkey patching authentic2 uwsgi.ini (cron jobs)
cur_brick="authentic2-multitenant"
uwsgi_ini_path="/etc/authentic2-multitenant/authentic2-multitenant-uwsgi.ini"
echo "$prefix $monkey_prefix $cur_brick $uwsgi_init_path (cron jobs)"
declare -A authentic_crons=(
  ["clearsessions"]="2 4"
  ["cleanupauthentic"]="15 22"
  ["clean-unused-accounts"]="23 43"
  ["clean-user-exports"]="1 5"
  ["sync-ldap-users"]="19 27"
  ["deactivate-orphaned-ldap-users"]="32 56"
)
declare -a authentic_used_minutes=()
for cron_def in "${!authentic_crons[@]}"; do
  IFS=' ' read -r -a range <<<"${authentic_crons[$cron_def]}"
  while :; do
    minute=$((RANDOM % (range[1] - range[0] + 1) + range[0]))
    if [[ ! " ${authentic_used_minutes[@]} " =~ " ${minute} " ]]; then
      break
    fi
  done
  authentic_used_minutes+=("$minute")
  original_line=$(grep "$cron_def" $uwsgi_ini_path)
  sed -i "/$cron_def/ s/minute=[^,]*,/minute=$minute,/" $uwsgi_ini_path
  modified_line=$(grep "$cron_def" $uwsgi_ini_path)
  echo "✨ $cron_def ($cur_brick) · Original line: $original_line"
  echo "🔁 $cron_def ($cur_brick) · Modified line: $modified_line"
done

echo "✨ run.sh ·  Alter bijoe job to run them at random time."
cp /opt/publik/scripts/scripts_teleservices/bijoe_cron_randomizer/bijoe_new_cron /etc/cron.d/bijoe_random
sed -i "s/^0/$(((RANDOM % 60)))/" /etc/cron.d/bijoe
echo "✨ run.sh ·  Alter combo jobs to run them at random time."
sed -i "s/0 8/$(((RANDOM % 60))) $((6 + (RANDOM % 6)))/" /etc/cron.d/combo
sed -i "s#\*/10#$(((RANDOM % 9)))-59/10#" /etc/cron.d/combo
echo "✨ run.sh ·  Alter hobo jobs to run them at random time."
sed -i "s/50/$((40 + (RANDOM % 16)))/" /etc/cron.d/hobo-agent
echo "✨ run.sh ·  Alter passerelle jobs to run them at random time."
sed -i "s/cron = -5/cron = -$((5 + (RANDOM % 6)))/" /etc/passerelle/uwsgi.ini
sed -i "s/cron = 1 -1/cron = $((6 + (RANDOM % 10))) -1/" /etc/passerelle/uwsgi.ini
sed -i "s/cron = 17 -1/cron = $((17 + (RANDOM % 40))) -1/" /etc/passerelle/uwsgi.ini
echo "✨ run.sh ·  Alter hourly root jobs to run them at random time."
sed -i "s/^17/$(((RANDOM % 60)))/" /etc/crontab

echo "$prefix Starting services : hobo, fargo, bijoe, chrono, nginx, supervisor."
service hobo start
service fargo start
service bijoe update
service bijoe start
service chrono start
service nginx start
service supervisor start

if [ ! -f "/var/lib/wcs/skeletons/modele.zip" ]; then
  echo "$prefix Zipping wcs database config and cooking"
  zip -j /var/lib/wcs/skeletons/modele.zip /var/lib/wcs/skeletons/site-options.cfg /var/lib/wcs/skeletons/config.json
  sudo -u hobo hobo-manage cook /etc/hobo/recipe.json
fi
echo "$prefix Running hobo-manage cook /etc/hobo/recipe.json & setup wcs with our postrgesql"
sudo -u hobo hobo-manage cook /etc/hobo/recipe.json
test -e /etc/hobo/recipe*extra.json && sudo -u hobo hobo-manage cook /etc/hobo/recipe*extra.json
test -e /etc/hobo/extra/recipe*json && sudo -u hobo hobo-manage cook /etc/hobo/extra/recipe*.json

# should be commented or explained soon
if [ x$1 = xfromgit ]; then
  /opt/publik/scripts/scripts_teleservices/init-dev.sh
  screen -d -m -c /opt/publik/screenrc
fi

# iMio DE/FR translations monkey patch
# Should only run on Eupen or Kelmis
if [ -e /var/lib/wcs/tenants/eupen-formulaires.guichet-citoyen.be/ ] || [ -e /var/lib/wcs/tenants/kelmis-formulaires.guichet-citoyen.be/ ]; then
  echo "$prefix Eupen/Kelmis 🐒Monkey patch"
  echo "✨ Fetching raw file from GitHub for authentic..."
  curl https://raw.githubusercontent.com/IMIO/teleservices-german-translations/main/authentic2_django.po -o /usr/lib/python3/dist-packages/authentic2/locale/fr/LC_MESSAGES/django.po
  echo "Running django-admin compilemessages for authentic..."
  cd /usr/lib/python3/dist-packages/authentic2
  django-admin compilemessages
  cd -
  echo "✨ Restarting authentic..."
  service authentic2-multitenant restart
  echo "✨ Fetching raw file from GitHub for wcs..."
  curl https://raw.githubusercontent.com/IMIO/teleservices-german-translations/main/wcs_django.po -o /usr/lib/python3/dist-packages/wcs/locale/fr/LC_MESSAGES/django.po
  echo "✨ Running django-admin compilemessages for wcs..."
  cd /usr/lib/python3/dist-packages/wcs/
  django-admin compilemessages
  cd -
  echo "✨ Restarting wcs..."
  service wcs restart
  echo "✨ Fetching raw file from GitHub for combo..."
  curl https://raw.githubusercontent.com/IMIO/teleservices-german-translations/main/combo_django.po -o /usr/lib/python3/dist-packages/combo/locale/fr/LC_MESSAGES/django.po
  cd /usr/lib/python3/dist-packages/combo/
  echo "✨ Running django-admin compilemessages for combo..."
  django-admin compilemessages
  cd -
  service combo restart
  echo "✨ Fetching raw file from GitHub for auquotidien..."
  curl https://raw.githubusercontent.com/IMIO/teleservices-german-translations/main/auquotidien_django.po -o /usr/lib/python3/dist-packages/auquotidien/locale/fr/LC_MESSAGES/django.po
  echo "✨ Running django-admin compilemessages for auquotidien..."
  cd /usr/lib/python3/dist-packages/auquotidien
  django-admin compilemessages
  cd -
  echo "Restarting wcs..."
  service wcs restart
fi

echo "$prefix Update package of wcs elements."
if [ -f /etc/hobo/init.sh ]; then /etc/hobo/init.sh; fi
test -f /opt/publik/hooks/$HOSTNAME/run-finish-hook.sh && /opt/publik/hooks/$HOSTNAME/run-finish-hook.sh
tail -f /var/log/syslog
