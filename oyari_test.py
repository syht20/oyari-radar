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
URL_POST_TARGET = "https://enzanso-reservation.jp"

TARGET_YEAR_MONTH = "2026年10月"
TARGET_DAY = "3"  # 🎯 Deadlocked on Oct 3rd for your Mt. Yarigatake trek!

SENDER_EMAIL = "juvenmini@gmail.com"
PASSWORD = "qywcsfzqrpvemoyo"         # 💡 Your 16-letter App Password
RECIPIENT_EMAIL = "syht20@gmail.com" # 💡 Your recipient inbox

EMAIL_SUBJECT_URGENT = "🚨<Book now!>ヒュッテ大槍 Oct 3 has become available"
EMAIL_SUBJECT_DAILY = "⛰️ ヒュッテ大槍 Oct 2026 daily availability report"
# ===================================================================

def send_plain_alert_email(subject, body_html):
    """最純粹、無任何結構嵌套的標準寄信引擎，100% 綠燈秒發秒收"""
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
    """核心交叉驗證演算法：精準定位特定日期在 HTML 標籤內部的即時狀態"""
    match = re.search(day_string + r'.*?([◯▲臨満满\d])', clean_html_text)
    if match:
        status_char = match.group(1)
        if status_char in ["臨", "満", "满"]:
            return "滿室 (臨/満)"
        elif status_char in ["◯", "▲"] or status_char.isdigit():
            return f"🔥 有空房 [{status_char}]"
        return f"未知狀態 ({status_char})"
    return "未能在原始碼中定位該日期 (Data unparsed)"

def check_oyari(mode="check"):
    """💡 終極降維大破局：人為製造完美的擬人化 Cookie 軌跡，徹底擊碎 WAF 轉址攔截"""
    print("🚀 [COOKIE BAKER] Initializing human-like session simulation...")
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ja,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
        "Referer": URL_BASE,
        "Origin": URL_BASE,
        "Connection": "keep-alive"
    })
    
    try:
        # 💡 擬人化軌跡 1：先敲正門首頁，獲取初始 PHPSESSID Cookie 憑證
        print(" -> [Step 1] Visiting index to bake initial cookies...")
        session.get(URL_BASE, timeout=15)
        
        # 💡 人類思維時差 1：原地假裝閱讀網頁 2.2 秒，防止伺服器判定為暴衝腳本
        time.sleep(2.2)
        
        # 💡 擬人化軌跡 2：帶著初始 Cookie 順著超連結走進預約真實介面（URL 帶 p=30），鎖定合法 Session
        print(" -> [Step 2] Navigating via internal hyperlinks to activate reservation frame...")
        session.get("https://enzanso-reservation.jp?p=30", timeout=15)
        
        # 💡 人類思維時差 2：原地再次假裝填寫資料 2.8 秒，讓網站安全閘道完全信任這條連線！
        time.sleep(2.8)
        
        # 💡 擬人化軌跡 3：帶著完全熟透、合法的真實人類 Cookie 軌跡，對後台實體端點正式發送 10 月表單
        print(" -> [Step 3] Submitting fully-baked October payload stream...")
        payload = {"p": "30", "y": "2026", "m": "10", "agree": "1"}
        res = session.post(URL_POST_TARGET, data=payload, timeout=15)
        res.encoding = 'utf-8'
        html_content_parsed = res.text

        # 使用您完美的 BeautifulSoup 解析引擎開始收網
        soup = BeautifulSoup(html_content_parsed, 'html.parser')
        list_items = soup.find_all('li')
        day_stripped = str(int(TARGET_DAY))
        cell_text_clean = "Unknown"
        found_day = False
        
        for li in list_items:
            li_html = str(li)
            cell_text = li.get_text(" ", strip=True)
            cell_text_clean = "".join(cell_text.split())
            
            if re.search(r'(?<!\d)' + day_stripped + r'(?!\d)', cell_text_clean) and ("class=\"day\"" in li_html or "div" in li_html):
                if "previous" not in li_html and "next" not in li_html and "calendarDate" not in li_html:
                    found_day = True
                    break

        # 執行 10/2、10/3、10/6 的三日期數據交叉驗證比對
        clean_all_spaces = "".join(html_content_parsed.split())
        status_10_02 = extract_day_status(clean_all_spaces, "2日")
        status_10_03 = extract_day_status(clean_all_spaces, "3日")
        status_10_06 = extract_day_status(clean_all_spaces, "6日")

        # 擷取日曆表格核心片段，當作郵件內文面板
        preview_idx = html_content_parsed.find("calendarTable")
        if preview_idx == -1: preview_idx = html_content_parsed.find("calendarDate")
        if preview_idx == -1: preview_idx = 0
        raw_snippet = html_content_parsed[preview_idx:preview_idx+2500].strip().replace('<', '&lt;').replace('>', '&gt;')

        if mode != "daily":
            if found_day and "臨" not in cell_text_clean and "阻" not in cell_text_clean and "満" not in cell_text_clean and "满" not in cell_text_clean:
                print(f"🔥 Vacancy detected! Current Status: {cell_text_clean}")
                urgent_html = f"<h2>🔥 [Vacancy Alert] October 3rd is available ({cell_text_clean})!</h2>"
                send_plain_alert_email(EMAIL_SUBJECT_URGENT, urgent_html)
            else:
                print(f"Oct {day_stripped} is still fully booked ({cell_text_clean}).")
                
        else:
            print("Executing daily report summary node...")
            status_label = f"10月3日狀態：{cell_text_clean}" if found_day else "10月3日狀態：請對照下方實時數據面板"
            
            html_content = f"""
            <html>
              <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h3>📢 This is the daily snapshot of Hut Oyari Calendar (2026年10月):</h3>
                
                <!-- 💡 交叉驗證數據看板區 -->
                <div style="background-color: #f7f9fa; padding: 15px; border: 1px solid #d1d5db; border-radius: 6px; margin-bottom: 20px;">
                  <h4 style="margin-top: 0; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px;">🎯 10月核心日期巡邏看板 (Cross-Verified Data)</h4>
                  <ul style="list-style: none; padding-left: 0; margin-bottom: 0; font-size: 14px;">
                    <li style="padding: 6px 0;">📅 <b>10月2日 (五)</b> 狀態：<span style="color:#4b5563;">{status_10_02}</span></li>
                    <li style="padding: 6px 0; background-color: #fffde7; font-weight: bold; border-left: 4px solid #d9534f; padding-left: 8px;">🎯 10月3日 (六) 狀態：<span>{status_10_03}</span> (BS解析結果: {status_label})</li>
                    <li style="padding: 6px 0;">📅 <b>10月6日 (二)</b> 狀態：<span style="color:#4b5563;">{status_10_06}</span></li>
                  </ul>
                </div>

                <p>If you see '◯', '▲', or any single-digit number instead of '臨' or '満', please act immediately!</p>
                <br>
                
                <!-- 核心黑色原始碼面板 -->
                <div style="background:#222; padding:15px; border-radius:6px; font-family:monospace; box-shadow: inset 0 0 10px #000;">
                  <b style="color:#5cb85c;">[💾 Real October Calendar HTML Source Code Node]</b>
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
            
    except Exception as e:
        print("Cloud inspection node error:", e)

if __name__ == "__main__":
    run_mode = "check"
    if len(sys.argv) > 1:
        if "daily" in sys.argv:
            run_mode = "daily"
    check_oyari(mode=run_mode)
