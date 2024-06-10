import time
import requests
import multiprocessing
from trafilatura import extract
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import os

class NewsContentFetcher:
    def __init__(self):
        self.driver_path = self._get_driver_path()

    def _get_driver_path(self):
        if sys.platform.startswith('linux'):
            return os.path.join(os.getcwd(), 'chromedriver')
        elif sys.platform.startswith('win'):
            return os.path.join(os.getcwd(), 'chromedriver.exe')
        return None

    def _initialize_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
        )
        driver = webdriver.Chrome(options=options, executable_path=self.driver_path)
        return driver

    def fetch_web_content(self, url):
        try:
            session = requests.Session()
            response = session.get(url, allow_redirects=True)
            if response.status_code == 403:
                driver = self._initialize_driver()
                driver.get(url)
                response_text = driver.page_source
                driver.quit()
            else:
                response_text = response.text

            extracted_content = extract(response_text, include_comments=False, include_tables=False)
            if extracted_content:
                extracted_content = ''.join(extracted_content.splitlines())
            return extracted_content or ""
        except Exception as e:
            print(f"Error fetching content from {url}: {e}")
            return ""

    def process_article(self, article_data, results):
        try:
            article = article_data.pop()
        except IndexError:
            return ""

        link = article.get('web_url')
        if not link:
            return ""

        manager = multiprocessing.Manager()
        result = manager.Value('i', '')
        process = multiprocessing.Process(target=self.fetch_web_content, args=(link, result))

        try:
            process.start()
            process.join()
        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")

        article_body = result.value
        article['web_body'] = article_body
        results.append(article)
        return article_body

if __name__ == "__main__":
    # Example usage:
    fetcher = NewsContentFetcher()
    example_list_search = [{'web_url': 'http://example.com/news-article'}]
    result_list = []

    fetcher.process_article(example_list_search, result_list)
    print(result_list)