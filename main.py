import json
import socket

import requests as requests

TOKEN = ""  # cloudflare token
ZONE = ""  # cloudflare zode
SUB_DOMAIN = "local"  # subdomain to use local.cloud.com
RECORD_ID = ""  # DNS RECORD ID


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # use open vpn sub-mask
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def set_ip(ip):
    data = {"type": "A", "name": SUB_DOMAIN, "content": ip, "ttl": 120, "proxied": False}
    response = requests.patch(url=f"https://api.cloudflare.com/client/v4/zones/{ZONE}/dns_records/{RECORD_ID}",
                              data=json.dumps(data, indent=4),
                              headers={
                                  "Content-Type": "application/json",
                                  "Authorization": f"Bearer {TOKEN}",
                              })
    print(response.json())


if __name__ == '__main__':
    ip = get_ip()
    if ip.startswith("10.8.0"):
        set_ip(ip)
    else:
        print(f"Device not connected to VPN - {ip}")
