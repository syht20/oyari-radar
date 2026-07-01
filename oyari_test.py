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
from email import encoders 
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
    """📸 智慧動態校正：不論當前是幾月，只要畫面還沒到10月，就動態點擊『次月』直到抵達為止"""
    from playwright.sync_api import sync_playwright
    print("📸 [Playwright] Launching dynamic intelligent human simulation...")
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
            
            # 動態智慧導航：最大嘗試點擊 6 次，徹底封殺跨月移位地雷
            for attempt in range(1, 7):
                current_page_text = page.content()
                
                # 檢查網頁當前是否已經顯示了目標的 "2026年10月"
                if TARGET_YEAR_MONTH in current_page_text:
                    print(f"🟢 [SUCCESS] Targeted month reached at step {attempt}!")
                    break
                    
                print(" -> Current month is not target. Simulating human mouse click on '次月'...")
                next_month_link = page.get_by_role("link", name="次月")
                if next_month_link.is_visible():
                    next_month_link.hover()
                    page.wait_for_timeout(400)
                    next_month_link.click()
                    # 穩穩等待 4 秒鐘讓網頁局部加載完畢，防範系統判定為暴衝腳本
                    page.wait_for_timeout(4000)
                else:
                    print("⚠️ '次月' link is missing on this page view.")
                    break
            
            # 到達 10 月後，多留 2 秒鐘讓樣式檔完全歸位，然後拍照
            page.wait_for_timeout(2000)
            page.screenshot(path="screenshot.png", full_page=True)
            print("🟢 [Playwright] Secure calibrated 10月 snapshot saved.")
            
            captured_html = page.content()
            browser.close()
    except Exception as e:
        print(f"❌ [Playwright Error] Intelligent trajectory broken: {e}")
    return captured_html

def send_alert_email(current_status_text, is_daily_report=False):
    """Sends custom notification layout strictly compliant with RFC 2387 Email Protocols"""
    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    
    if is_daily_report:
        msg['Subject'] = EMAIL_SUBJECT_DAILY
        text_content = f"Hut Oyari Daily Snapshot. Current Status of Oct {TARGET_DAY}rd is: {current_status_text}."
        
        html_content = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h3>📢 This is the daily snapshot of Hut Oyari Calendar ({TARGET_YEAR_MONTH}):</h3>
            <p>Current Raw Code Text of October {TARGET_DAY}rd: <span style="background-color: #777; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: white;">{current_status_text}</span></p>
            <p>If you see '◯', '▲', or any single-digit number instead of '満', please click below to book immediately!</p>
            <br>
            <p><b>📸 Below is the live calendar screenshot from the official server:</b></p>
            <img src="cid:calendar_image" alt="[Calendar Image]" style="max-width: 100%; border: 1px solid #ccc; border-radius: 5px;">
            <br><br>
            <div style="margin: 20px 0;">
              <a href="https://enzanso-reservation.jp" style="background-color: #337ab7; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Go to Official Booking Site</a>
            </div>
            <br>
            <hr style="border: 0; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #777;"><i>(This daily report is sent automatically by GitHub cloud server at 22:00 JST.)</i></p>
          </body>
        </html>
        """
        
        msg_related = MIMEMultipart('related')
        msg_related.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        if os.path.exists("screenshot.png"):
            try:
                with open("screenshot.png", "rb") as f:
                    image = MIMEImage(f.read(), _subtype="png")
                    encoders.encode_base64(image)
                    image.add_header('Content-ID', '<calendar_image>') 
                    image.add_header('Content-Disposition', 'inline', filename='screenshot.png')
                    msg_related.attach(image)
                    print("🟢 [MIME PROCESS] Base64 Image nested safely.")
            except Exception as e:
                print(f"❌ [MIME ERROR] Image attachment encoding failed: {e}")
        else:
            print("❌ [MIME ERROR] screenshot.png was missing during envelope assembly!")
            
        msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
        msg.attach(msg_related)
        
    else:
        msg['Subject'] = EMAIL_SUBJECT_URGENT
        html_content = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #d9534f;">🔥 [Hut Oyari] Vacancy Alert for October 3rd!</h2>
            <p>Dear Climber,</p>
            <p>Our cloud monitoring system has successfully detected a vacancy. <b>October 3rd</b> is no longer fully booked!</p>
            <p>Current Status: <span style="background-color: #f0ad4e; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: white;">{current_status_text}</span></p>
            <p>A cancellation has just been released. Please act immediately!</p>
            <br>
            <div style="margin: 20px 0;">
              <a href="https://enzanso-reservation.jp" style="background-color: #5cb85c; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Book Now</a>
            </div>
          </body>
        </html>
        """
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    smtp_target = "://gmail.com"
    try:
        socket.gethostbyname(smtp_target)
    except socket.gaierror:
        smtp_target = "64.233.189.108"

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
            print("✉️ Mail delivered via backup secure channel.")
        except Exception as e2:
            print("❌ Mail failed:", e2)

def check_oyari(mode="check"):
    """💡 獨立函數：只負責純網頁數據解析，與 Playwright 徹底隔開"""
    html_content_parsed = run_playwright_workflow()
    
    if not html_content_parsed:
        print("⚠️ Calibrated browser returned blank. Protection triggered.")
        return

    try:
        soup = BeautifulSoup(html_content_parsed, 'html.parser')
        list_items = soup.find_all('li')
        day_stripped = str(int(TARGET_DAY))
        found_day = False
        cell_text_clean = "Unknown"
        
        for li in list_items:
            li_html = str(li)
            cell_text = li.get_text(" ", strip=True)
            cell_text_clean = "".join(cell_text.split())
            
            if re.search(r'(?<!\d)' + day_stripped + r'(?!\d)', cell_text_clean) and ("class=\"day\"" in li_html or "div" in li_html):
                if "previous" not in li_html and "next" not in li_html and "calendarDate" not in li_html:
                    found_day = True
                    
                    if mode == "daily":
                        print(f"Executing daily summary check. Status: {cell_text_clean}")
                        send_alert_email(cell_text_clean, is_daily_report=True)
                    else:
                        if "阻" in cell_text_clean or "満" in cell_text_clean or "满足" in cell_text_clean or "-" in cell_text_clean or "－" in cell_text_clean:
                            print(f"Oct {day_stripped} is still fully booked ({cell_text_clean}).")
                        else:
                            print(f"🔥 Vacancy detected! Current Status: {cell_text_clean}")
                            send_alert_email(cell_text_clean, is_daily_report=False)
                    # 💡 終極修正：將 break 準確縮排進 if 肚子裡，徹底拔除全劇編譯地雷！

                    

                    
