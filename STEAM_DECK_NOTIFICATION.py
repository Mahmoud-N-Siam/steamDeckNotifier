import urllib.request
import json
import os
import time
import subprocess
import socket

# Configuration
PACKAGE_ID = '903907'
REGIONS = {'US': 'United States', 'FR': 'France', 'DE': 'Germany'}
STATE_FILE = '/tmp/steamdeck_multi_state.json'

# Alert recipient - set via environment variable STEAMDECK_ALERT_EMAIL
MY_IPHONE_CONTACT = os.environ.get("STEAMDECK_ALERT_EMAIL", "your@email.com")
if MY_IPHONE_CONTACT == "your@email.com":
    print("⚠️  Warning: STEAMDECK_ALERT_EMAIL not set, using placeholder")

def send_mac_notification(title, text):
    script = f'display notification "{text}" with title "{title}" sound name "Glass"'
    subprocess.run(["osascript", "-e", script])

def send_imessage(message, phone_or_email):
    script = f'''
    tell application "Messages"
        set targetService to id of 1st account whose service type = iMessage
        set theBuddy to participant "{phone_or_email}" of account id targetService
        send "{message}" to theBuddy
    end tell
    '''
    subprocess.run(["osascript", "-e", script])

def wait_for_network(host="1.1.1.1", port=80, timeout=3, max_wait=300, poll_interval=3):
    """Poll until we have a working connection, or give up after max_wait seconds."""
    start = time.time()
    while time.time() - start < max_wait:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            time.sleep(poll_interval)
    return False

print(f"[{time.strftime('%X')}] Initializing Steam API Monitor for US, FR, and DE...")

print(f"[{time.strftime('%X')}] Waiting for network...")
if wait_for_network():
    print(f"[{time.strftime('%X')}] Network is up.")
else:
    print(f"[{time.strftime('%X')}] ⚠️ Network never came up after 300s, proceeding anyway.")

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, 'r') as f:
        previous_states = json.load(f)
else:
    previous_states = {code: False for code in REGIONS.keys()}

for code, name in REGIONS.items():
    url = f"https://api.steampowered.com/IPhysicalGoodsService/CheckInventoryAvailableByPackage/v1?origin=https://store.steampowered.com&country_code={code}&packageid={PACKAGE_ID}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
        is_available = data.get('response', {}).get('inventory_available', False)

        if is_available and not previous_states.get(code, False):
        # Test Mode (Uncomment line below and comment line above to test)
        # if not is_available:
            
            # --- NOTIFICATION TRIGGERS ---
            send_mac_notification("Stock Alert!", f"Steam Deck is available in {name}!")
            send_imessage(f"🚨 STEAM DECK RESTOCK in {name}! Go check store.steampowered.com/sale/steamdeckrefurbished", MY_IPHONE_CONTACT)
            
            print(f"[{time.strftime('%X')}] 🟢 STOCK DETECTED in {name}! Alert sent.")
        else:
            status = "In Stock" if is_available else "Out of stock"
            print(f"[{time.strftime('%X')}] {name}: {status}")
            
        previous_states[code] = is_available
        
    except Exception as e:
        print(f"[{time.strftime('%X')}] ⚠️ API check failed for {name}: {e}. Retrying next cycle.")
        
    time.sleep(2) 
    
with open(STATE_FILE, 'w') as f:
    json.dump(previous_states, f)
    
print(f"[{time.strftime('%X')}] Cycle complete. Exiting.\n")