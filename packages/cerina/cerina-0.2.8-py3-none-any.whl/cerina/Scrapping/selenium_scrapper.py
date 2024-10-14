# cerina/selenium_scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumScraper:
    def __init__(self, name: str, base_url: str, css_selector: str = None, headless: bool = True):
        self.name = name
        self.base_url = base_url
        self.css_selector = css_selector
        self.headless = headless
        self.driver = self._init_driver()

    def _init_driver(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Use webdriver-manager to handle ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    def scrape(self, path: str = '') -> str:
        url = f"{self.base_url}{path}"
        self.driver.get(url)
        
        try:
            if self.css_selector:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.css_selector))
                )
                elements = self.driver.find_elements(By.CSS_SELECTOR, self.css_selector)
                content = "\n".join([element.text for element in elements])
            else:
                content = self.driver.page_source
        except Exception as e:
            raise Exception(f"Failed to scrape {url}. Error: {str(e)}")
        finally:
            self.driver.quit()
        
        return content

    async def use_tool(self, query: str = '') -> str:
        # For simplicity, let's assume the query is directly the path to scrape
        return self.scrape(query)
