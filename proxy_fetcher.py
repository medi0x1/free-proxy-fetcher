import requests
import sys
import time
import base64

def get_key():
    parts = [
        base64.b64decode("bXk=").decode(),
        base64.b64decode("X3NlY3JldA==").decode(),
        base64.b64decode("X2tleQ==").decode(),
        base64.b64decode("XzIwMjU=").decode()
    ]
    return ''.join(parts)

def xor_crypt(data, key):
    key_bytes = key.encode()
    result = bytearray()
    for i, byte in enumerate(data):
        result.append(byte ^ key_bytes[i % len(key_bytes)])
    return bytes(result)

def decrypt_config(encrypted_b64, key):
    encrypted = base64.b64decode(encrypted_b64)
    decrypted = xor_crypt(encrypted, key)
    return decrypted.decode('utf-8')

ENCRYPTED_BASE = "BQ0rAxZZXUoELQQdAHFfVVpRBEttEQANGwNaKAQXEjpAQxxRCA8="
ENCRYPTED_API = "IDwXNyw8Ijc7BzI6S28ABQ=="

k = get_key()
BASE = decrypt_config(ENCRYPTED_BASE, k)
API_KEY = decrypt_config(ENCRYPTED_API, k)
del k

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

POPULAR = ["US", "GB", "DE", "FR", "CA", "AU", "NL", "SE"]

REGIONS = {
    "North America": ["US", "CA", "MX"],
    "Europe": ["GB", "DE", "FR", "IT", "ES", "NL", "PL", "SE", "FI", "DK", 
               "IE", "PT", "CZ", "RO", "BG", "GR", "HU", "LT", "LV", "EE", 
               "SI", "CY", "BY", "UA", "MD"],
    "Asia": ["CN", "IN", "ID", "TH", "VN", "MY", "IL", "TR", "KZ", "KG", 
             "AM", "GE"],
    "Oceania": ["AU"],
    "South America": ["BR"],
    "Africa": ["ZA", "MU", "SC"]
}

def banner():
    print(r"""
  __  __ _____ ____ ___ ___  __  ______ 
 |  \/  | ____|  _ \_ _/ _ \ \ \/ /_  _|
 | |\/| |  _| | | | | | | | | \  /  | |  
 | |  | | |___| |_| | | |_| | /  \ _| |_ 
 |_|  |_|_____|____/___\___/ /_/\_\_____|
         
 by github.com/medi0x1
""")

