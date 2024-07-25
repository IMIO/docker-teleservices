#!/bin/bash

prefix="✨ fix_wcs_utf8.sh ·"

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
