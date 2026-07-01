import time
import sys
import requests
from bs4 import BeautifulSoup

URL_BASE = "https://enzanso-reservation.jp"
URL_POST_TARGET = "https://enzanso-reservation.jp"

def verify_html(html_text, method_name):
    """診斷大會師：嚴格檢查回傳的網頁到底是不是 10 月真實數據"""
    if not html_text:
        print(f"❌ [{method_name}] -> 失敗：回傳真空（None/Empty）")
        return False
        
    clean_text = "".join(html_text.split())
    
    if "metahttp-equiv=\"refresh\"" in clean_text or "予約ページへ移動しています" in clean_text:
        print(f"❌ [{method_name}] -> 失敗：被 WAF 攔截，吐回 222 位元組轉址空殼。")
        return False
        
    # 核心檢查：10/2, 10/3, 10/6 實時網頁特徵字串
    features = ["20261002", "20261003", "20261006", "3日", "onclick=\"return doPost"]
    matched = [f for f in features if f in html_text]
    
    if len(matched) > 0:
        print(f"🟢🟢🟢 [{method_name}] -> 突破防線成功！！！")
        print(f"    -> 命中 10 月特徵: {matched}")
        return True
    else:
        print(f"❌ [{method_name}] -> 失敗：網頁順利下載，但死死卡在預設月份（7月），查無 10 月資料。")
        return False

# ===================================================================
# 🧪 矩陣 1：Playwright 從首頁正門進 + 物理點擊次月 3 次
# ===================================================================
def test_matrix_1():
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL_BASE, wait_until="networkidle")
            time.sleep(2)
            
            # 使用 no_wait_after=True 阻止它死等整頁重新整理
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(6)
            
            html = page.content()
            browser.close()
            verify_html(html, "矩陣 1: Playwright 正門進 + 物理連續點擊次月")
    except Exception as e:
        print(f"💥 [矩陣 1] 發生重大崩潰: {e}")

# ===================================================================
# 🧪 矩陣 2：Playwright 從正門進 + 純 Python 操作 select 選單
# ===================================================================
def test_matrix_2():
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL_BASE, wait_until="networkidle")
            time.sleep(2)
            
            page.select_option("select[name='y']", value="2026")
            page.select_option("select[name='m']", value="10")
            page.locator("input[type='submit'][value='表示']").click(no_wait_after=True)
            time.sleep(6.5)
            
            html = page.content()
            browser.close()
            verify_html(html, "矩陣 2: Playwright 正門進 + 變更 select 選單")
    except Exception as e:
        print(f"💥 [矩陣 2] 發生重大崩潰: {e}")

# ===================================================================
# 🧪 矩陣 3：Playwright 引進 stealth 隱形外掛 + 物理點擊次月 3 次
# ===================================================================
def test_matrix_3():
    from playwright.sync_api import sync_playwright
    try:
        from playwright_stealth import stealth_sync
    except ImportError:
        print("❌ [矩陣 3] 失敗：環境缺乏 playwright-stealth")
        return
        
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
            page = browser.new_page()
            stealth_sync(page) # 抹除機器人指紋特徵
            
            page.goto(URL_BASE, wait_until="networkidle")
            time.sleep(2)
            
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(3.5)
            page.get_by_role("link", name="次月").click(no_wait_after=True)
            time.sleep(6)
            
            html = page.content()
            browser.close()
            verify_html(html, "矩陣 3: Playwright + Stealth防偵測 + 物理點擊")
    except Exception as e:
        print(f"💥 [矩陣 3] 發生重大崩潰: {e}")

# ===================================================================
# 🧪 矩陣 4：Playwright 從正門進 + 注入純單行 JavaScript 表單提交
# ===================================================================
def test_matrix_4():
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL_BASE, wait_until="networkidle")
            time.sleep(3)
            
            js_code = "() => { const f = document.querySelector('form'); if(f) { f.p.value='30'; f.y.value='2026'; f.m.value='10'; f.agree.value='1'; f.submit(); } }"
            page.evaluate(js_code)
            time.sleep(8)
            
            html = page.content()
            browser.close()
            verify_html(html, "矩陣 4: Playwright 正門進 + 注入 JS form.submit()")
    except Exception as e:
        print(f"💥 [矩陣 4] 發生重大崩潰: {e}")

# ===================================================================
# 🧪 矩陣 5：Playwright 從正門進 + 智慧 DOM 字串監聽 (wait_for_selector)
# ===================================================================
def test_matrix_5():
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL_BASE, wait_until="networkidle")
            time.sleep(2)
            
            page.select_option("select[name='m']", value="10")
            page.locator("input[type='submit'][value='表示']").click(no_wait_after=True)
            
            print(" -> [矩陣 5 監視器啟動] 正在盯梢網頁 DOM 樹變更...")
            page.wait_for_selector("text=2026年10月", timeout=12000)
            time.sleep(2)
            
            html = page.content()
            browser.close()
            verify_html(html, "矩陣 5: Playwright 正門進 + wait_for_selector 智慧盯梢")
    except Exception as e:
        print(f"💥 [矩陣 5] 發生重大崩潰: {e}")

if __name__ == "__main__":
    print("===================================================================")
    print("🔬 啟動 GitHub 雲端環境【全矩陣自動化模擬技術】大範圍測試大會師 🔬")
    print("===================================================================\n")
    test_matrix_1()
    test_matrix_2()
    test_matrix_3()
    test_matrix_4()
    test_matrix_5()
    print("==================== 🧪 矩陣交叉實驗全部結束 ====================")
