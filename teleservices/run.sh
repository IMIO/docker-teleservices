#!/bin/bash

# Fix problem causing scripts still run by " init.d " not work working properly
# https://dev.entrouvert.org/issues/41958
# https://dev.entrouvert.org/issues/41960
echo "$prefix 🏁 Starting script 🏁"

export LANG=C.UTF-8

printenv >>/etc/environment # set env variables for cron jobs
prefix="✨ run.sh ·"
monkey_prefix="🐒Monkey-patching"
echo -n "$prefix cleaning some pid/sock files that can be generated at image creation (if they exist)."
for file in /var/run/{authentic2-multitenant/authentic2-multitenant,chrono/chrono,fargo/fargo,hobo/hobo,combo/combo,nginx,rsyslogd,supervisord,wcs,passerelle/passerelle,bijoe/bijoe}.{pid,sock}; do
  test -e $file && (rm $file || echo "deletion of $file failed! ❌")
done
echo "$prefix cleaning some pid/sock files that can be generated at image creation (if they exist) done! ✅"

echo -n "$prefix updating some Entr'Ouvert services folders user:group via chown..."
chown authentic-multitenant:authentic-multitenant /var/lib/authentic2-multitenant/tenants -R &&
chown hobo:hobo /var/lib/hobo/tenants -R &&
chown bijoe:bijoe /var/lib/bijoe/tenants -R &&
chown chrono:chrono /var/lib/chrono/tenants -R &&
chown combo:combo /var/lib/combo/tenants -R &&
chown passerelle:passerelle /var/lib/passerelle/tenants -R &&
chown wcs:wcs /var/lib/wcs -R &&
echo " done! ✅"

echo -n "$prefix verifying uploads & attachments permission folders..."
[ -d /var/lib/wcs/tenants/*/attachments ] && (chown -R wcs:wcs /var/lib/wcs/tenants/*/attachments/ && echo -n " attachments done! ✅..." || echo -n " attachments failed! ❌...") || echo -n " attachments skipped! 🚫... "
[ -d /var/lib/wcs/tenants/*/uploads ] && (chown -R wcs:wcs var/lib/wcs/tenants/*/uploads/ && echo " uploads done! ✅" || echo "uploads failed! ❌") || echo " uploads skipped! 🚫"

echo -m "$prefix $monkey_prefix mails via '/var/lib/authentic2/locale/fr/LC_MESSAGES/mail-translation.py'..."
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
test -f /opt/publik/hooks/$HOSTNAME/run-hook.sh && (/opt/publik/hooks/$HOSTNAME/run-hook.sh && echo " done! ✅" || echo "$prefix exec run-hook.sh... failed! ❌") || echo " skipped! 🚫"

echo "$prefix  Check if UTF8 is well configured (wcs cron jobs)."
if ! grep -q 'LANG=C.UTF-8' /etc/cron.d/wcs; then
  sed -i '2i LANG=C.UTF-8' /etc/cron.d/wcs
  if [ $? -eq 0 ]; then
    echo " --- LANG=C.UTF-8 has been added to /etc/cron.d/wcs ..."
  else
    echo " --- I encountered a problem with the sed command ..."
  fi
else
  echo " --- the /etc/cron.d/wcs file is well configured with the LANG=C.UTF-8 option ! :-)"
fi
echo "$prefix  Check if UTF8 is well configured (wcs cron jobs) done! ✅"

echo "$prefix  Restarting services : rsyslog, cron."
# new way to start rsyslog since bookworm
/usr/sbin/rsyslogd && echo -n " rsyslog started! ✅..." || echo -n " rsyslog failed to start! ❌..."

service cron start
echo "$prefix  Restarting services : rsyslob, cron done! ✅"

# Monkey patching chrono uwsgi.ini (cron jobs)
cur_brick="chrono"
uwsgi_ini_path="/etc/chrono/uwsgi.ini"
echo "$prefix $monkey_prefix $cur_brick $uwsgi_ini_path (cron jobs)"
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
echo "$prefix $monkey_prefix $cur_brick $uwsgi_ini_path (cron jobs) done! ✅"

