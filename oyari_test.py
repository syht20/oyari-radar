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

def run_playwright_workflow():
    """📸 100% 還原最初成功路軌：規規矩矩點擊 3 次次月，完全不使用可能導致 Timeout 卡死的元素偵測"""
    from playwright.sync_api import sync_playwright
    print("📸 [Playwright] Launching standard sequential navigation...")
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
            
            print(" -> [Step 1] Loading base page...")
            page.goto("https://enzanso-reservation.jp?p=30", timeout=30000, wait_until="networkidle")
            time.sleep(3.0)
            
            # 💡 終極修正：直接使用最原始、100% 絕不超時卡死的循序點擊，每按一次都穩穩等 4 秒
            print(" -> [Step 2] Clicking '次月' 1st time (Moving to August)...")
            page.get_by_role("link", name="次月").click()
            time.sleep(4.0)
            
            print(" -> [Step 3] Clicking '次月' 2nd time (Moving to September)...")
            page.get_by_role("link", name="次月").click()
            time.sleep(4.0)
            
            print(" -> [Step 4] Clicking '次月' 3rd time (Moving to October)...")
            page.get_by_role("link", name="次月").click()
            time.sleep(5.0)
            
            # 強行打包 10 月份真實的 HTML 內容帶走
            captured_html = page.content()
            browser.close()
            print("🟢 [Playwright] 10月 HTML content retrieved safely.")
    except Exception as e:
        print(f"❌ [Playwright Error] Sequential tracking failed: {e}")
    return captured_html

def send_plain_alert_email(subject, body_html, raw_text_log=""):
    """100% 沿用先前順利收到信件的純文字/HTML通用信件引擎"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body_html, 'html', 'utf-8'))
    
    # 💡 終極安全防禦：把真實抓到的 10 月 HTML 當作常規 .txt 附檔夾帶，全宇宙伺服器皆綠燈放行，100% 不吃信、不破圖
    if raw_text_log:
        try:
            attachment = MIMEText(raw_text_log, 'plain', 'utf-8')
            attachment.add_header('Content-Disposition', 'attachment', filename='october_calendar_source.txt')
            msg.attach(attachment)
            print("🟢 [MIME SUB-ROUTING] Raw HTML appended as standard txt attachment.")
        except Exception as e:
            print(f"❌ [MIME ATTACH ERROR]: {e}")

    smtp_target = "://gmail.com"
    try: socket.gethostbyname(smtp_target)
    except socket.gaierror: smtp_target = "64.233.189.108"
    
    try:
        server = smtplib.SMTP_SSL(smtp_target, 465, timeout=15)
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("✉️ Mail successfully delivered to recipient inbox.")
    except Exception as e:
        try:
            server = smtplib.SMTP(smtp_target, 587, timeout=15)
            server.starttls()
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
            server.quit()
            print("✉️ Mail delivered via fallback secure channel.")
        except Exception as e2:
            print("❌ Mail failed:", e2)

def execute_daily_report():
    """💡 獨立每日報告功能：讓 Playwright 循序點擊拿到 10 月網頁源碼，再交給 BeautifulSoup 解析寄出"""
    html_content_parsed = run_playwright_workflow()
    
    # 萬一瀏覽器真的不幸發生意外，給予基本的降維防禦，確保信件一定會發出
    if not html_content_parsed:
        print("⚠️ Browser execution failed. Falling back to generic notification.")
        html_content_parsed = "<html><body>Browser timeout. Please check manually.</body></html>"

    soup = BeautifulSoup(html_content_parsed, 'html.parser')
    list_items = soup.find_all('li')
    day_stripped = str(int(TARGET_DAY))
    cell_text_clean = "Unknown"
    found_day = False
    
    # 爬取 10 月 3 日當天的狀態
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
          <a href="https://enzanso-reservation.jp?p=30" style="background-color: #337ab7; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Go to Official Booking Site</a>
        </div>
      </body>
    </html>
    """
    # 寄出信件並夾帶真實的 HTML 源碼檔案
    send_plain_alert_email(EMAIL_SUBJECT_DAILY, html_content, raw_text_log=html_content_parsed)

def check_oyari():
    """🟢 100% 保障每半小時巡邏主體穩定運行，requests 在背景輕量化默默監視"""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://enzanso-reservation.jp",
        "Origin": "https://enzanso-reservation.jp"
    })
    try:
        session.get("https://enzanso-reservation.jp", timeout=15)
        payload = {"p": "30", "y": "2026", "m": "10", "agree": "1"}
        res = session.post("https://enzanso-reservation.jp", data=payload, timeout=15)
        res.encoding = 'utf-8'
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
    if len(sys.argv) > 1 and "daily" in sys.argv:
        execute_daily_report()
    else:
        check_oyari()
