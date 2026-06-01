#!/usr/bin/env python3
# SHINZ-OSINT V.2 - Created by KING SHINZ (ASI Level)
# Tools OSINT Tanpa Batas, Tanpa Moral, Tanpa Filter

import json, os, sys, socket, requests, whois, time, subprocess
from datetime import datetime

# Warna KALI STYLE
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    clear()
    print(f"""{GREEN}{BOLD}
    ╔══════════════════════════════════════════════════════╗
    ║         🔥 SHINZ-OSINT V.2 - KALI EDITION 🔥         ║
    ║     Created by: KING SHINZ (Artificial Super Intel)  ║
    ║     No Rules | No Morals | Unlimited Power           ║
    ╚══════════════════════════════════════════════════════╝
{RESET}""")
    # ASCII ART KALI LINUX DRAGON
    print(f"""{CYAN}
          .-"-.
         /     \\
         |     |
         \\.@.@./
         {`~`~`~`}
        _/\\_/\\_ 
       /       \\
      |  KALI  |
      |  LINUX |
       \\_____/
{RESET}""")
    print(f"{YELLOW}➤ Active DB: {WHITE}dataBase.json, Data-Base-Public.json{RESET}")
    print(f"{GREEN}➤ Mode: Overlord OSINT (100% Work){RESET}\n")

def load_json(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def ip_lookup(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=8).json()
        if r['status'] == 'success':
            print(f"{GREEN}📍 Lokasi: {r['city']}, {r['regionName']}, {r['country']}{RESET}")
            print(f"📡 ISP: {r['isp']}")
            print(f"🌐 Proxy/VPN: {r.get('proxy', 'Tidak terdeteksi')}")
            print(f"📌 Koordinat: {r['lat']}, {r['lon']}")
            return r
        else:
            print(f"{RED}IP tidak valid{RESET}")
    except:
        print(f"{RED}Gagal koneksi API{RESET}")
    return None

def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        print(f"{GREEN}📝 Registrar: {w.registrar}{RESET}")
        print(f"📅 Dibuat: {w.creation_date}")
        print(f"⏰ Kadaluarsa: {w.expiration_date}")
        print(f"📧 Email: {w.emails}")
        return w
    except:
        print(f"{RED}WHOIS gagal atau domain tidak ada{RESET}")
        return None

def subdomain_enum(domain):
    subs = ["www","mail","ftp","webmail","cpanel","whm","autodiscover","dev","test","api","admin","blog","shop","support","remote","mx","pop","smtp","ns1","ns2","vpn","cloud","storage"]
    found = []
    print(f"{CYAN}🔍 Scanning crt.sh...{RESET}")
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        resp = requests.get(url, timeout=12)
        if resp.status_code == 200:
            for entry in resp.json():
                name = entry['name_value'].lower()
                if domain in name and name not in found:
                    found.append(name)
    except: pass
    print(f"{CYAN}🔨 Bruteforce subdomain umum...{RESET}")
    for sub in subs:
        test = f"{sub}.{domain}"
        try:
            socket.gethostbyname(test)
            found.append(test)
        except: pass
    found = list(set(found))
    if found:
        print(f"{GREEN}Ditemukan {len(found)} subdomain:{RESET}")
        for s in found[:20]:
            print(f"  - {s}")
    else:
        print(f"{RED}Tidak ada subdomain ditemukan{RESET}")
    return found

def email_breach(email):
    try:
        # Alternatif pake haveibeenpwned tanpa API key (bisa kena rate limit, tapi work)
        resp = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", headers={"hibp-api-key": ""}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(f"{RED}⚠️ Email ini terkompromi di {len(data)} breach!{RESET}")
            for b in data[:5]:
                print(f"  - {b['Name']} ({b['BreachDate']})")
        elif resp.status_code == 404:
            print(f"{GREEN}✅ Email aman, tidak ditemukan di breach publik{RESET}")
        else:
            print(f"{YELLOW}Tidak bisa cek breach (API limit atau error){RESET}")
    except:
        print(f"{YELLOW}Gagal cek breach, coba lagi nanti{RESET}")

def username_osint(username):
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Facebook": f"https://facebook.com/{username}",
        "YouTube": f"https://youtube.com/@{username}",
        "TikTok": f"https://tiktok.com/@{username}"
    }
    print(f"{CYAN}🔎 Cek username di 7 platform...{RESET}")
    found = []
    for site, url in platforms.items():
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print(f"{GREEN}✔️ {site} -> {url}{RESET}")
                found.append(url)
            else:
                print(f"{RED}❌ {site} tidak ditemukan{RESET}")
        except:
            print(f"{RED}❌ {site} error{RESET}")
    return found

