import time
import datetime
import smtplib
import socket
import re
import sys
import os # 👈 新增：只用來檢查圖片檔案是否存在
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage # 👈 新增：只用來夾帶圖片，不影響純文字
from bs4 import BeautifulSoup
import requests

# ==================== Cloud Email Configuration ====================
URL_BASE = "https://enzanso-reservation.jp"
TARGET_YEAR_MONTH = "2026年10月"
TARGET_DAY = "3"  # 🎯 Deadlocked on Oct 3rd for your Mt. Yarigatake trek!

# ✉️ Please fill in your traditional email credentials here:
SENDER_EMAIL = "juvenmini@gmail.com"
PASSWORD = "qywcsfzqrpvemoyo"         # 💡 Your 16-letter App Password (e.g. "abcdefghijklmnop")
RECIPIENT_EMAIL = "syht20@gmail.com" # 💡 Your recipient inbox

EMAIL_SUBJECT_URGENT = "🚨<Book now!>ヒュッテ大槍 Oct 3 has become available"
# 🎯 Daily 標題已依您的要求精準修改為：
EMAIL_SUBJECT_DAILY = "⛰️ ヒュッテ大槍 Oct 2026 daily availability report"
# ===================================================================

def send_alert_email(current_status_text, is_daily_report=False):
    """Sends custom notification layout based on mode (Python 3.12 compatible)"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    
    if is_daily_report:
        msg['Subject'] = EMAIL_SUBJECT_DAILY
        # 📊 Daily visual report content layout
        # 💡 唯一改動：在文字下方留一個位置給圖片 (如果截圖成功就會顯示)
        html_content = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h3>📢 This is the daily snapshot of Hut Oyari Calendar ({TARGET_YEAR_MONTH}):</h3>
            <p>Current Raw Code Text of October {TARGET_DAY}rd: <span style="background-color: #777; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: white;">{current_status_text}</span></p>
            <p>If you see '◯', '▲', or any single-digit number instead of '満', please click below to book immediately!</p>
            <br>
            <p><b>📸 Below is the live calendar screenshot:</b></p>
            <img src="cid:calendar_image" alt="[Calendar Image]" style="max-width: 100%; border: 1px solid #ccc;">
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
    else:
        msg['Subject'] = EMAIL_SUBJECT_URGENT
        # 🔥 Urgent vacancy trigger warning layout
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
              <a href="{URL_BASE}" style="background-color: #5cb85c; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Book Now</a>
            </div>
          </body>
        </html>
        """
        
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    # 🛠️ 【外掛防禦機制】：如果是 daily 且有圖片檔案才夾帶，就算失敗也完全不影響原本信件寄出！
    if is_daily_report and os.path.exists("screenshot.png"):
        try:
            with open("screenshot.png", "rb") as f:
                image = MIMEImage(f.read())
                image.add_header('Content-ID', '<calendar_image>')
                msg.attach(image)
                print("📎 Screenshot attached safely.")
        except Exception as e:
            print("⚠️ Image attach skipped, but mail will still send:", e)

    # 🔴 您最核心、測試很久的雙保險 SMTP 寄信邏輯，100% 沒動：
    smtp_target = "://gmail.com"  # 修正原本 ://gmail.com 連線小錯，確保穩定
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
            print("✉️ Mail delivered via backup secure channel.")
        except Exception as e2:
            print("❌ Mail failed:", e2)

def check_oyari(mode="check"):
    # 🛠️ 【外掛防禦機制】：只有 daily 模式會在背景嘗試截圖，失敗會印出錯誤，但絕對會繼續往下跑您原本的 requests 流程。
    if mode == "daily":
        try:
            run_playwright_screenshot()
        except Exception as e:
            print("⚠️ Screenshot subsystem bypassed due to error:", e)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": URL_BASE,
        "Origin": "https://enzanso-reservation.jp"
    })
    try:
        session.get(URL_BASE, timeout=15)
        payload = {"p": "30", "y": "2026", "m": "10", "agree": "1"}
        res = session.post("https://enzanso-reservation.jp", data=payload, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
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
                        if "阻" in cell_text_clean or "満" in cell_text_clean or "满" in cell_text_clean or "-" in cell_text_clean or "－" in cell_text_clean:
                            print(f"Oct {day_stripped} is still fully booked ({cell_text_clean}).")
                        else:
                            print(f"🔥 Vacancy detected! Current Status: {cell_text_clean}")
                            send_alert_email(cell_text_clean, is_daily_report=False)
                    break
                    
        if not found_day and mode == "daily":
            send_alert_email("Checked (Data unparsed, please verify link manually)", is_daily_report=True)
            
    except Exception as e:
        print("Cloud inspection node error:", e)

# 🛠️ 【全新外掛函數】：完全獨立在最底下，不干涉上面的任何舊代碼
def run_playwright_screenshot():
    from playwright.sync_api import sync_playwright
    print("📸 [Playwright] Trying to capture calendar snapshot...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL_BASE, timeout=20000)
        page.evaluate("""() => {
            const form = document.createElement('form'); form.method = 'POST'; form.action = 'https://enzanso-reservation.jp';
            const pIn = document.createElement('input'); pIn.type = 'hidden'; pIn.name = 'p'; pIn.value = '30';
            const yIn = document.createElement('input'); yIn.type = 'hidden'; yIn.name = 'y'; yIn.value = '2026';
            const mIn = document.createElement('input'); mIn.type = 'hidden'; mIn.name = 'm'; mIn.value = '10';
            const aIn = document.createElement('input'); aIn.type = 'hidden'; aIn.name = 'agree'; aIn.value = '1';
            form.appendChild(pIn); form.appendChild(yIn); form.appendChild(mIn); form.appendChild(aIn);
            document.body.appendChild(form); form.submit();
        }""")
        page.wait_for_timeout(4000)
        page.screenshot(path="screenshot.png", full_page=True)
        browser.close()
    print("🟢 [Playwright] Snapshot saved to workspace.")

if __name__ == "__main__":
    run_mode = "check"
    if len(sys.argv) > 1:
        run_mode = sys.argv[1]
    check_oyari(mode=run_mode)
