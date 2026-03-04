"""
NSE Option Chain Scraper using Selenium (Browser Automation)
This bypasses NSE's anti-scraping by using real browser
"""

def get_nse_data_selenium(symbol="NIFTY"):
    """
    Fetch NSE data using Selenium (requires Chrome/Firefox)
    Install: pip install selenium webdriver-manager
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
        import time
        import json
        
        print(f"🌐 Opening browser to fetch LIVE {symbol} data...")
        
        # Setup Chrome in headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize driver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        try:
            # Visit NSE homepage first
            driver.get("https://www.nseindia.com")
            time.sleep(2)
            
            # Now fetch option chain API
            api_url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
            driver.get(api_url)
            
            # Wait for page to load
            time.sleep(2)
            
            # Get JSON data from page
            page_source = driver.find_element(By.TAG_NAME, "pre").text
            data = json.loads(page_source)
            
            option_data = data.get('records', {}).get('data', [])
            
            if option_data:
                underlying = data.get('records', {}).get('underlyingValue', 'N/A')
                print(f"✅ SUCCESS via Selenium! Fetched {len(option_data)} strikes")
                print(f"📊 {symbol} Live Price: {underlying}")
                driver.quit()
                return option_data
            else:
                print("⚠️ Selenium fetched data but it's empty")
                driver.quit()
                return None
                
        except Exception as e:
            print(f"❌ Selenium error: {e}")
            driver.quit()
            return None
            
    except ImportError:
        print("❌ Selenium not installed")
        print("📦 Install with: pip install selenium webdriver-manager")
        return None
    except Exception as e:
        print(f"❌ Selenium setup failed: {e}")
        return None


def is_selenium_available():
    """Check if Selenium is installed"""
    try:
        import selenium
        from webdriver_manager.chrome import ChromeDriverManager
        return True
    except ImportError:
        return False
