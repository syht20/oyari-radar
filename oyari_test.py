import time
import datetime
import smtplib
import socket
import sys
import os 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage 

# ==================== Cloud Email Configuration ====================
URL_BASE = "https://enzanso-reservation.jp"
TARGET_YEAR_MONTH = "2026年10月"
TARGET_DAY = "3"  # 🎯 Deadlocked on Oct 3rd for your Mt. Yarigatake trek!

SENDER_EMAIL = "juvenmini@gmail.com"
PASSWORD = "qywcsfzqrpvemoyo"         # 💡 Your 16-letter App Password
RECIPIENT_EMAIL = "syht20@gmail.com" # 💡 Your recipient inbox

EMAIL_SUBJECT_DAILY = "⛰️ ヒュッテ大槍 Oct 2026 daily availability report"
# ===================================================================

def run_playwright_workflow():
    """📸 終極破局：利用真實硬體級鍵盤操作切換月份，徹底繞過 WAF 轉址攔截與異步死鎖"""
    from playwright.sync_api import sync_playwright
    print("📸 [Playwright] Initializing authentic hardware-level keypress simulation...")
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
            
            # Step 1: 突破第一層重導向天險，進入真實預約介面 (預設 7 月)
            print(" -> Loading base reservation interface...")
            page.goto(URL_BASE, timeout=35000, wait_until="networkidle")
            time.sleep(3.0)
            
            # Step 2: 聚焦在月份選單上，用實體鍵盤硬性向下推移 3 個月
            print(" -> Simulating physical keyboard navigation to October...")
            month_dropdown = page.locator("select[name='m']")
            month_dropdown.focus()
            time.sleep(0.5)
            
            # 7月 -> 8月
            page.keyboard.press("ArrowDown")
            time.sleep(0.8)
            # 8月 -> 9月
            page.keyboard.press("ArrowDown")
            time.sleep(0.8)
            # 9月 -> 10月
            page.keyboard.press("ArrowDown")
            time.sleep(1.0)
            
            # 按下 Enter 鎖定選單並觸發原生的 AJAX 局部切換
            page.keyboard.press("Enter")
            
            # Step 3: 💡 降維核心：完全不執行任何 click() 點擊或元素偵測，防範 Playwright 原地死等。
            # 直接讓網頁在原地定格、睡足 7.5 秒！給予雲端 Linux 最完美的 AJAX 局部表格渲染時差！
            print(" -> Freezing pipeline for 7.5s to let AJAX populate 10月 data...")
            time.sleep(7.5)
            
            # 拍攝實體高畫質 PNG 照片 (不開 full_page，防止 Linux 算錯高度吐出空檔)
            page.screenshot(path="screenshot.png", full_page=False)
            browser.close()
            print("🟢 [Playwright] October calibrated snapshot captured successfully.")
    except Exception as e:
        print(f"❌ [Playwright Error] Subsystem tracking failed: {e}")

def execute_daily_report():
    """💡 100% 沿用收信成功、最不易被攔截的 Version 1 標準普通檔案附件封包引擎"""
    print("🚀 [DAILY REPORT NODE] Constructing clean mail with calendar attachment...")
    
    # 調用隱形瀏覽器進行實體鍵盤推移截圖
    run_playwright_workflow()
    
    # 建立最乾淨的標準信件主體
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = EMAIL_SUBJECT_DAILY
    
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h3>📢 This is the daily snapshot of Hut Oyari Calendar (2026年10月):</h3>
        <p>If you see '◯', '▲', or any single-digit number instead of '満', please click below to book immediately!</p>
        <br>
        <p style="padding: 10px; background-color: #ffffcc; border-left: 4px solid #f0ad4e; font-weight: bold;">
          📎 10月份最新預約日曆照片，已作為「常規檔案附件」夾帶於本郵件最下方，請點開查看！
        </p>
        <br>
        <div style="margin: 20px 0;">
          <a href="https://enzanso-reservation.jp" style="background-color: #337ab7; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Go to Official Booking Site</a>
        </div>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    # 將生成完好的實體 10 月照片作為常規 Attachment 掛在信件最底下
    if os.path.exists("screenshot.png"):
        try:
            with open("screenshot.png", "rb") as f:
                attachment = MIMEImage(f.read()) # 100% 還原成最初收信成功的安全封包宣告
                attachment.add_header('Content-Disposition', 'attachment', filename='oyari_calendar_october.png')
                msg.attach(attachment)
                print("🟢 [MIME ROUTING] 10月 PNG appended safely as a standard attachment.")
        except Exception as e:
            print(f"❌ [MIME ROUTING ERROR] Attachment binding failed: {e}")
    else:
        print("❌ [MIME ROUTING ERROR] screenshot.png was missing!")

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
            print("✉️ Mail delivered via secure fallback channel.")
        except Exception as e2:
            print("❌ Mail failed:", e2)

if __name__ == "__main__":
    execute_daily_report()
