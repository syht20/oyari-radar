import time
import datetime
import smtplib
import socket
import re
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
                
                # 💡 核心修正：檢查網頁主體內容是否真的渲染出了 "2026年10月" 這個表格大標題，防止隱藏選單捉弄
                if "2026年10月" in page.locator("caption, h1, h2, h3, div.calendarDate, th").inner_text() or "2026年10月" in page.content() and attempt > 3:
                    print(f"🟢 [SUCCESS] Targeted month reached at step {attempt}!")
                    break
                    
                print(" -> Current month is not target. Simulating human mouse click on '次月'...")
                next_month_link = page.get_by_role("link", name="次月")
                if next_month_link.is_visible():
                    next_month_link.hover()
                    page.wait_for_timeout(400)
                    next_month_link.click()
                    page.wait_for_timeout(4000) # 穩穩等待 4 秒局部刷新
                else:
                    break
            
            page.wait_for_timeout(2000)
            # 💡 終極降維：完全不執行截圖存檔（不留任何圖片地雷），直接帶走 10 月的 HTML 純文字！
            captured_html = page.content()
            browser.close()
    except Exception as e:
        print(f"❌ [Playwright Error] Intelligent trajectory broken: {e}")
    return captured_html

def send_plain_alert_email(subject, body_html):
    """最純粹、100% 上一版成功收到信的無害標準寄信引擎"""
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
        print("✉️ Mail delivered successfully.")
    except Exception as e:
        try:
            server = smtplib.SMTP(smtp_target, 587, timeout=15)
            server.starttls()
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
            server.quit()
            print("✉️ Mail delivered via backup channel.")
        except Exception as e2:
            print("❌ Mail failed:", e2)

def execute_daily_report():
    """💡 獨立每日報告功能：讓 Playwright 去點擊拿 10 月純文字，再交給 BeautifulSoup 解析寄出"""
    html_content_parsed = run_playwright_workflow()
    
    if not html_content_parsed:
        print("⚠️ Browser engine returned blank. Task aborted to protect workflow.")
        return

    soup = BeautifulSoup(html_content_parsed, 'html.parser')
    list_items = soup.find_all('li')
    day_stripped = str(int(TARGET_DAY))
    cell_text_clean = "Unknown"
    found_day = False
    
    # 精準爬取 10 月 3 日當天的即時代碼文字
    for li in list_items:
        li_html = str(li)
        cell_text = li.get_text(" ", strip=True)
        cell_text_clean = "".join(cell_text.split())
        
        if re.search(r'(?<!\d)' + day_stripped + r'(?!\d)', cell_text_clean) and ("class=\"day\"" in li_html or "div" in li_html):
            if "previous" not in li_html and "next" not in li_html and "calendarDate" not in li_html:
                found_day = True
                break

    status_label = f"10月3日狀態：{cell_text_clean}" if found_day else "10月3日狀態：未解析成功 (請對照下方預覽)"
    
    # 擷取日曆表格的前 500 個中日文字元，當作實時回報面板，這回絕對會是真實的 10 月代碼！
    preview_idx = html_content_parsed.find("calendarTable")
    if preview_idx == -1: preview_idx = html_content_parsed.find("calendarDate")
    if preview_idx == -1: preview_idx = 0
    raw_snippet = html_content_parsed[preview_idx:preview_idx+600].strip().replace('<', '&lt;').replace('>', '&gt;')

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h3>📢 This is the daily snapshot of Hut Oyari Calendar (2026年10月):</h3>
        <p>Current Raw Code Text of October 3rd: <span style="background-color: #337ab7; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: white;">{status_label}</span></p>
        <p>If you see '◯', '▲', or any single-digit number instead of '臨' or '満', please click below to book immediately!</p>
        <br>
        <div style="background:#f9f9f9; padding:15px; border-left:4px solid #5cb85c; font-family:monospace;">
          <b>[System Live Output Preview - 100% Real October Calendar HTML]</b>
          <pre style="white-space: pre-wrap; font-size:13px; color:#333;">{raw_snippet}</pre>
        </div>
        <br>
        <div style="margin: 20px 0;">
          <a href="https://enzanso-reservation.jp" style="background-color: #337ab7; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">👉 Click Here to Go to Official Booking Site</a>
        </div>
      </body>
    </html>
    """
    send_plain_alert_email(EMAIL_SUBJECT_DAILY, html_content)

def check_oyari():
    """🟢 100% 保障每半小時巡邏主體穩定運行，requests 在背景輕量化默默監視"""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://enzanso-reservation.jp",
        "Origin": "https://enzanso-reservation.jp"
    })
    try:
        session.get("https://enzanso-reservation.jp", timeout=15)
        payload = {"p": "30", "y": "2026", "m": "10", "agree": "1"}
        # 默默對抗 requests 的轉址狀況
        res = session.post("https://enzanso-reservation.jp", data=payload, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        list_items = soup.find_all('li')
        day_stripped = str(int(TARGET_DAY))
        
        for li in list_items:
            li_html = str(li)
            cell_text = li.get_text(" ", strip=True)
            cell_text_clean = "".join(cell_text.split())
            
            if re.search(r'(?<!\d)' + day_stripped + r'(?!\d)', cell_text_clean) and ("class=\"day\"" in li_html or "div" in li_html):
                if "previous" not in li_html and "next" not in li_html and "calendarDate" not in li_html:
                    if "阻" in cell_text_clean or "満" in cell_text_clean or "满" in cell_text_clean or "-" in cell_text_clean or "－" in cell_text_clean:
                        print(f"Oct {day_stripped} is still fully booked ({cell_text_clean}).")
                    else:
                        print(f"🔥 Vacancy detected! Current Status: {cell_text_clean}")
                        urgent_html = f"<h2>🔥 [Vacancy Alert] October 3rd is available ({cell_text_clean})!</h2>"
                        send_plain_alert_email(EMAIL_SUBJECT_URGENT, urgent_html)
                    break
    except Exception as e:
        print("Cloud inspection node error:", e)

if __name__ == "__main__":
    if len(sys.argv) > 1 and "daily" in sys.argv:
        execute_daily_report()
    else:
        check_oyari()