def get_proxies(country):
    url = f"{BASE}/api/v1/free/proxies"
    params = {"country": country, "key": API_KEY}
    r = requests.get(url, params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    data = r.json()
    return [p for p in data.get("proxies", []) if not p.get("archive")]

def get_proxy_info(country, hostname):
    url = f"{BASE}/api/v1/free/proxy"
    params = {"country": country, "hostname": hostname, "key": API_KEY}
    r = requests.get(url, params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json().get("proxy")

def find_fastest():
    fastest = None
    print("\n[+] Searching fastest proxy...\n")
    
    all_countries = []
    for countries in REGIONS.values():
        all_countries.extend(countries)
    
    for cc in all_countries:
        print(f"Checking {cc}...")
        try:
            proxies = get_proxies(cc)
        except:
            continue
        
        for p in proxies:
            ping = p.get("ping")
            if ping is None:
                continue
            
            if fastest is None or ping < fastest["ping"]:
                fastest = {"country": cc, "hostname": p["hostname"], "ping": ping}
    
    return fastest

def pick_popular():
    print("\n" + "="*50)
    print("  POPULAR COUNTRIES")
    print("="*50)
    
    for i, cc in enumerate(POPULAR, 1):
        print(f"{i}. {cc}")
    print(f"{len(POPULAR) + 1}. Back")
    
    try:
        choice = int(input("\nSelect: ")) - 1
        if choice == len(POPULAR):
            return None
        if 0 <= choice < len(POPULAR):
            return POPULAR[choice]
        print("Invalid!")
        time.sleep(1)
        return None
    except:
        print("Invalid!")
        time.sleep(1)
        return None

def pick_region():
    print("\n" + "="*50)
    print("  SELECT REGION")
    print("="*50)
    
    region_names = list(REGIONS.keys())
    for i, name in enumerate(region_names, 1):
        cnt = len(REGIONS[name])
        print(f"{i}. {name} ({cnt} countries)")
    print(f"{len(region_names) + 1}. Back")
    
    try:
        choice = int(input("\nSelect: ")) - 1
        if choice == len(region_names):
            return None
        if choice < 0 or choice >= len(region_names):
            print("Invalid!")
            time.sleep(1)
            return None
        
        region = region_names[choice]
        countries = REGIONS[region]
        
        print(f"\n{region} Countries:")
        print("-" * 50)
        
        # show 4 per row
        for i in range(0, len(countries), 4):
            row = countries[i:i+4]
            line = ""
            for j, c in enumerate(row):
                line += f"{i+j+1:2}. {c:4}  "
            print(line)
        
        idx = int(input(f"\nSelect (1-{len(countries)}): ")) - 1
        if 0 <= idx < len(countries):
            return countries[idx]
        print("Invalid!")
        time.sleep(1)
        return None
    except:
        print("Invalid!")
        time.sleep(1)
        return None

def search_country():
    all_cc = []
    for countries in REGIONS.values():
        all_cc.extend(countries)
    
    query = input("\nType country code (e.g US, GB) or 'list': ").strip().upper()
    
    if query == "LIST":
        print("\nAll countries:")
        print(", ".join(sorted(all_cc)))
        return search_country()
    
    if query in all_cc:
        return query
    
    print(f"'{query}' not found!")
    time.sleep(1)
    return None

def show_proxy_details(country, hostname):
    details = get_proxy_info(country, hostname)
    if not details:
        print("[-] Failed to get details")
        return
    
    proto = details.get("protocols", {})
    ip = details["ip"]
    user = details["login"]
    pwd = details["password"]
    
    print("\n" + "="*50)
    print("           PROXY DETAILS")
    print("="*50)
    print(f"Country : {country}")
    print(f"IP      : {ip}")
    print(f"Login   : {user}")
    print(f"Pass    : {pwd}")
    print("-"*50)
    
    if "http" in proto:
        print(f"HTTP  : http://{user}:{pwd}@{ip}:{proto['http']}")
    if "socks5" in proto:
        print(f"SOCKS5: socks5://{user}:{pwd}@{ip}:{proto['socks5']}")

def main():
    banner()
    
    while True:
        print("\n" + "="*50)
        print("        FREE PROXY FETCHER")
        print("="*50)
        print("\n1) Popular countries")
        print("2) Browse by region")
        print("3) Search country code")
        print("4) Find fastest proxy")
        print("5) Exit")
        
        choice = input("\nOption: ").strip()
        
        if choice == "5":
            print("\nBye 👋")
            sys.exit(0)
        
        try:
            country = None
            hostname = None
            
            if choice == "4":
                result = find_fastest()
                if not result:
                    print("[-] Nothing found")
                    continue
                
                country = result["country"]
                hostname = result["hostname"]
                print(f"\n[✔] Fastest: {hostname} ({result['ping']} ms)")
            
            elif choice == "1":
                country = pick_popular()
            elif choice == "2":
                country = pick_region()
            elif choice == "3":
                country = search_country()
            else:
                print("Invalid option!")
                time.sleep(1)
                continue
            
            if not country:
                continue
            
            # get proxy list if needed
            if not hostname:
                print(f"\n[+] Loading proxies for {country}...")
                proxies = get_proxies(country)
                if not proxies:
                    print("[-] No proxies available")
                    input("\nPress ENTER...")
                    continue
                
                print(f"\nFound {len(proxies)} proxies:")
                for i, p in enumerate(proxies, 1):
                    ping = p.get("ping") or "N/A"
                    print(f"{i}. {p['hostname']} (ping: {ping})")
                
                idx = int(input("\nSelect proxy: ")) - 1
                if idx < 0 or idx >= len(proxies):
                    print("Invalid!")
                    continue
                hostname = proxies[idx]["hostname"]
            
            show_proxy_details(country, hostname)
            input("\nPress ENTER...")
        
        except Exception as e:
            print(f"[!] Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()