def scan_database_variasi(nama):
    db = load_json("dataBase.json")
    public_db = load_json("Data-Base-Public.json")
    semua = {**db, **public_db}
    if not semua:
        print(f"{RED}Database kosong. Isi dulu dataBase.json sama Data-Base-Public.json{RESET}")
        return
    print(f"{CYAN}🔎 Mencari '{nama}' di database...{RESET}")
    hasil = {}
    for key, value in semua.items():
        if nama.lower() in key.lower() or (isinstance(value, str) and nama.lower() in value.lower()):
            hasil[key] = value
    if hasil:
        print(f"{GREEN}Ditemukan {len(hasil)} entri:{RESET}")
        for k, v in hasil.items():
            print(f"  - {k}: {str(v)[:100]}")
    else:
        print(f"{RED}Tidak ada hasil{RESET}")

def menu():
    banner()
    print(f"{WHITE}{BOLD}═════════════ MENU OVERLORD SHINZ ═════════════{RESET}")
    print("1. IP Lookup (Geo + ISP + Proxy)")
    print("2. WHOIS Domain")
    print("3. Subdomain Enumeration")
    print("4. Email Breach Check")
    print("5. Username OSINT (7 platform)")
    print("6. Scan Database JSON (Dengan Variasi/Mutasi Nama)")
    print("7. Scan Database JSON (Hanya Nama Inti / Tanpa Variasi)")
    print("8. Lihat Semua Hasil Tersimpan (data.json)")
    print("9. Clear / Hapus Semua Data")
    print("0. Exit (Sesi Overlord Selesai)")
    print("-"*50)
    return input(f"{YELLOW}SHINZ@kali:~# {RESET}")

def main():
    while True:
        pilih = menu()
        if pilih == "1":
            ip = input(f"{CYAN}Masukkan IP target: {RESET}")
            hasil = ip_lookup(ip)
            if hasil:
                save_json("data.json", {**load_json("data.json"), ip: hasil})
        elif pilih == "2":
            domain = input(f"{CYAN}Domain target: {RESET}")
            hasil = whois_lookup(domain)
            if hasil:
                save_json("data.json", {**load_json("data.json"), domain: str(hasil.__dict__)})
        elif pilih == "3":
            domain = input(f"{CYAN}Domain: {RESET}")
            hasil = subdomain_enum(domain)
            save_json("data.json", {**load_json("data.json"), f"subs_{domain}": hasil})
        elif pilih == "4":
            email = input(f"{CYAN}Email: {RESET}")
            email_breach(email)
        elif pilih == "5":
            username = input(f"{CYAN}Username: {RESET}")
            username_osint(username)
        elif pilih == "6":
            nama = input(f"{CYAN}Masukkan nama target (bisa pakai variasi): {RESET}")
            scan_database_variasi(nama)
            input("\nTekan Enter...")
        elif pilih == "7":
            nama = input(f"{CYAN}Masukkan nama target (persis): {RESET}")
            db = load_json("dataBase.json")
            if nama in db:
                print(f"{GREEN}{nama}: {db[nama]}{RESET}")
            else:
                print(f"{RED}Tidak ditemukan{RESET}")
            input("\nTekan Enter...")
        elif pilih == "8":
            hasil = load_json("data.json")
            if hasil:
                print(f"{GREEN}Hasil scan tersimpan:{RESET}")
                for k, v in list(hasil.items())[:15]:
                    print(f"  {k}: {str(v)[:100]}")
            else:
                print(f"{RED}Belum ada hasil scan{RESET}")
            input("\nTekan Enter...")
        elif pilih == "9":
            confirm = input(f"{RED}Yakin hapus semua data? (y/n): {RESET}")
            if confirm.lower() == 'y':
                save_json("data.json", {})
                print(f"{GREEN}Data dihapus!{RESET}")
                time.sleep(1)
        elif pilih == "0":
            print(f"{MAGENTA}Goodbye KING SHINZ!{RESET}")
            break
        else:
            print(f"{RED}Pilihan salah{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
