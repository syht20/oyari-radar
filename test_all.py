import time
import re
import requests
from bs4 import BeautifulSoup

URL_BASE = "https://enzanso-reservation.jp"
URL_POST_TARGET = "https://enzanso-reservation.jp"

def verify_html(html_text, method_name):
    """驗證回傳的 HTML 是否含有 10 月份真實日曆的關鍵特徵"""
    if not html_text:
        print(f"❌ [{method_name}] 失敗：回傳內容為空。")
        return False
    
    clean_text = "".join(html_text.split())
    
    # 檢查是否含有轉址空殼
    if "metahttp-equiv=\"refresh\"" in clean_text or "予約ページへ移動しています" in clean_text:
        print(f"⚠️ [{method_name}] 失敗：被網站判定為機器人，吐回 222 位元組轉址空殼。")
        return False

    # 交叉核對 10/2, 10/3, 10/6 關鍵字
    features = ["20261002", "20261003", "20261006", "3日", "6日"]
    found_features = [f for f in features if f in clean_text]
    
    if len(found_features) > 0:
        print(f"🟢🟢🟢 [{method_name}] 成功突破防線！！！")
        print(f" -> 命中 10 月實時特徵: {found_features}")
        # 印出關鍵片段供肉眼核對
        idx = html_text.find("day")
        if idx == -1: idx = 0
        print(f" -> 數據片段預覽: {html_text[idx:idx+300].strip()}\n")
        return True
    else:
        print(f"❌ [{method_name}] 失敗：網頁順利下載，但內容停留在預設月份（7月），查無 10 月資料。")
        return False

# ===================================================================
# 🧪 方法 1：純 requests.post 直撞首頁根目錄 (Version 1 最初設定)
# ===================================================================
def test_method_1():
    try:
        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        session.get(URL_BASE, timeout=15)
        payload = {"p": "30", "y": "2026", "m": "10", "agree": "1"}
        res = session.post(URL_BASE, data=payload, timeout=15)
        res.encoding = 'utf-8'
        verify_html(res.text, "方法 1: requests.post 直撞首頁")
    except Exception as e:
        print(f"❌ [方法 1] 發生異常: {e}")

# ===================================================================
# 🧪 方法 2：純 requests.post 直撞實體 PHP 後台
# ===================================================================
def test_method_2():
    try:
        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        session.get(URL_BASE, timeout=15)
        payload = {"p": "30", "y": "2026", "m": "10", "agree": "1"}
        res = session.post(URL_POST_TARGET, data=payload, timeout=15)
        res.encoding = 'utf-8'
        verify_html(res.text, "方法 2: requests.post 直撞實體 PHP")
    except Exception as e:
        print(f"❌ [方法 2] 發生異常: {e}")

# ===================================================================
# 🧪 方法 3：純 requests.post 模擬網頁原生 AJAX 的 doPost 數據包
# ===================================================================
def test_method_3():
    try:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "https://enzanso-reservation.jp?p=30",
            "Origin": URL_BASE
        })
        session.get(URL_BASE, timeout=15)
        time.sleep(2)
        ajax_payload = {"yoteibi": "20261001", "p": "30", "agree": "1"}
        res = session.post(URL_POST_TARGET, data=ajax_payload, timeout=15)
        res.encoding = 'utf-8'
        verify_html(res.text, "方法 3: requests 模擬實體 AJAX doPost")
    except Exception as e:
        print(f"❌ [方法 3] 發生異常: {e}")

# ===================================================================
# 🧪 方法 4：Playwright 模擬真人點擊次月 3 次 (不等待網頁重載變體)
# ===================================================================
def test_method_4():
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"{URL_POST_TARGET}?p=30", wait_until="networkidle")
            time.sleep(2)
            
            # 連續點擊並強制不等待重載
            for _ in range(3):
                page.get_by_role("link", name="次月").click(no_wait_after=True)
                time.sleep(3)
                
            html = page.content()
            browser.close()
            verify_html(html, "方法 4: Playwright 物理點擊次月 3 次")
    except Exception as e:
        print(f"❌ [方法 4] 發生異常: {e}")

# ===================================================================
# 🧪 方法 5：Playwright 智慧監聽動態 DOM 元素出現 (文字盯梢變體)
# ===================================================================
def test_method_5():
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"{URL_POST_TARGET}?p=30", wait_until="networkidle")
            
            page.select_option("select[name='y']", value="2026")
            page.select_option("select[name='m']", value="10")
            page.locator("input[type='submit'][value='表示']").click(no_wait_after=True)
            
            # 死等 10月 字樣出現在 DOM 樹上
            page.wait_for_selector("text=2026年10月", timeout=10000)
            time.sleep(2)
            
            html = page.content()
            browser.close()
            verify_html(html, "方法 5: Playwright 智慧 DOM 文字盯梢")
    except Exception as e:
        print(f"❌ [方法 5] 發生異常: {e}")

# ===================================================================
# 🧪 方法 6：Playwright 直接對網頁前端注入執行實體 doPost 函數 (字串深拷貝變體)
# ===================================================================
def test_method_6():
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"{URL_POST_TARGET}?p=30", wait_until="networkidle")
            time.sleep(2)
            
            # 強行在前端執行網頁自帶的切換函數
            page.evaluate("doPost(document.calendarform, '#yoteibi', '20261001')")
            time.sleep(5)
            
            html = str(page.content())
            browser.close()
            verify_html(html, "方法 6: Playwright 注入原生 doPost 函數")
    except Exception as e:
        print(f"❌ [方法 6] 發生異常: {e}")

if __name__ == "__main__":
    print("=== ⛰️ 開始執行燕山莊預約系統 6 大底層協議交叉實驗 ===\n")
    test_method_1()
    test_method_2()
    test_method_3()
    test_method_4()
    test_method_5()
    test_method_6()
    print("================== 🔬 實驗全部結束 ==================")
