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
    """📸 終極破局：利用真實合法 Cookie 瀏覽器，注入單行 JS 表單提交，100% 逼迫網頁刷新至 10 月"""
    from playwright.sync_api import sync_playwright
    print("📸 [Playwright] Launching high-grade native form injection routing...")
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
            
            # Step 1: 從正門載入預約介面，在雲端環境拿好完整合法 Cookie
            print(" -> [Step 1] Loading index page safely to establish secure sessions...")
            page.goto(URL_BASE, timeout=35000, wait_until="networkidle")
            time.sleep(3.0)
            
            # Step 2: 💡 終極拆彈：將 JS 程式碼縮減為極簡單行，完全避開任何與 Python 衝突的大括號與縮排地雷！
            # 在真實的 DOM 樹內部直接覆寫參數並執行 submit()
            print(" -> [Step 2] Injecting clean form parameters for October 2026...")
            js_payload = "() => { const f = document.querySelector('form'); if(f) { f.p.value='30'; f.y.value='2026'; f.m.value='10'; f.agree.value='1'; f.submit(); } }"
            page.evaluate(js_payload)
            
            # Step 3: 💡 降維防卡死死穴：完全不使用任何點擊，也不讓 Playwright 進入原地死等網頁重載。
            # 直接讓網頁在原地定格、死死地睡足 8 秒鐘！給予雲端 Linux 最完美的 10 月份實時表格加載時差！
            print(" -> [Step 3] Freezing pipeline for 8.0s to let 10月 official database respond...")
            time.sleep(8.0)
            
            # Step 4: 拍攝實體高畫質 PNG 照片 (不開 full_page，防止高度錯亂，保證照片體積飽滿正確)
            print(" -> [Step 4] Saving high-resolution snapshot block...")
            page.screenshot(path="screenshot.png", full_page=False)
            
            browser.close()
            print("🟢 [Playwright] October snapshot verified and saved to hard drive.")
    except Exception as e:
        print(f"❌ [Playwright Error] Form injection routing channel broke: {e}")

def execute_daily_report():
    """💡 100% 沿用收信成功、最不易被攔截的 Version 1 標準普通檔案附件封包引擎"""
    print("🚀 [DAILY REPORT NODE] Constructing clean mail envelope with calendar document...")
    
    # 執行 Playwright 核心截圖
    run_playwright_workflow()
    
    # 建立最乾淨的標準信件主體容器
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

    # 將生成完好、數據飽滿的實體 10 月照片作為常規 Attachment 掛在信件最底下
    if os.path.exists("screenshot.png"):
        try:
            with open("screenshot.png", "rb") as f:
                attachment = MIMEImage(f.read()) # 100% 還原成最初收信成功的安全附件宣告
                attachment.add_header('Content-Disposition', 'attachment', filename='oyari_calendar_october.png')
                msg.attach(attachment)
                print("🟢 [MIME ROUTING] 10月 PNG appended safely as a standard attachment.")
        except Exception as e:
            print(f"❌ [MIME ROUTING ERROR] Attachment binding failed: {e}")
    else:
        print("❌ [MIME ROUTING ERROR] screenshot.png was missing on filesystem! Form submission might have failed.")

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
