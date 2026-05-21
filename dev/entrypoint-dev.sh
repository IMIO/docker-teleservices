#!/bin/bash
set -e

echo "=== Dev entrypoint: installing mounted iMio packages ==="

# pip install mounted iMio packages in editable mode (overrides apt-installed versions)
if [ -d /opt/imio-src ]; then
  for pkg_dir in /opt/imio-src/*/; do
    if [ -f "$pkg_dir/setup.py" ] || [ -f "$pkg_dir/pyproject.toml" ]; then
      echo "  pip install --no-deps -e $pkg_dir"
      pip install --no-deps --break-system-packages -e "$pkg_dir" 2>&1 | tail -1
    fi
  done
fi

echo "=== Dev entrypoint done, starting prod run.sh ==="
exec /run.sh
