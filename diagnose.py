import requests
from bs4 import BeautifulSoup

URL_BASE = "https://enzanso-reservation.jp"

def do_diagnose():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": URL_BASE,
        "Origin": "https://enzanso-reservation.jp"
    })
    
    print("🚀 [DIAGNOSTIC] Step 1: Requesting base URL...")
    res1 = session.get(URL_BASE, timeout=15)
    print(f" -> Base URL Status Code: {res1.status_code}")
    
    print("🚀 [DIAGNOSTIC] Step 2: Posting Payload for October 2026...")
    payload = {"p": "30", "y": "2026", "m": "10", "agree": "1"}
    res2 = session.post("https://enzanso-reservation.jp", data=payload, timeout=15)
    res2.encoding = 'utf-8'
    
    print(f" -> Post Status Code: {res2.status_code}")
    print(f" -> Total HTML length received: {len(res2.text)} bytes")
    
    soup = BeautifulSoup(res2.text, 'html.parser')
    list_items = soup.find_all('li')
    print(f" -> Total <li> tags found in HTML: {len(list_items)}")
    
    print("\n📝 [DIAGNOSTIC] Step 3: Printing the first 1000 characters of the received HTML:")
    print("==================================================")
    print(res2.text[:1000])
    print("==================================================")

if __name__ == "__main__":
    do_diagnose()