# Monkey patching authentic2 uwsgi.ini (cron jobs)
cur_brick="authentic2-multitenant"
uwsgi_ini_path="/etc/authentic2-multitenant/authentic2-multitenant-uwsgi.ini"
echo "$prefix $monkey_prefix $cur_brick $uwsgi_ini_path (cron jobs)"
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
echo "$prefix $monkey_prefix $cur_brick $uwsgi_ini_path (cron jobs) done! ✅"

# Monkey patching combo uwsgi.ini (cron jobs)
cur_brick="combo"
uwsgi_ini_path="/etc/combo/uwsgi.ini"
echo "$prefix $monkey_prefix $cur_brick $uwsgi_ini_path (cron jobs)"
declare -A combo_crons=(
  ["clear_snapshot_pages"]="34 49"
)

for cron_def in "${!combo_crons[@]}"; do
  IFS=' ' read -r -a range <<<"${combo_crons[$cron_def]}"
  while :; do
    minute=$((RANDOM % (range[1] - range[0] + 1) + range[0]))
    if [[ ! " ${combo_used_minutes[@]} " =~ " ${minute} " ]]; then
      break
    fi
  done
  combo_used_minutes+=("$minute")
  original_line=$(grep "$cron_def" $uwsgi_ini_path)
  sed -i "/$cron_def/ s/minute=[^,]*,/minute=$minute,/" $uwsgi_ini_path
  modified_line=$(grep "$cron_def" $uwsgi_ini_path)
  echo "✨ $cron_def ($cur_brick) · Original line: $original_line"
  echo "🔁 $cron_def ($cur_brick) · Modified line: $modified_line"
done

combo_crond_random_8=$((RANDOM % 5 + 5))    # random number between 5 and 9
combo_crond_random_10=$((RANDOM % 15 + 13)) # random number between 13 and 27
combo_crond_file="/etc/cron.d/combo"
combo_crond_original_line1=$(grep "notify_new_remote_invoices" $combo_crond_file)
combo_crond_original_line2=$(grep "lingo-poll-backend" $combo_crond_file)
echo "✨ notify_new_remote_invoices ($cur_brick) · Original line: $combo_crond_original_line1"
echo "✨ lingo-poll-backend ($cur_brick) · Original line: $combo_crond_original_line2"
sed -i -E "/notify_new_remote_invoices/ s/([0-9]+) ([0-9]+)(.*combo-manage tenant_command notify_new_remote_invoices.*)/0 $combo_crond_random_8\3/;
     /lingo-poll-backend/ s/(\*\/)[0-9]+(.*)/\*\/$combo_crond_random_10\2/" $combo_crond_file
combo_crond_altered_line1=$(grep "notify_new_remote_invoices" $combo_crond_file)
combo_crond_altered_line2=$(grep "lingo-poll-backend" $combo_crond_file)
echo "🔁 notify_new_remote_invoices ($cur_brick) · Modified line: $combo_crond_altered_line1"
echo "🔁 lingo-poll-backend ($cur_brick) · Modified line: $combo_crond_altered_line2"
echo "$prefix $monkey_prefix $cur_brick $uwsgi_ini_path (cron jobs) done! ✅"

# Monkey patching passerelle uwsgi.ini (cron jobs)
cur_brick="passerelle"
uwsgi_ini_path="/etc/passerelle/uwsgi.ini"
echo "$prefix $monkey_prefix $cur_brick $uwsgi_ini_path (cron jobs)"
declare -A passerelle_crons=(
  ["cron --all-tenants availability"]="-11 -21"
  ["cron --all-tenants jobs"]="-11 -21"
  ["clearsessions"]="11 21"
  ["cron --all-tenants hourly"]="42 57"
  ["cron --all-tenants daily"]="25 45"
  ["cron --all-tenants weekly"]="30 55"
  ["cron --all-tenants monthly"]="40 57"
)
declare -a passerelle_used_minutes=()
for cron_def in "${!passerelle_crons[@]}"; do
  IFS=' ' read -r -a range <<<"${passerelle_crons[$cron_def]}"
  while :; do
    minute=$((RANDOM % (range[1] - range[0] + 1) + range[0]))
    if [[ ! " ${passerelle_used_minutes[@]} " =~ " ${minute} " ]]; then
      break
    fi
  done

  passerelle_used_minutes+=("$minute")
  original_line=$(grep "$cron_def" $uwsgi_ini_path)
  sed -i "/$cron_def/ s~unique-cron = [-0-9]*~unique-cron = $minute~" $uwsgi_ini_path
  # echo "DEBUG $original_line"
  # sed -i "/$cron_def/ s~unique-cron = (-\d+|\d+)~unique-cron = $minute~" $uwsgi_ini_path
  # sed -i "/$cron_def/ s/minute=[^,]*,/minute=$minute,/" $uwsgi_ini_path
  modified_line=$(grep "$cron_def" $uwsgi_ini_path)
  echo "✨ $cron_def ($cur_brick) · Original line: $original_line"
  echo "🔁 $cron_def ($cur_brick) · Modified line: $modified_line"
