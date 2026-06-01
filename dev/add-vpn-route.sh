#!/bin/bash
set -e

HOST="keycloak-apps.cloud.imio-test.be"

echo "Resolving $HOST..."
IP=$(getent hosts "$HOST" | awk '{print $1}')
if [ -z "$IP" ]; then
    echo "ERROR: cannot resolve $HOST"
    exit 1
fi
echo "  -> $IP"

GATEWAY=$(ip route | awk '/^default/ {print $3; exit}')
echo "Default gateway: $GATEWAY"

echo "Adding route: $IP/32 via $GATEWAY"
ip route add "$IP/32" via "$GATEWAY" 2>/dev/null || echo "  (route already exists)"

echo "Testing connectivity..."
curl -fsS --max-time 5 "https://$HOST" -o /dev/null && echo "OK: $HOST is reachable" || echo "FAIL: still not reachable"
