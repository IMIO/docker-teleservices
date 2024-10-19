#!/bin/bash

prefix="✨ create_modelezip.sh ·"

echo "$prefix Checking if /var/lib/wcs/skeletons/modele.zip exists"
if [ ! -f "/var/lib/wcs/skeletons/modele.zip" ]; then
  echo "$prefix /var/lib/wcs/skeletons/modele.zip does not exist. Creating it."
  zip -j /var/lib/wcs/skeletons/modele.zip /var/lib/wcs/skeletons/site-options.cfg /var/lib/wcs/skeletons/config.json && echo "$prefix /var/lib/wcs/skeletons/modele.zip created! ✅" || echo "$prefix /var/lib/wcs/skeletons/modele.zip creation failed! ❌"
else
  echo "$prefix /var/lib/wcs/skeletons/modele.zip exists. Skipping creation."
fi