from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

from database import Paper, Session

url = "https://kns.cnki.net/kns8s/defaultresult/index?crossids=YSTT4HG0%2CLSTPFY1C%2CJUP3MUPD%2CMPMFIG1A%2CWQ0UVIAA%2CBLZOG7CK%2CPWFIRAGL%2CEMRPGLPA%2CNLBO1Z6R%2CNN3FJMUV&korder=SU&kw=%E8%A5%BF%E5%AE%89%E6%96%87%E7%90%86"

chrome_options = Options()
# 可以选择是否以无头模式运行（即不显示浏览器窗口）
# chrome_options.add_argument('--headless')


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

cookies_str = 'SID=017030; Ecp_loginuserjf=17364510072; Ecp_LoginStuts={"IsAutoLogin":true,"UserName":"17364510072","ShowName":"17364510072","UserType":"jf","BUserName":"KP1002","BShowName":"%E6%B8%A9%E5%B7%9E%E5%A4%A7%E5%AD%A6","BUserType":"bk","r":"mnd9Yn","Members":[]}; c_m_LinID=LinID=WEEvREcwSlJHSldTTEYySCtSZ1hhTEhqdThwdk9RSDJoRzlDMFVrOE9Odz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&ot=06%2F04%2F2025%2001%3A21%3A54; LID=WEEvREcwSlJHSldTTEYySCtSZ1hhTEhqdThwdk9RSDJoRzlDMFVrOE9Odz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; c_m_expire=2025-06-04%2001%3A21%3A54; Ecp_session=1; tfstk=gftjdMxkxSVfh5ITCZDPdDNgteIsTYoeBR69KdE4BiIx1F9Oan7wgE8W5BJdMiJNg8COwBL27qXqCOp6Ooz2_1RSfQOpu5-6Il69BCDc_x0ynKjGXXlFfDJDncMZcxlPXApRbO12ShhHnKjgEXlEYDJ0CZDUMxs96gURI9sOBoEtF7BFwoBTDOF-F_fRX1dOXY9RZOsO6ChhZb6olspjnCFn0QWc9KC7XlwFhZCKx_ZTX36bT6pf-lE9Vt_v2C30KR72WpbH0Ko_qiJBygBX6DhA2pLWLZtjOo5G53OX5IkaSTT6BHjcARnvFi1fJn_0IoApFdLFP3kKxisAMFSDQJG2FnO2n39aBzIf0U_BcMn3M18ydh66jfmWOKLp6Fszuk5Btu4aFwq1F6kSFP4ZXYDM4toZXZQAET-EFYNbSZBlF_DSFPVVkTXPHYM7-8C..; _c_WBKFRo=vElnlF9lffHu8hltBAlh3ZydNGiwKuwQWhbkdeM9; _nb_ioWEgULi='
cookies = {k.strip(): v.strip() for k, v in (cookie.split("=", 1) for cookie in cookies_str.split("; "))}

driver.get(url)

for name, value in cookies.items():
    driver.add_cookie({'name': name, 'value': value})

driver.refresh()

page_num = 5
current_page = 1

try:
    while current_page <= page_num:
        print(f'Current Page:{current_page}')
        time.sleep(5)

        paper_table = driver.find_element(By.CLASS_NAME, 'result-table-list')
        tr_elements = paper_table.find_elements(By.TAG_NAME, 'tr')

        session = Session()
        for tr in tr_elements[1:]:
            # print(tr.text)
            paper_name = tr.find_element(By.CSS_SELECTOR, 'td.name')
            try:
                paper_author = tr.find_element(By.CSS_SELECTOR, 'a.KnowledgeNetLink')
            except:
                paper_author = type('EmptyElement', (), {'text': ''})()
            paper_date = tr.find_element(By.CSS_SELECTOR, 'td.date')
            paper_data = tr.find_element(By.CSS_SELECTOR, 'td.data')
            try:
                paper_source = tr.find_element(By.TAG_NAME, 'p')
            except:
                paper_source = type('EmptyElement', (), {'text': ''})()
            print(f'论文题目:{paper_name.text}')
            print(f'作者名称:{paper_author.text}')
            print(f'发表时间:{paper_date.text}')
            print(f'数据来源:{paper_source.text}')
            print(f'数据库：{paper_data.text}')
            print("=" * 16)

            paper = Paper(
                paper_name=paper_name.text,
                paper_author=paper_author.text,
                paper_date=paper_date.text,
                paper_source=paper_source.text,
                paper_data=paper_data.text
            )
            session.add(paper)
        session.commit()
        session.close()

        try:
            next_page_button = driver.find_element(By.CSS_SELECTOR, 'a.pagesnums#PageNext')
            next_page_button.click()
            current_page += 1
        except:
            break


except Exception as e:
    print(f"发生错误: {e}")
# finally:
# 关闭浏览器
# driver.quit()
