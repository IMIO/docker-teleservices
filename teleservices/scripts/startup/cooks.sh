#!/bin/bash

prefix="✨ cooks.sh ·"

echo "$prefix Running hobo-manage cook /etc/hobo/recipe.json..."
sudo -u hobo hobo-manage cook /etc/hobo/recipe.json && echo " hobo-manage cook /etc/hobo/recipe.json done! ✅" || echo " hobo-manage cook /etc/hobo/recipe.json failed! ❌"

echo -n "$prefix Running hobo-manage cook /etc/hobo/recipe*extra.json..."
test -e /etc/hobo/recipe*extra.json && (sudo -u hobo hobo-manage cook /etc/hobo/recipe*extra.json && echo " done! ✅" || echo " failed! ❌") || echo " skipped! 🚫"

echo -n "$prefix Running hobo-manage cook /etc/hobo/extra/recipe*.json..."
test -e /etc/hobo/extra/recipe*json && (sudo -u hobo hobo-manage cook /etc/hobo/extra/recipe*.json && echo " done! ✅" || echo " failed! ❌") || echo " skipped! 🚫 "
