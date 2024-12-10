#!/bin/bash

prefix="✨ cron_monkey_patch.sh ·"
monkey_prefix="🐒Monkey-patching"

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

# WEB-4156: Randomize the minute of the cron job "tenant_command cron"
minute=$((RANDOM % 59 + 1))
original_line=$(grep "combo-manage tenant_command cron" $uwsgi_ini_path)
sed -i "/combo-manage tenant_command cron/ s/minute=[^,]*,/minute=$minute,/" $uwsgi_ini_path
modified_line=$(grep "combo-manage tenant_command cron" $uwsgi_ini_path)
echo "✨ $cron_def ($cur_brick) · Original line: $original_line"
echo "🔁 $cron_def ($cur_brick) · Modified line: $modified_line"


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