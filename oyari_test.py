import time
import datetime
import smtplib
import socket
import re
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

# ==================== Cloud Email Configuration ====================
URL_BASE = "https://enzanso-reservation.jp"
URL_POST_TARGET = "https://enzanso-reservation.jp"

TARGET_YEAR_MONTH = "2026年10月"
SENDER_EMAIL = "juvenmini@gmail.com"
PASSWORD = "qywcsfzqrpvemoyo"         # 💡 Your 16-letter App Password
RECIPIENT_EMAIL = "syht20@gmail.com" # 💡 Your recipient inbox

EMAIL_SUBJECT_DAILY = "⛰️ ヒュッテ大槍 Oct 2026 daily availability report"
# ===================================================================

def send_plain_alert_email(subject, body_html):
    """最純粹、無任何結構嵌套的標準寄信引擎，100% 綠燈放行"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body_html, 'html', 'utf-8'))
    
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

def extract_day_status(clean_html_text, day_string):
    """核心交叉驗證演算法：精準定位特定日期在 HTML 內部的即時狀態"""
    # 尋找例如 "2日"、"3日"、"6日"
    match = re.search(day_string + r'.*?([◯▲満满\d])', clean_html_text)
    if match:
        status_char = match.group(1)
        if status_char in ["満", "满"]:
            return "滿室 (満)"
        elif status_char in ["◯", "▲"] or status_char.isdigit():
            return f"🔥 有空房 [{status_char}]"
        return f"未知狀態 ({status_char})"
    return "未能在原始碼中定位該日期 (Data unparsed)"

def execute_daily_report():
    """💡 終極降維：利用優化後的 requests 直擊 10 月實體後台，並執行 3 日期交叉驗證"""
    print("🚀 [DAILY ROUTINE] Executing full tracking with 3-day cross verification...")
    session = requests.Session()
    
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ja,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
        "Referer": URL_BASE,
        "Origin": URL_BASE
    })
    
    # 軌跡同步：拜訪首頁並定格睡 3 秒
    session.get(URL_BASE, timeout=15)
    time.sleep(3.0)
    
    # 發送真實表單至 PHP 實體後台端點
    payload = {"p": "30", "y": "2026", "m": "10", "agree": "1"}
    res = session.post(URL_POST_TARGET, data=payload, timeout=15)
    res.encoding = 'utf-8'
    html_source_10 = res.text
    
    # 壓縮並清洗所有字串空格
    clean_text = "".join(html_source_10.split())
    
    # 💡 核心變更：單獨抽離 10/2、10/3、10/6 進行資料交叉比對校正
    status_10_02 = extract_day_status(clean_text, "2日")
    status_10_03 = extract_day_status(clean_text, "3日")
    status_10_06 = extract_day_status(clean_text, "6日")
    
    # 💡 核心變更：將 Preview 預覽範圍擴大至 2500 字元，確保 10 月上旬所有的 HTML 代碼完全外露呈現！
    preview_idx = html_source_10.find("calendarTable")
    if preview_idx == -1: preview_idx = html_source_10.find("calendarDate")
    if preview_idx == -1: preview_idx = 0
    raw_snippet = html_source_10[preview_idx:preview_idx+2500].strip().replace('<', '&lt;').replace('>', '&gt;')

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h3>📢 This is the daily snapshot of Hut Oyari Calendar (2026年10月):</h3>
        
        <!-- 💡 交叉驗證數據看板區 -->
        <div style="background-color: #f7f9fa; padding: 15px; border: 1px solid #d1d5db; border-radius: 6px; margin-bottom: 20px;">
          <h4 style="margin-top: 0; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px;">🎯 10月核心日期巡邏看板 (Testing Cross-Verification)</h4>
          <ul style="list-style: none; padding-left: 0; margin-bottom: 0; font-size: 14px;">
            <li style="padding: 6px 0;">📅 <b>10月2日 (五)</b> 狀態：<span style="color:#4b5563;">{status_10_02}</span></li>
            <li style="padding: 6px 0; background-color: #fffde7; font-weight: bold; border-left: 4px solid #d9534f; padding-left: 8px;">🎯 10月3日 (六) 狀態：<span>{status_10_03}</span></li>
            <li style="padding: 6px 0;">📅 <b>10月6日 (二)</b> 狀態：<span style="color:#4b5563;">{status_10_06}</span></li>
          </ul>
        </div>

        <p>If you see '◯', '▲', or any single-digit number instead of '満', please click below to book immediately!</p>
        <br>
        
        <!-- 核心黑色原始碼面板 (已擴大範圍至 2500 字元) -->
        <div style="background:#222; padding:15px; border-radius:6px; font-family:monospace; box-shadow: inset 0 0 10px #000;">
          <b style="color:#5cb85c;">[💾 Expanded Live Source Code Preview - 100% Real Time Data]</b>
          <pre style="white-space: pre-wrap; font-size:12px; color:#fff; margin-top:10px; line-height:1.4;">{raw_snippet}</pre>
        </div>
        <br>
        <div style="margin: 20px 0;">
          <a href="https://enzanso-reservation.jp?p=30" style="background-color: #337ab7; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Go to Official Booking Site</a>
        </div>
      </body>
    </html>
    """
    send_plain_alert_email(EMAIL_SUBJECT_DAILY, html_content)

if __name__ == "__main__":
    execute_daily_report()