done
echo "$prefix $monkey_prefix $cur_brick $uwsgi_ini_path (cron jobs) done! ✅"

# Monkey patching hobo (cron.d job)
echo "$prefix $monkey_prefix monkey patching hobo_provision (hobo related cron.d job)"
hobo_agent_random=$((RANDOM % 11 + 40)) # random number between 40 and 50
hobo_agent_file="/etc/cron.d/hobo-agent"
hobo_agent_original_line=$(grep "hobo_provision" $hobo_agent_file)
echo "✨ hobo_provision · Original line: $hobo_agent_original_line"

if sed -i -E "/hobo_provision/ s/([0-9]+)(.*hobo_provision.*)/$hobo_agent_random\2/" $hobo_agent_file; then
  echo "Changes applied."
else
  echo "Changes not applied."
fi

hobo_agent_altered_line=$(grep "hobo_provision" $hobo_agent_file)
echo "🔁 hobo_provision · Modified line: $hobo_agent_altered_line"
echo "$prefix $monkey_prefix monkey patching hobo_provision (hobo related cron.d job) done! ✅"

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

echo "$prefix Checking if /var/lib/wcs/skeletons/modele.zip exists"
if [ ! -f "/var/lib/wcs/skeletons/modele.zip" ]; then
  echo "$prefix /var/lib/wcs/skeletons/modele.zip does not exist. Creating it."
  zip -j /var/lib/wcs/skeletons/modele.zip /var/lib/wcs/skeletons/site-options.cfg /var/lib/wcs/skeletons/config.json && echo "$prefix /var/lib/wcs/skeletons/modele.zip created! ✅" || echo "$prefix /var/lib/wcs/skeletons/modele.zip creation failed! ❌"
else
  echo "$prefix /var/lib/wcs/skeletons/modele.zip exists. Skipping creation."
fi
echo "$prefix Running hobo-manage cook /etc/hobo/recipe.json..."
sudo -u hobo hobo-manage cook /etc/hobo/recipe.json && echo " hobo-manage cook /etc/hobo/recipe.json done! ✅" || echo " hobo-manage cook /etc/hobo/recipe.json failed! ❌"

echo -n "$prefix Running hobo-manage cook /etc/hobo/recipe*extra.json..."
test -e /etc/hobo/recipe*extra.json && (sudo -u hobo hobo-manage cook /etc/hobo/recipe*extra.json && echo " done! ✅" || echo " failed! ❌") || echo " skipped! 🚫"

echo -n "$prefix Running hobo-manage cook /etc/hobo/extra/recipe*.json..."
test -e /etc/hobo/extra/recipe*json && (sudo -u hobo hobo-manage cook /etc/hobo/extra/recipe*.json && echo " done! ✅" || echo " failed! ❌") || echo " skipped! 🚫 "

# iMio DE/FR translations monkey patch
# Should only run on Eupen or Kelmis
if [ -e /var/lib/wcs/tenants/eupen-formulaires.guichet-citoyen.be/ ] || [ -e /var/lib/wcs/tenants/kelmis-formulaires.guichet-citoyen.be/ ]; then
  echo "$prefix $monkey_prefix Monkey-patching translations files  (iMio DE/FR translations monkey patch)."
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
  echo "$prefix $monkey_prefix Monkey-patching translations files  (iMio DE/FR translations monkey patch) done! ✅"
fi

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
