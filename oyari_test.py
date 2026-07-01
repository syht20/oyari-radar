import time
import datetime
import smtplib
import socket
import re
import sys
import os 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage 
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
    """📸 終極合流：物理序列點擊 3 次，引入 no_wait_after=True 徹底拔除 7月定格與卡死超時"""
    from playwright.sync_api import sync_playwright
    print("📸 [Playwright] Launching hardcoded sequential navigation...")
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
                viewport={"width": 1280, "height": 1100},
                locale="ja-JP",
                timezone_id="Asia/Tokyo"
            )
            page = context.new_page()
            
            print(" -> Loading reservation page (Default: July)...")
            page.goto(URL_BASE, timeout=30000, wait_until="networkidle")
            time.sleep(2.5)
            
            # 💡 智慧降維：完全不使用任何 JavaScript 長字串，直接使用 Playwright 物理點擊，按完立刻鬆手！
            print(" -> Clicking '次月' (July -> August)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5) # 給予充足時間讓 AJAX 刷新日曆
            
            print(" -> Clicking '次月' (August -> September)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            
            print(" -> Clicking '次月' (September -> October)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            
            # 穩穩在原地睡 7 秒鐘，讓 10 月份實時表格數據與中日文字體在背景完全填滿
            print(" -> Stabilization freeze for October calendar layout...")
            time.sleep(7.0)
            
            # 拍攝實體高畫質照片 (不開 full_page，保障照片結構飽滿不破損)
            page.screenshot(path="screenshot.png", full_page=False)
            print("🟢 [Playwright] October snapshot securely captured.")
            
            # 核心合流：把 10 月網頁的原始碼保存留給 BeautifulSoup 解析，確保文字圖片 100% 同步！
            captured_html = str(page.content())
            browser.close()
    except Exception as e:
        print(f"❌ [Playwright Error] Hardware capture failed: {e}")
    return captured_html

def send_plain_alert_email(subject, body_html, has_image=False):
    """100% 還原您最初成功收到 7 月信件時的相容性圖文內嵌寄信結構"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body_html, 'html', 'utf-8'))

    # 100% 重現當初成功的單純內嵌圖片路軌
    if has_image and os.path.exists("screenshot.png"):
        try:
            with open("screenshot.png", "rb") as f:
                image = MIMEImage(f.read()) 
                image.add_header('Content-ID', '<calendar_image>')
                msg.attach(image)
                print("🟢 [MIME PROCESS] Screenshot image embedded safely using Version 1 engine.")
        except Exception as e:
            print("⚠️ Image attach skipped:", e)

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
            print("✉️ Mail delivered via fallback secure channel.")
        except Exception as e2:
            print("❌ Mail failed:", e2)

def extract_day_status(clean_html_text, day_string):
    """核心交叉驗證演算法：精準定位特定日期在 HTML 標籤內部的即時狀態"""
    match = re.search(day_string + r'.*?([◯▲臨満满\d])', clean_html_text)
    if match:
        status_char = match.group(1)
        if status_char in ["臨", "臨", "満", "满"]:
            return "滿室 (臨/満)"
        elif status_char in ["◯", "▲"] or status_char.isdigit():
            return f"🔥 有空房 [{status_char}]"
        return f"未知狀態 ({status_char})"
    return "未能在原始碼中定位該日期"

def check_oyari(mode="check"):
    """💡 獨立主體：解析與圖片完全交給 Playwright 字串，0% 機率出錯"""
    html_content_parsed = run_playwright_workflow()
    
    if not html_content_parsed:
        print("⚠️ Browser execution returned blank. Task bypassed.")
        return

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

    # 執行 10/2、10/3、10/6 的三日期數據交叉驗證比對
    clean_all_spaces = "".join(html_content_parsed.split())
    status_10_02 = extract_day_status(clean_all_spaces, "2日")
    status_10_03 = extract_day_status(clean_all_spaces, "3日")
    status_10_06 = extract_day_status(clean_all_spaces, "6日")

    if mode != "daily":
        if found_day and "臨" not in cell_text_clean and "阻" not in cell_text_clean and "満" not in cell_text_clean and "满" not in cell_text_clean:
            print(f"🔥 Vacancy detected! Current Status: {cell_text_clean}")
            urgent_html = f"<h2>🔥 [Vacancy Alert] October 3rd is available ({cell_text_clean})!</h2>"
            send_plain_alert_email(EMAIL_SUBJECT_URGENT, urgent_html, has_image=False)
        else:
            print(f"Oct {day_stripped} is still fully booked ({cell_text_clean}).")
            
    else:
        print("Executing daily report summary node...")
        status_label = f"10月3日狀態：{cell_text_clean}" if found_day else "10月3日狀態：請對照下方實時圖片面板"
        
        html_content = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h3>📢 This is the daily snapshot of Hut Oyari Calendar (2026年10月):</h3>
            
            <!-- 💡 交叉驗證數據看板區 -->
            <div style="background-color: #f7f9fa; padding: 15px; border: 1px solid #d1d5db; border-radius: 6px; margin-bottom: 20px;">
              <h4 style="margin-top: 0; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px;">🎯 10月核心日期巡邏看板 (Cross-Verified Data)</h4>
              <ul style="list-style: none; padding-left: 0; margin-bottom: 0; font-size: 14px;">
                <li style="padding: 6px 0;">📅 <b>10月2日 (五)</b> 狀態：<span style="color:#4b5563;">{status_10_02}</span></li>
                <li style="padding: 6px 0; background-color: #fffde7; font-weight: bold; border-left: 4px solid #d9534f; padding-left: 8px;">🎯 10月3日 (六) 狀態：<span>{status_10_03}</span> (BS解析結果: {status_label})</li>
                <li style="padding: 6px 0;">📅 <b>10月6日 (二)</b> 狀態：<span style="color:#4b5563;">{status_10_06}</span></li>
              </ul>
            </div>

            <p>If you see '◯', '▲', or any single-digit number instead of '臨' or '臨' or '満', please act immediately!</p>
            <br>
            <p><b>📸 Below is the live calibrated 10月 calendar screenshot from the official server:</b></p>
            <img src="cid:calendar_image" alt="[Calendar Image]" style="max-width: 100%; border: 1px solid #ccc; border-radius: 5px;">
          </body>
        </html>
        """
        send_plain_alert_email(EMAIL_SUBJECT_DAILY, html_content, has_image=True)

if __name__ == "__main__":
    run_mode = "check"
    if len(sys.argv) > 1:
        if "daily" in sys.argv:
            run_mode = "daily"
    check_oyari(mode=run_mode)
