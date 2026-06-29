import time
import datetime
import smtplib
import socket
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests

# ==================== Cloud Email Configuration ====================
URL_BASE = "https://enzanso-reservation.jp"
TARGET_YEAR_MONTH = "2026年10月"
TARGET_DAY = "3"  # 🎯 Formally locked onto October 3rd for your Mt. Yarigatake trek!

# ✉️ Please fill in your traditional email credentials here:
SENDER_EMAIL = "juvenmini@gmail.com"
PASSWORD = "qywcsfzqrpvemoyo"         # 💡 Your 16-letter App Password (e.g. "abcdefghijklmnop")
RECIPIENT_EMAIL = "syht20@gmail.com" # 💡 Your recipient inbox

EMAIL_SUBJECT = "🚨<Book now!>ヒュッテ大槍 Oct 3 has become available"
# ===================================================================

def send_alert_email(current_status_text):
    msg = MIMEMultipart()
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #d9534f;">🔥 [Hut Oyari] Vacancy Alert for October 3rd!</h2>
        <p>Dear Climber,</p>
        <p>Our cloud monitoring system has successfully detected a change on the official reservation server. 
        <b>October 3rd</b> is no longer fully booked!</p>
        <p>Current Room Status Code: <span style="background-color: #f0ad4e; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: white;">{current_status_text}</span></p>
        <p>This indicates that a cancellation has just been released. Please act immediately before others take it!</p>
        <br>
        <div style="margin: 20px 0;">
          <a href="{URL_BASE}" style="background-color: #5cb85c; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Book on Official Site</a>
        </div>
        <br>
        <hr style="border: 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #777;"><i>(This email is fully automated by Microsoft GitHub cloud server. You can safely keep your personal computer turned off.)</i></p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    smtp_target = "://gmail.com"
    try: socket.gethostbyname(smtp_target)
    except socket.gaierror: smtp_target = "64.233.189.108"

    try:
        server = smtplib.SMTP_SSL(smtp_target, 465, timeout=15)
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✉️ Alert email successfully delivered to recipient!")
    except Exception as e:
        try:
            server = smtplib.SMTP(smtp_target, 587, timeout=15)
            server.starttls()
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
            server.quit()
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✉️ Alert email delivered via backup secure channel.")
        except Exception as e2:
            print("❌ Critical: Mail transmission failed:", e2)

def check_oyari_cloud_form_version():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": URL_BASE,
        "Origin": "https://enzanso-reservation.jp"
    })
    try:
        session.get(URL_BASE, timeout=15)
        payload = {"p": "30", "y": "2026", "m": "10", "agree": "1"}
        res = session.post("https://enzanso-reservation.jp", data=payload, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        list_items = soup.find_all('li')
        day_stripped = str(int(TARGET_DAY))
        found_day = False
        
        for li in list_items:
            li_html = str(li)
            cell_text = li.get_text(" ", strip=True)
            cell_text_clean = "".join(cell_text.split())
            
            if re.search(r'(?<!\d)' + day_stripped + r'(?!\d)', cell_text_clean) and ("class=\"day\"" in li_html or "div" in li_html):
                if "previous" not in li_html and "next" not in li_html and "calendarDate" not in li_html:
                    found_day = True
                    if "阻" in cell_text_clean or "満" in cell_text_clean or "满" in cell_text_clean or "-" in cell_text_clean or "－" in cell_text_clean:
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 📡 Cloud loop: Oct {day_stripped} is still fully booked ({cell_text_clean}).")
                    else:
                        print(f"🔥 [Vacancy Detected!] October {day_stripped} is currently available!")
                        send_alert_email(cell_text_clean)
                    break
                    
        if not found_day:
            full_raw_html = "".join(res.text.split())
            if f"{day_stripped}満" in full_raw_html or f"{day_stripped}_滿" in full_raw_html or f"{day_stripped}满" in full_raw_html:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 📡 Fuzzy Filter: Oct {day_stripped} is confirmed still fully booked.")
            else:
                print(f"🔥 [Fuzzy Breakout Success!] Oct {day_stripped} has NO booking block feature!")
                send_alert_email("Available")
    except Exception as e:
        print("Cloud Form inspection encounter an issue:", e)

if __name__ == "__main__":
    check_oyari_cloud_form_version()
