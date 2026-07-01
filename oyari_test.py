import time
import datetime
import smtplib
import socket
import sys
import os 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage # 💡 僅用來讀取實體照片

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
    """📸 智慧動態校正：不論當前是幾月，只要畫面還沒到10月，就動態點擊『次月』直到抵達為止"""
    from playwright.sync_api import sync_playwright
    print("📸 [Playwright] Launching dynamic intelligent human simulation...")
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
            
            print(" -> Loading reservation interface...")
            page.goto(URL_BASE, timeout=30000, wait_until="networkidle")
            time.sleep(2.5)
            
            # 動態智慧導航：自動辨識並點擊，徹底封殺跨月移位地雷
            for attempt in range(1, 7):
                if TARGET_YEAR_MONTH in page.content():
                    print(f"🟢 [SUCCESS] Targeted month reached!")
                    break
                    
                print(" -> Current month is not target. Simulating human mouse click on '次月'...")
                next_month_link = page.get_by_role("link", name="次月")
                if next_month_link.is_visible():
                    next_month_link.hover()
                    time.sleep(0.4)
                    next_month_link.click(no_wait_after=True) # 鎖定防卡死引爆點
                    time.sleep(4.0)
                else:
                    break
            
            time.sleep(2.0)
            # 拍攝實體高畫質照片
            page.screenshot(path="screenshot.png", full_page=False)
            browser.close()
            print("🟢 [Playwright] 10月 physical snapshot saved to storage.")
    except Exception as e:
        print(f"❌ [Playwright Error] Intelligent trajectory broken: {e}")

def execute_daily_report():
    """💡 終極降維大破局：完全拋棄會被 Gmail 阻擋的內嵌標籤，改用 100% 絕對放行的普通檔案附件"""
    print("🚀 [DAILY REPORT NODE] Starting safe sequential mail structure...")
    
    # 執行 Playwright 真人序列點擊截圖
    run_playwright_workflow()
    
    # 💡 核心修正：回歸最相容、全宇宙郵件伺服器最認可的標準混合容器
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = EMAIL_SUBJECT_DAILY
    
    # 💡 核心修正：HTML 內完全不寫 cid 標籤，徹底拔除破圖叉叉，直接提示用戶下載最下方的實體附檔！
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h3>📢 This is the daily snapshot of Hut Oyari Calendar (2026年10月):</h3>
        <p>If you see '◯', '▲', or any single-digit number instead of '満', please click below to book immediately!</p>
        <br>
        <p style="padding: 10px; background-color: #ffffcc; border-left: 4px solid #f0ad4e; font-weight: bold;">
          📎 10月份最新預約日曆實體照片，已作為「常規檔案附件」夾帶於本封郵件最下方，請點擊打開查看！
        </p>
        <br>
        <div style="margin: 20px 0;">
          <a href="https://enzanso-reservation.jp" style="background-color: #337ab7; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Go to Official Booking Site</a>
        </div>
        <br>
        <hr style="border: 0; border-top: 1px solid #eee;">
        <p style="font-size: 12px; color: #777;"><i>(This daily report is sent automatically by GitHub cloud server at 22:00 JST.)</i></p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    # 💡 核心修正：將生成的 10 月照片作為最純粹的實體附加檔案（Attachment）掛在信件最尾巴
    if os.path.exists("screenshot.png"):
        try:
            with open("screenshot.png", "rb") as f:
                attachment = MIMEImage(f.read(), _subtype="png")
                # 設定標準的附件下載標頭
                attachment.add_header('Content-Disposition', 'attachment', filename='oyari_calendar_october.png')
                msg.attach(attachment)
                print("🟢 [MAIL ROUTING] PNG document appended successfully as a standard attachment.")
        except Exception as e:
            print(f"❌ [MAIL ROUTING ERROR] Attachment failed: {e}")
    else:
        print("❌ [MAIL ROUTING ERROR] screenshot.png was missing!")

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
