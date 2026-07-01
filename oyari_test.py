import time
import datetime
import smtplib
import socket
import sys
import os 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage 
from email import encoders # 💡 核心安全：引入強制的 Base64 編碼器，保證圖片流在傳輸時不破損

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
    """📸 終極破局：真人模擬連續點擊，並採用固定的 Viewport 視窗抓拍，徹底封殺空殼破圖"""
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
                viewport={"width": 1280, "height": 1000}, # 鎖定高畫質黃金視窗
                locale="ja-JP",
                timezone_id="Asia/Tokyo"
            )
            page = context.new_page()
            
            print(" -> Loading reservation page (Default: July)...")
            page.goto(URL_BASE, timeout=30000, wait_until="networkidle")
            time.sleep(2.5)
            
            # 點擊切換月份 (no_wait_after=True 拆除超時地雷)
            print(" -> Clicking '次月' (July -> August)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            
            print(" -> Clicking '次月' (August -> September)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            
            print(" -> Clicking '次月' (September -> October)...")
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            
            # 穩穩給予 6.5 秒，讓 10 月份實時表格與燕山莊綠色外殼樣式完全渲染歸位
            print(" -> Stabilization freeze for October calendar layout...")
            time.sleep(6.5)
            
            # 💡 終極修正：徹底拋棄 full_page=True（防止 Linux 算錯高度吐出空檔），直接進行實體視窗截圖！
            print(" -> Capturing physical viewport image block...")
            page.screenshot(path="screenshot.png", full_page=False)
            
            browser.close()
            print("🟢 [Playwright] Calibrated 10月 physical snapshot successfully captured.")
    except Exception as e:
        print(f"❌ [Playwright Error] Hardware capture failed: {e}")

def execute_daily_report():
    """💡 100% 沿用並固化您最初成功收到 7 月信件時的相容性寄信結構"""
    print("🚀 [DAILY REPORT NODE] Starting secure 图文信件封包...")
    
    # 執行真人點擊與視窗截圖
    run_playwright_workflow()
    
    # 💡 遵循 RFC 國際標準：多圖文內嵌主要容器採用 alternative
    msg = MIMEMultipart('alternative')
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
    
    # 建立內嵌 nested 容器
    msg_related = MIMEMultipart('related')
    msg_related.attach(MIMEText(html_content, 'html', 'utf-8'))

    # 將剛才順利生成、100% 飽滿的實體 10 月照片內嵌進信裡
    if os.path.exists("screenshot.png"):
        try:
            with open("screenshot.png", "rb") as f:
                # 💡 強制注入 Base64 編碼標頭，擊碎所有信箱的破圖過濾機制！
                image = MIMEImage(f.read(), _subtype="png")
                encoders.encode_base64(image)
                image.add_header('Content-ID', '<calendar_image>') # 帶上標準角括號
                image.add_header('Content-Disposition', 'inline', filename='screenshot.png')
                msg_related.attach(image)
                print("🟢 [MIME PROCESS] Base64 Image nested safely with bracketed Content-ID.")
        except Exception as e:
            print("⚠️ Image attach skipped:", e)
    else:
        print("❌ [MIME ERROR] screenshot.png was not generated!")

    msg.attach(msg_related)

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
    execute_daily_report()
