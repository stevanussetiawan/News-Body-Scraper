import time
import requests
import multiprocessing
# from fuzzywuzzy import fuzz
from trafilatura import fetch_url 
from trafilatura import extract
from trafilatura.spider import focused_crawler
from trafilatura.spider import is_still_navigation
from trafilatura.settings import use_config
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import urllib.request

class GetIsiBerita:
    
    def open_driver(self,linknya):
        # print('-----------------------------', linknya)
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage') 
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0")   

        if sys.platform.startswith('linux'):
            chromedriver = os.path.join(os.getcwd(),'chromedriver')
        
        elif sys.platform.startswith('win'):
            chromedriver = os.path.join(os.getcwd(),'chromedriver.exe')

        driver = webdriver.Chrome(options=options, executable_path="folder_chromedriver\chromedriver.exe")
        driver.get(linknya)

        return driver

    def request_web(self,url):
        try:
            # print(url)
            # url_new = req.split("URL=\\'")[1].split("\\'\">'")[0].strip("../")
            session = requests.Session()
            # resp = session.get(url,  headers=headers,proxies=proxies, allow_redirects=True)
            resp = session.get(url, allow_redirects=True)
            # print(resp.url)
            downloaded = resp.text
            if resp.status_code == 403:
                print('MASUK MAS')
                print(url)
                driver = self.open_driver(url)
                # wait = WebDriverWait(driver, 10)
                # element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'b_algo')))
                downloaded = driver.page_source
            response = extract(downloaded, include_comments=False, include_tables=False)
            isi_berita = response
            isi_berita = ''.join(isi_berita.splitlines())
            isi_berita = isi_berita.replace("\n", "")
            print(response)
            # print(result)
        except Exception as e:
            # result.value = response_full
            isi_berita = ""
            print("*************************************")
            print(e)
        return isi_berita
    
    def  get_isi_berita(self, list_search, result):
        sts = False
        isi_berita = ''
        try:
            data = list_search.pop()
            sts = True
        except:
            pass
        
        if sts:
            link_berita = data.get('web_url')

            if link_berita:
                    s_req = time.time()
                    manager = multiprocessing.Manager()
                    res = manager.Value('i','')
                    p = multiprocessing.Process(target=self.request_web, args=(link_berita,res,))
                    try:
                        p.start()
                        p.join()
                    except FileNotFoundError as e:
                        print(f"FileNotFoundError: {e}")
                    response = res.value
                    # print(response)
                    if response:
                        isi_berita = response
                        isi_berita = ''.join(isi_berita.splitlines())
                        isi_berita = isi_berita.replace("\n", "")
                    else:
                        isi_berita = ''
            else:
                isi_berita = ''
                
            data.setdefault('web_body',isi_berita)
            result.append(data)
        # print(result)
        return isi_berita