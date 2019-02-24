from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException,NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
from spiderMaterialsProject import config
from spiderMaterialsProject import dataManager
import os

def loadSharedCookies(browser,cookiesPath = "sharedCookies.json"):
    """ load Cookies for login """
    import json
    import os
    if os.path.exists(cookiesPath):
        with open(cookiesPath,'r',encoding="utf-8") as rjson:
            listCookies = json.loads(rjson.read())
        for cookies in listCookies:
            browser.add_cookie(cookies)
    return browser


def get_png(url,filename = "test.png"):
    """ download png from url by requests"""
    import requests
    r = requests.get(url)
    with open(filename,"wb") as png:
        png.write(r.content)


def loopToTry(count = 10):
    """ a decorator for loop try """
    def www(callback):
        def new(spider):
            for i in range(count):
                try:
                    callback(spider)
                    break
                except ElementNotVisibleException as e:
                    print("wait to try for %d/%d" % (i,count))
                    time.sleep(1)
        return new
    return www
        
def first_click_btn_by_css_selector(css):
    def www(callback):
        def new(spider):
            browser = spider.getBrowser()
            btn_selector = (By.CSS_SELECTOR,css)
            WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(btn_selector))
            btn = browser.find_element_by_css_selector(css)
            btn.click()
            callback(spider)
        return new
    return www

class spider(object):
    """docstring for spider"""
    def __init__(self):
        super(spider, self).__init__()
        if False:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            browser = webdriver.Chrome(options = chrome_options)
        else:
            browser = webdriver.Chrome()  # register a browser
        if not "index" in config.url.keys():
            raise ValueError("please set a index page url") 
        browser.get(config.url["index"])
        if "cookies" in config.savepath.keys():  # load cookies to login
            browser = loadSharedCookies(browser,config.savepath["cookies"])
        self.browser = browser

    def getBrowser(self):
        return self.browser

    def search(self,query_str):
        browser = self.getBrowser()
        browser.get(config.url["index"])
        material_id = []
        try:
            selector = (By.ID,"input-primary")
            WebDriverWait(browser,20,0.5).until(EC.presence_of_element_located(selector))
            inputArea = browser.find_element_by_id("input-primary")
            inputArea.clear()
            for char in query_str:
                inputArea.send_keys(char)
        except Exception as e:
            raise e
        try:
            selector = (By.ID,"submit-search")
            WebDriverWait(browser,20,0.5).until(EC.presence_of_element_located(selector))
            submit = browser.find_element_by_id("submit-search")
            submit.click()
        except Exception as e:
            raise e
        try:
            selector = (By.TAG_NAME,"table")
            WebDriverWait(browser,20,0.5).until(EC.presence_of_element_located(selector))
            table = browser.find_element_by_tag_name("table")
            information = table.text.split("\n")[1:]
            import re
            re_m = re.compile("^[\\S]+-[\\S]+")
            for inform in information:
                match = re_m.search(inform)
                if match:
                    material_id.append(match.group())
        except Exception as e:
            raise e
        return material_id
            

    def innerPage(self,id):  # go to innerPage by id
        browser = self.getBrowser()
        url = config.url["innerpage"] % id
        browser.get(url)
        print(self.get_Material_Details())  # get MaterialDetails str
        try:
            print(self.get_band_image_src())    # get band image url
            print(self.get_dos_image_src())     # get dos image url
        except Exception as e:
            pass   
        self.download_vasp_file()           # download file

    def exceptionHandle(self):
        pass
        
    def get_Material_Details(self):
        browser = self.getBrowser()
        span = browser.find_element_by_class_name('span3')
        return span.text

    def get_band_image_src(self):
        browser = self.getBrowser()
        parent = browser.find_element_by_id('bandstructure-plot')
        img = parent.find_element_by_tag_name('img')
        imgsrc = img.get_attribute('src')
        return imgsrc

    def get_dos_image_src(self):
        browser = self.getBrowser()
        parent = browser.find_element_by_id('dos-graph')
        img = parent.find_element_by_tag_name('img')
        return img.get_attribute('src')

    @loopToTry(10)
    @first_click_btn_by_css_selector('.multiselect.dropdown-toggle.btn.btn-link')
    def download_vasp_file(self):
        """ default path is ~/Download 
            make sure your browser is not in headless mode
        """
        browser = self.getBrowser()
        selection = browser.find_element_by_css_selector('.multiselect-container.dropdown-menu')
        vasp_select = selection.find_elements_by_tag_name('input')
        vasp_select = vasp_select[1]
        vasp_select.click()
        download_btn = browser.find_element_by_id('download-files')
        download_btn.click()

    def quit(self):
        self.browser.quit()
        
        
class requestsDownload(object):
    """docstring for requestsDownload
        this class is designed for downloading file quickly 
    """
    def __init__(self):
        from spiderMaterialsProject import loadHar
        super(requestsDownload, self).__init__()
        headers = config.headers
        postdata = config.postdata
        postdata,headers = loadHar.loadHar(postdata,headers,config.savepath["har"])
        self.headers = headers
        self.postdata = postdata
        self.ZipUrl = config.url["ZipUrl"]

    def getBandImage(self,url):
        """ make sure resource is exists """
        get_png(url,"band.png")

    def getDosImage(self,url):
        """ make sure resource is exists """
        get_png(url,"dos.png")

    def getVaspZip(self,id):
        """ download zip file """
        import requests
        postdata = self.postdata
        postdata["material_id"] = id
        r = requests.post(self.ZipUrl, headers = self.headers, data = postdata)
        with open("Vasp.zip","wb") as file:
            file.write(r.content)

    def searchByElement(self,query):
        """ search by Element;
            query is a dict like 
                {"nelements":2,"elements":"Mo-Se"}
        """
        import requests
        s = "https://www.materialsproject.org/apps/materials_explorer/results?query={%s}"
        query_str = '"nelements":{nelements},"elements":"{elements}"'.format(**query)
        r = requests.get(s % query_str, headers = self.headers)
        return r



