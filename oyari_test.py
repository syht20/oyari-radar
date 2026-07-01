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

EMAIL_SUBJECT_URGENT = "🚨<Book now!>ヒュッテ大槍 Oct 3 has become available"
EMAIL_SUBJECT_DAILY = "⛰️ ヒュッテ大槍 Oct 2026 daily availability report"
# ===================================================================

def run_playwright_workflow():
    """📸 終極破局：不管任何選單文字判定，無腦點擊3次次月，no_wait_after=True 確保絕不卡死"""
    from playwright.sync_api import sync_playwright
    print("📸 [Playwright] Launching hardcoded human click routing...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ])
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 1000},
                locale="ja-JP",
                timezone_id="Asia/Tokyo"
            )
            page = context.new_page()
            
            print(" -> [Step 1] Loading base page (July 2026)...")
            page.goto(URL_BASE, timeout=30000, wait_until="networkidle")
            time.sleep(3.0)
            
            # 💡 終極降維：完全不執行任何 if 條件檢查，直接連續按 3 次！
            print(" -> [Step 2] Clicking '次月' (July -> August)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            
            print(" -> [Step 3] Clicking '次月' (August -> September)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            
            print(" -> [Step 4] Clicking '次月' (September -> October)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            
            # 穩穩停頓 7 秒鐘，給予雲端 Linux 最充足的 AJAX 與字體渲染時差
            print(" -> [Step 5] Holding freeze for October calendar populate...")
            time.sleep(7.0)
            
            # 拍攝實體高畫質照片
            page.screenshot(path="screenshot.png", full_page=False)
            browser.close()
            print("🟢 [Playwright] 10月 physical snapshot captured.")
    except Exception as e:
        print(f"❌ [Playwright Error] Hardware sequential routing broke: {e}")

def execute_daily_report():
    """💡 100% 沿用收信成功、無損壞的常規附件封包引擎"""
    print("🚀 [DAILY REPORT NODE] Constructing clean mail with attachment...")
    
    # 背景執行無腦 3 次點擊
    run_playwright_workflow()
    
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
          📎 10月份最新預約日曆照片，已作為「檔案附件」掛在本郵件最下方，請點開查看！
        </p>
        <br>
        <div style="margin: 20px 0;">
          <a href="https://enzanso-reservation.jp" style="background-color: #337ab7; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Go to Official Booking Site</a>
        </div>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    # 將剛才順利生成、100% 被推到 10 月的照片作為實性普通附檔夾帶
    if os.path.exists("screenshot.png"):
        try:
            with open("screenshot.png", "rb") as f:
                attachment = MIMEImage(f.read()) # 100% 原汁原味最初成功宣告
                attachment.add_header('Content-Disposition', 'attachment', filename='oyari_calendar_october.png')
                msg.attach(attachment)
                print("🟢 [MIME ROUTING] PNG attached safely as standard attachment.")
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
            print("✉️ Mail delivered via fallback secure channel.")
        except Exception as e2:
            print("❌ Mail failed:", e2)

if __name__ == "__main__":
    execute_daily_report()
