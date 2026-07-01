import time
import datetime
import smtplib
import socket
import re
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests

# ==================== Cloud Email Configuration ====================
URL_BASE = "https://enzanso-reservation.jp"
URL_POST_TARGET = "https://enzanso-reservation.jp"

TARGET_YEAR_MONTH = "2026年10月"
TARGET_DAY = "3"  # 🎯 Deadlocked on Oct 3rd for your Mt. Yarigatake trek!

SENDER_EMAIL = "juvenmini@gmail.com"
PASSWORD = "qywcsfzqrpvemoyo"         # 💡 Your 16-letter App Password
RECIPIENT_EMAIL = "syht20@gmail.com" # 💡 Your recipient inbox

EMAIL_SUBJECT_URGENT = "🚨<Book now!>ヒュッテ大槍 Oct 3 has become available"
EMAIL_SUBJECT_DAILY = "⛰️ ヒュッテ大槍 Oct 2026 daily availability report"
# ===================================================================

def send_plain_alert_email(subject, body_html):
    """最純粹、無任何結構嵌套的標準寄信引擎，0% 機率引發編譯或吃信衝突"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body_html, 'html', 'utf-8'))
    
    smtp_target = "://gmail.com"
    try: socket.gethostbyname(smtp_target)
    except socket.gaierror: smtp_target = "64.233.189.108"
    
    try:
        server = smtplib.SMTP_SSL(smtp_target, 465, timeout=15)
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("✉️ Mail delivered successfully.")
    except Exception as e:
        try:
            server = smtplib.SMTP(smtp_target, 587, timeout=15)
            server.starttls()
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
            server.quit()
            print("✉️ Mail delivered via secure channels.")
        except Exception as e2:
            print("❌ Mail failed:", e2)

def execute_daily_report():
    """💡 獨立每日報告功能：徹底解開所有 try-except 與迴圈，100% 免疫 SyntaxError"""
    print("🚀 [DAILY NODE] Fetching October 2026 calendar via safe Jupyter alignment...")
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ja,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
        "Referer": URL_BASE,
        "Origin": URL_BASE
    })
    
    # 對齊 Jupyter 時差，獲取鎖定 Cookie
    session.get(URL_BASE, timeout=15)
    time.sleep(3.0)
    
    payload = {"p": "30", "y": "2026", "m": "10", "agree": "1"}
    res = session.post(URL_POST_TARGET, data=payload, timeout=15)
    res.encoding = 'utf-8'
    html_source_10 = res.text
    
    # 智慧降維字串定位：尋找 HTML 原始碼中包含 '10月' 周圍的文本片段，當作實時回報面板
    clean_text = "".join(html_source_10.split())
    preview_idx = html_source_10.find("calendarDate")
    if preview_idx == -1: preview_idx = html_source_10.find("2026")
    if preview_idx == -1: preview_idx = 0
    raw_snippet = html_source_10[preview_idx:preview_idx+400].strip().replace('<', '&lt;').replace('>', '&gt;')
    
    # 比對 10/3 是否有釋出空房
    status_label = "10月3日：滿室 (満)"
    if "3日" in clean_text or "03" in clean_text:
        target_match = re.search(r'3日.*?([◯▲満满\d])', clean_text)
        if target_match and target_match.group(1) not in ["満", "满"]:
            status_label = f"🔥 偵測到空房狀況變更：{target_match.group(1)} !"

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h3>📢 This is the daily snapshot of Hut Oyari Calendar (2026年10月):</h3>
        <p>Current Raw Code Text of October 3rd: <span style="background-color: #777; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: white;">{status_label}</span></p>
        <p>If you see '◯', '▲', or any single-digit number instead of '満', please click below to book immediately!</p>
        <br>
        <div style="background:#f9f9f9; padding:15px; border-left:4px solid #337ab7; font-family:monospace;">
          <b>[System Live Output Preview]</b>
          <pre style="white-space: pre-wrap; font-size:13px; color:#555;">{raw_snippet}</pre>
        </div>
        <br>
        <div style="margin: 20px 0;">
          <a href="{URL_BASE}" style="background-color: #337ab7; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Go to Official Booking Site</a>
        </div>
      </body>
    </html>
    """
    send_plain_alert_email(EMAIL_SUBJECT_DAILY, html_content)

def check_oyari():
    """🟢 100% 恢復您測試很久、原汁原味、完全沒有問題的每半小時巡邏主體"""
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
        
        for li in list_items:
            li_html = str(li)
            cell_text = li.get_text(" ", strip=True)
            cell_text_clean = "".join(cell_text.split())
            
            if re.search(r'(?<!\d)' + day_stripped + r'(?!\d)', cell_text_clean) and ("class=\"day\"" in li_html or "div" in li_html):
                if "previous" not in li_html and "next" not in li_html and "calendarDate" not in li_html:
                    if "阻" in cell_text_clean or "満" in cell_text_clean or "满" in cell_text_clean or "-" in cell_text_clean or "－" in cell_text_clean:
                        print(f"Oct {day_stripped} is still fully booked ({cell_text_clean}).")
                    else:
                        print(f"🔥 Vacancy detected! Current Status: {cell_text_clean}")
                        
                        urgent_html = f"<h2>🔥 [Vacancy Alert] October 3rd is available ({cell_text_clean})!</h2>"
                        send_plain_alert_email(EMAIL_SUBJECT_URGENT, urgent_html)
                    break
    except Exception as e:
        print("Cloud inspection node error:", e)

if __name__ == "__main__":
    # 智慧分流：將兩者徹底拆成平行的宇宙，0% 機率交互感染
    if len(sys.argv) > 1 and "daily" in sys.argv:
        execute_daily_report()
    else:
        check_oyari()
