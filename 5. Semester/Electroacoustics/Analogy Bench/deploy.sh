#!/usr/bin/env bash
# Build and push the bench to the home server: CT 116 "study" (192.168.50.220), nginx.
# The desktop key only reaches the Proxmox host, so files go host -> pct push -> container.
set -euo pipefail
cd "$(dirname "$0")"
python3 build.py
tar czf /tmp/analogy-bench.tgz -C dist .
scp -q /tmp/analogy-bench.tgz root@192.168.50.200:/tmp/analogy-bench.tgz
ssh root@192.168.50.200 '
  pct push 116 /tmp/analogy-bench.tgz /tmp/analogy-bench.tgz &&
  pct exec 116 -- bash -c "mkdir -p /var/www/analogy-bench && tar xzf /tmp/analogy-bench.tgz -C /var/www/analogy-bench && rm /tmp/analogy-bench.tgz && chown -R www-data:www-data /var/www/analogy-bench && nginx -s reload" &&
  rm /tmp/analogy-bench.tgz'
echo "deployed → http://192.168.50.220/"
