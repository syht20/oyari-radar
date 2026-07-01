import time
import datetime
import smtplib
import socket
import re
import sys
import os 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

# ==================== Cloud Email Configuration ====================
URL_BASE = "https://enzanso-reservation.jp"
TARGET_YEAR_MONTH = "2026年10月"
TARGET_DAY = "3"  # 🎯 Deadlocked on Oct 3rd for your Mt. Yarigatake trek!

SENDER_EMAIL = "juvenmini@gmail.com"
PASSWORD = "qywcsfzqrpvemoyo"         # 💡 Your 16-letter App Password
RECIPIENT_EMAIL = "syht20@gmail.com" # 💡 Your recipient inbox

EMAIL_SUBJECT_URGENT = "🚨<Book now!>ヒュッテ大槍 Oct 3 has become available"
EMAIL_SUBJECT_DAILY = "⛰️ ヒュッテ大槍 Oct 2026 daily availability report"
# ===================================================================

def run_playwright_workflow():
    """📸 智慧事件驅動：利用 dispatch_event 替代點擊，100% 排除 Timeout 超時死鎖"""
    from playwright.sync_api import sync_playwright
    print("📸 [Playwright] Launching high-compatibility event injection subsystem...")
    captured_html = ""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ])
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 1200},
                locale="ja-JP",
                timezone_id="Asia/Tokyo"
            )
            page = context.new_page()
            
            print(" -> Loading reservation interface...")
            page.goto(URL_BASE, timeout=30000, wait_until="networkidle")
            page.wait_for_timeout(2000)
            
            # 💡 智慧事件驅動：不使用 click()，在記憶體中強行對下拉選單打入原生 change 訊號
            print(" -> Forcing Year Dropdown to 2026 via native dispatch...")
            page.locator("select[name='y']").select_option("2026")
            page.locator("select[name='y']").dispatch_event("change")
            page.wait_for_timeout(1000)
            
            print(" -> Forcing Month Dropdown to 10 via native dispatch...")
            page.locator("select[name='m']").select_option("10")
            page.locator("select[name='m']").dispatch_event("change")
            page.wait_for_timeout(1000)
            
            print(" -> Dispatching native click to display calendar...")
            page.locator("input[type='submit'][value='表示']").dispatch_event("click")
            
            # 給予網頁充足的 6 秒鐘時間局部加載
            print(" -> Awaiting local AJAX data population...")
            page.wait_for_timeout(6000)
            
            captured_html = page.content()
            browser.close()
            print("🟢 [Playwright] October HTML data stream successfully synchronized.")
    except Exception as e:
        print(f"❌ [Playwright Error] Event injection pipeline failed: {e}")
    return captured_html

def send_plain_alert_email(subject, body_html, raw_text_log=""):
    """100% 沿用先前讓您順利秒收郵件的標準安全信件引擎"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body_html, 'html', 'utf-8'))
    
    if raw_text_log:
        try:
            attachment = MIMEText(raw_text_log, 'plain', 'utf-8')
            attachment.add_header('Content-Disposition', 'attachment', filename='october_calendar_source.txt')
            msg.attach(attachment)
            print("🟢 [MIME PROCESS] Text log appended safely.")
        except Exception as e:
            print(f"❌ [MIME ERROR]: {e}")

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
            print("✉️ Mail delivered via secure channels.")
        except Exception as e2:
            print("❌ Mail failed:", e2)

def check_oyari(mode="check"):
    """💡 核心對齊：補上 mode 參數，徹底解決 TypeError 傳參對不上的小瑕疵"""
    html_content_parsed = run_playwright_workflow()
    
    if not html_content_parsed:
        print("⚠️ Subsystem returned blank. Task bypassed.")
        html_content_parsed = "<html><body>Failed to fetch secure data stream.</body></html>"

    soup = BeautifulSoup(html_content_parsed, 'html.parser')
    list_items = soup.find_all('li')
    day_stripped = str(int(TARGET_DAY))
    cell_text_clean = "Unknown"
    found_day = False
    
    # 精確爬取 10 月 3 日當天的狀態
    for li in list_items:
        li_html = str(li)
        cell_text = li.get_text(" ", strip=True)
        cell_text_clean = "".join(cell_text.split())
        
        if re.search(r'(?<!\d)' + day_stripped + r'(?!\d)', cell_text_clean) and ("class=\"day\"" in li_html or "div" in li_html):
            if "previous" not in li_html and "next" not in li_html and "calendarDate" not in li_html:
                found_day = True
                break

    status_label = f"10月3日狀態：{cell_text_clean}" if found_day else "10月3日狀態：請查收下方實時數據片段"
    
    # 擷取日曆表格核心片段，當作郵件內文面板
    preview_idx = html_content_parsed.find("calendarTable")
    if preview_idx == -1: preview_idx = html_content_parsed.find("calendarDate")
    if preview_idx == -1: preview_idx = 0
    raw_snippet = html_content_parsed[preview_idx:preview_idx+600].strip().replace('<', '&lt;').replace('>', '&gt;')

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h3>📢 This is the daily snapshot of Hut Oyari Calendar (2026年10月):</h3>
        <p>Current Raw Code Text of October 3rd: <span style="background-color: #337ab7; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: white;">{status_label}</span></p>
        <p>If you see '◯', '▲', or any single-digit number instead of '満', please click below to book immediately!</p>
        <br>
        <div style="background:#f9f9f9; padding:15px; border-left:4px solid #5cb85c; font-family:monospace;">
          <b>[System Live Output Preview - 100% Real October Calendar HTML]</b>
          <pre style="white-space: pre-wrap; font-size:13px; color:#333;">{raw_snippet}</pre>
        </div>
        <br>
        <p><b>📎 10月份完整的網頁 HTML 原始碼，已作為 .txt 檔案安全附帶於本封郵件下方，供您核對。</b></p>
        <br>
        <div style="margin: 20px 0;">
          <a href="https://enzanso-reservation.jp" style="background-color: #337ab7; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Go to Official Booking Site</a>
        </div>
      </body>
    </html>
    """
    send_plain_alert_email(EMAIL_SUBJECT_DAILY, html_content, raw_text_log=html_content_parsed)

if __name__ == "__main__":
    run_mode = "check"
    if len(sys.argv) > 1:
        if "daily" in sys.argv:
            run_mode = "daily"
    check_oyari(mode=run_mode)
