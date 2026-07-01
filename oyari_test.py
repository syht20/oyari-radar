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
    """📸 真人模擬點擊 3 次次月：帶入 no_wait_after=True 與 Viewport 抓拍，保證生成飽滿 10 月圖片"""
    from playwright.sync_api import sync_playwright
    print("📸 [Playwright] Launching safe sequential tracking sub-routing...")
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
            
            print(" -> Loading reservation page (July)...")
            page.goto(URL_BASE, timeout=30000, wait_until="networkidle")
            time.sleep(2.5)
            
            # 循序點擊 3 次（no_wait_after=True 徹底拔除 Timeout 超時死鎖）
            print(" -> Clicking '次月' (July -> August)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            
            print(" -> Clicking '次月' (August -> September)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            
            print(" -> Clicking '次月' (September -> October)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            
            # 給予極其充裕的 6.5 秒，讓 10 月份數據表格與中文字體完全渲染歸位
            print(" -> Stabilization freeze for October calendar render...")
            time.sleep(6.5)
            
            # 視窗截圖（不使用 full_page，確保 Linux 不會算錯高度）
            page.screenshot(path="screenshot.png", full_page=False)
            browser.close()
            print("🟢 [Playwright] 10月 snapshot saved.")
    except Exception as e:
        print(f"❌ [Playwright Error] Capture failed: {e}")

def execute_daily_report():
    """💡 100% 還原您最一開始成功收到 7 月信件時的相容性寄信結構，不加任何多餘標頭與重複編碼"""
    print("🚀 [DAILY REPORT NODE] Initializing pure Version 1 mail envelope...")
    
    # 後台執行 Playwright 截圖
    run_playwright_workflow()
    
    # 💡 終極修正：100% 還原成您最原始成功的 MIMEMultipart() 結構，一行都不多改！
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
        <p><b>📸 Below is the live calibrated 10月 calendar screenshot from the official server:</b></p>
        <img src="cid:calendar_image" alt="[Calendar Image]" style="max-width: 100%; border: 1px solid #ccc; border-radius: 5px;">
        <br><br>
        <div style="margin: 20px 0;">
          <a href="{URL_BASE}" style="background-color: #337ab7; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Go to Official Booking Site</a>
        </div>
        <br>
        <hr style="border: 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #777;"><i>(This daily report is sent automatically by GitHub cloud server at 22:00 JST.)</i></p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    # 💡 終極修正：原汁原味 Version 1 內嵌法，絕不呼叫 encoders.encode_base64 造成雙重編碼破損！
    if os.path.exists("screenshot.png"):
        try:
            with open("screenshot.png", "rb") as f:
                image = MIMEImage(f.read()) # 100% 重現當初成功的單純宣告
                image.add_header('Content-ID', '<calendar_image>')
                msg.attach(image)
                print("🟢 [MIME PROCESS] Raw image attached via original stable path.")
        except Exception as e:
            print("⚠️ Image attach skipped:", e)
    else:
        print("❌ [MIME ERROR] screenshot.png was missing!")

    # 🔴 您 Version 1 最核心、穩定不變的雙保險 SMTP 寄信邏輯
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
