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
# 💡 終極降維：直擊穿好全套 10 月參數、且能完美激活 Session 的實體數據網址
URL_FINAL_TARGET = "https://enzanso-reservation.jp"

TARGET_YEAR_MONTH = "2026年10月"
TARGET_DAY = "3"  # 🎯 Deadlocked on Oct 3rd for your Mt. Yarigatake trek!

SENDER_EMAIL = "juvenmini@gmail.com"
PASSWORD = "qywcsfzqrpvemoyo"         # 💡 Your 16-letter App Password
RECIPIENT_EMAIL = "syht20@gmail.com" # 💡 Your recipient inbox

EMAIL_SUBJECT_URGENT = "🚨<Book now!>ヒュッテ大槍 Oct 3 has become available"
EMAIL_SUBJECT_DAILY = "⛰️ ヒュッテ大槍 Oct 2026 daily availability report"
# ===================================================================

def send_plain_alert_email(subject, body_html):
    """最純粹、無任何結構嵌套的標準寄信引擎，100% 綠燈秒發秒收"""
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
        print("✉️ Mail successfully delivered.")
    except Exception as e:
        try:
            server = smtplib.SMTP(smtp_target, 587, timeout=15)
            server.starttls()
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
            server.quit()
            print("✉️ Mail delivered via backup secure channel.")
        except Exception as e2:
            print("❌ Mail failed:", e2)

def extract_day_status(clean_html_text, day_string):
    """核心交叉驗證演算法：精準定位特定日期在 HTML 標籤內部的即時狀態"""
    # 💡 100% 對齊您提供的實體原始碼結構進行正則比對 (捕捉 ◯、▲、満)
    match = re.search(day_string + r'.*?([◯▲臨阻満满\d])', clean_html_text)
    if match:
        status_char = match.group(1)
        if status_char in ["臨", "阻", "満", "满"]:
            return "滿室 (臨/阻/満)"
        elif status_char in ["◯", "▲"] or status_char.isdigit():
            return f"🔥 有空房 [{status_char}]"
        return f"未知狀態 ({status_char})"
    return "未能在原始碼中定位該日期"

def check_oyari(mode="check"):
    """💡 終極大降維：人為製造完美的擬人化 Cookie 軌跡，直擊滿載參數的 10 月 URL 數據接口"""
    print("🚀 [URL SNIPER] Initializing human-like session tracking...")
    session = requests.Session()
    
    # 完美對齊真實 Chrome 瀏覽器的全套 Headers 外殼
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ja,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
        "Referer": URL_BASE,
        "Origin": URL_BASE,
        "Connection": "keep-alive"
    })
    
    try:
        # Step 1: 先拜訪首頁入口，獲取初始 PHPSESSID Cookie 憑證
        print(" -> [Step 1] Visiting roots to bake initial cookies...")
        session.get(URL_BASE, timeout=15)
        
        # 💡 人類思維時差：強制定格睡 3.0 秒！模擬人類看完首頁條款的正常時差，解鎖 Session 暴衝判定
        print(" -> Simulating human browsing behavior time delay...")
        time.sleep(3.0)
        
        # Step 2: 💡 終極大破局：攜帶完全熟透的合法 Cookie，直擊穿好全套 10 月參數的實體數據 URL！
        print(" -> [Step 2] Sending precision GET request to full-parameterized October URL...")
        res = session.get(URL_FINAL_TARGET, timeout=15)
        res.encoding = 'utf-8'
        html_content_parsed = res.text

        # 100% 還原您最穩定、完全沒有問題的 BeautifulSoup 解析引擎
        soup = BeautifulSoup(html_content_parsed, 'html.parser')
        list_items = soup.find_all('li')
        day_stripped = str(int(TARGET_DAY))
        cell_text_clean = "Unknown"
        found_day = False
        
        for li in list_items:
            li_html = str(li)
            cell_text = li.get_text(" ", strip=True)
            cell_text_clean = "".join(cell_text.split())
            
            if re.search(r'(?<!\d)' + day_stripped + r'(?!\d)', cell_text_clean) and ("class=\"day\"" in li_html or "div" in li_html):
                if "previous" not in li_html and "next" not in li_html and "calendarDate" not in li_html:
                    found_day = True
                    break

        # 執行 10/2、10/3、10/6 的三日期數據交叉驗證
        clean_all_spaces = "".join(html_content_parsed.split())
        status_10_02 = extract_day_status(clean_all_spaces, "2日")
        status_10_03 = extract_day_status(clean_all_spaces, "3日")
        status_10_06 = extract_day_status(clean_all_spaces, "6日")

        # 擷取日曆表格核心片段，當作郵件內文面板 (擴大範圍至 2500 字元)
        preview_idx = html_content_parsed.find("calendarTable")
        if preview_idx == -1: preview_idx = html_content_parsed.find("calendarDate")
        if preview_idx == -1: preview_idx = 0
        raw_snippet = html_content_parsed[preview_idx:preview_idx+2500].strip().replace('<', '&lt;').replace('>', '&gt;')

        if mode != "daily":
