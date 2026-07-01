import time
import datetime
import smtplib
import socket
import re
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests

# ==================== Cloud Email Configuration ====================
URL_BASE = "https://enzanso-reservation.jp"
# 💡 降維修正：直接對齊診斷出來的實體預約後台接收端點
URL_POST_TARGET = "https://enzanso-reservation.jp"

TARGET_YEAR_MONTH = "2026年10月"
TARGET_DAY = "3"  # 🎯 Deadlocked on Oct 3rd for your Mt. Yarigatake trek!

SENDER_EMAIL = "juvenmini@gmail.com"
PASSWORD = "qywcsfzqrpvemoyo"         # 💡 Your 16-letter App Password
RECIPIENT_EMAIL = "syht20@gmail.com" # 💡 Your recipient inbox

EMAIL_SUBJECT_URGENT = "🚨<Book now!>ヒュッテ大槍 Oct 3 has become available"
EMAIL_SUBJECT_DAILY = "⛰️ ヒュッテ大槍 Oct 2026 daily availability report"
# ===================================================================

def generate_live_calendar_table(soup):
    """💡 降維核心：用純粹的安全 HTML 直接繪製實時日曆，100% 免疫反爬蟲與破圖"""
    try:
        list_items = soup.find_all('li')
        calendar_html = """
        <table style="width: 100%; max-width: 400px; border-collapse: collapse; text-align: center; font-family: sans-serif; margin-top: 15px;">
          <tr style="background-color: #337ab7; color: white; font-weight: bold;">
            <th style="padding: 10px; border: 1px solid #ddd;">日期</th>
            <th style="padding: 10px; border: 1px solid #ddd;">剩餘狀況</th>
          </tr>
        """
        
        row_count = 0
        for li in list_items:
            li_html = str(li)
            text = li.get_text(" ", strip=True)
            text_clean = "".join(text.split())
            
            if ("class=\"day\"" in li_html or "div" in li_html) and "previous" not in li_html and "next" not in li_html and "calendarDate" not in li_html:
                match = re.match(r'(\d+)(.*)', text_clean)
                if match:
                    day_num = match.group(1)
                    status_text = match.group(2) if match.group(2) else "-"
                    
                    bg_color = "#fff"
                    if day_num == TARGET_DAY:
                        bg_color = "#ffffcc; font-weight: bold; border: 2px solid #d9534f;"
                    elif row_count % 2 == 1:
                        bg_color = "#f9f9f9"
                        
                    status_color = "#333"
                    if "阻" in status_text or "満" in status_text or "满" in status_text:
                        status_color = "#999"
                    elif "◯" in status_text or "▲" in status_text or status_text.isdigit():
                        status_color = "#d9534f; font-weight: bold;"
                        
                    calendar_html += f"""
                    <tr style="background-color: {bg_color};">
                      <td style="padding: 8px; border: 1px solid #ddd;">10月 {day_num} 日</td>
                      <td style="padding: 8px; border: 1px solid #ddd; color: {status_color};">{status_text}</td>
                    </tr>
                    """
                    row_count += 1
                    
        calendar_html += "</table>"
        if row_count > 0:
            return calendar_html
        return "<p style='color: #777;'><i>(未能成功解析日曆數據，請點擊下方按鈕至官網確認)</i></p>"
    except Exception as e:
        return f"<p style='color: red;'>日曆排版發生異常: {e}</p>"

def send_alert_email(current_status_text, is_daily_report=False, calendar_table_html=""):
    """Sends custom notification layout strictly using Version 1 secure email format"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    
    if is_daily_report:
        msg['Subject'] = EMAIL_SUBJECT_DAILY
        html_content = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h3>📢 This is the daily snapshot of Hut Oyari Calendar ({TARGET_YEAR_MONTH}):</h3>
            <p>Current Raw Code Text of October {TARGET_DAY}rd: <span style="background-color: #777; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: white;">{current_status_text}</span></p>
            <p>If you see '◯', '▲', or any single-digit number instead of '満', please click below to book immediately!</p>
            
            <br>
            <p><b>📊 10月份預約狀態實時回報面板 (100% 數據同步)：</b></p>
            {calendar_table_html}
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
            print("✉️ Mail delivered via backup secure channel.")
        except Exception as e2:
            print("❌ Mail failed:", e2)

def check_oyari(mode="check"):
    session = requests.Session()
    # 💡 降維修正：注入與您 Jupyter 完全對齊的全套真實Headers偽裝
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ja,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
        "Referer": URL_BASE,
        "Origin": URL_BASE
    })
    try:
        # Step 1: 先拜訪首頁，拿 Cookie
        session.get(URL_BASE, timeout=15)
        
        # 💡 核心環境對齊：強制定格睡 3 秒！模擬人類閱讀首頁的正常時差，破除網站對 Session 暴衝的判定
        time.sleep(3.0)
        
        # Step 2: 正式提交 POST 參數給實體後台端點
        payload = {"p": "30", "y": "2026", "m": "10", "agree": "1"}
        res = session.post(URL_POST_TARGET, data=payload, timeout=15)
        
        res.encoding = 'utf-8'
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
                        table_html = generate_live_calendar_table(soup)
                        send_alert_email(cell_text_clean, is_daily_report=True, calendar_table_html=table_html)
                    else:
                        if "阻" in cell_text_clean or "満" in cell_text_clean or "满" in cell_text_clean or "-" in cell_text_clean or "－" in cell_text_clean:
                            print(f"Oct {day_stripped} is still fully booked ({cell_text_clean}).")
                        else:
                            print(f"🔥 Vacancy detected! Current Status: {cell_text_clean}")
                            send_alert_email(cell_text_clean, is_daily_report=False)
                    break
                    
        if not found_day and mode == "daily":
            # 💡 如果真的沒抓到，自動抓取當前網頁片段呈現在信中，不留大灰底
            error_preview = res.text[:300].replace('<', '&lt;').replace('>', '&gt;')
            fallback_html = f"<div style='background:#f4f4f4;padding:10px;'><b>[System Log]</b>: <pre>{error_preview}</pre></div>"
            table_html = generate_live_calendar_table(soup)
            send_alert_email("Checked (Data unparsed)", is_daily_report=True, calendar_table_html=table_html + fallback_html)
