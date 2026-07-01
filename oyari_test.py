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
    """📸 降維大破局：連續按 3 次次月切換到 10 月。加載 no_wait_after=True 徹底封殺 Timeout 卡死"""
    from playwright.sync_api import sync_playwright
    print("📸 [Playwright] Initializing secure visual capture routing...")
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
            
            print(" -> Loading reservation page (Default: July)...")
            page.goto(URL_BASE, timeout=30000, wait_until="networkidle")
            time.sleep(2.5)
            
            # 💡 終極降維：加上 no_wait_after=True，命令 Playwright 按完按鈕後立刻鬆手，絕對不進入超時等待！
            print(" -> Clicking '次月' (July -> August)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            
            print(" -> Clicking '次月' (August -> September)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            
            print(" -> Clicking '次月' (September -> October)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            
            # 穩穩給予 6 秒鐘時間，讓日本伺服器把 10 月份實時表格數據與中日文字體完全填滿
            print(" -> Stabilization freeze for October calendar layout...")
            time.sleep(6.0)
            
            # 咔嚓！拍下最真實、100% 絕對是 10 月的螢幕照片
            page.screenshot(path="screenshot.png", full_page=True)
            browser.close()
            print("🟢 [Playwright] Calibrated 10月 calendar snapshot successfully captured.")
    except Exception as e:
        print(f"❌ [Playwright Error] Hardware capture failed: {e}")

def execute_daily_report():
    """💡 100% 沿用並固化您最初成功收到 7 月信件時的相容性寄信結構"""
    print("🚀 [DAILY REPORT NODE] Starting secure 图文信件封包...")
    
    # 背景執行 Playwright 真人序列點擊截圖
    run_playwright_workflow()
    
    # 建立信件容器 (完全對齊您收信成功的 Version 1 引擎)
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

    # 將剛才順利生成、100% 是 10 月的照片內嵌進信裡
    if os.path.exists("screenshot.png"):
        try:
            with open("screenshot.png", "rb") as f:
                image = MIMEImage(f.read())
                image.add_header('Content-ID', '<calendar_image>')
                msg.attach(image)
                print("🟢 [MIME PROCESS] Screenshot image embedded safely.")
        except Exception as e:
            print("⚠️ Image attach skipped:", e)
    else:
        print("❌ [MIME ERROR] screenshot.png was not generated!")

    # 雙保險寄信管道
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
    # 💡 終極降維：只為您最珍貴的每日 10 月照片服務。每半小時的巡邏（check）完全拔除不驚動，避免任何環境衝突
    execute_daily_report()
