#!/bin/bash
set -e

echo "=== Dev entrypoint: installing mounted iMio packages ==="

# pip install mounted iMio packages in editable mode (overrides apt-installed versions)
if [ -d /opt/imio-src ]; then
  for pkg_dir in /opt/imio-src/*/; do
    if [ -f "$pkg_dir/setup.py" ] || [ -f "$pkg_dir/pyproject.toml" ]; then
      echo "  pip install --no-deps -e $pkg_dir"
      if ! pip install --no-deps --break-system-packages -e "$pkg_dir" > /tmp/pip_out.txt 2>&1; then
        echo "  ERROR: pip install failed for $pkg_dir:"
        cat /tmp/pip_out.txt
        exit 1
      fi
      tail -1 /tmp/pip_out.txt
    else
      echo "  WARN: $pkg_dir has no setup.py/pyproject.toml — skipping (run 'make clone-src'?)"
    fi
  done
fi

echo "=== Dev entrypoint done, starting prod run.sh ==="
exec /run.sh
