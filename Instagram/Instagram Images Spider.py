import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
from multiprocessing import Pool

def getimgurl(url,imgurlset):
    driver = webdriver.Chrome("C:/Program Files (x86)/Google/Chrome/Application/chromedriver")
    driver.get(url)
    i = 0  
    while i < 10:
        try:
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            img = soup.find("img",attrs={"class":'FFVAD'})
            imgsrc = img.attrs["src"]
            imgurlset.append(imgsrc)
            button = driver.find_element_by_css_selector('a._8kphn._by8kl.coreSpriteRightChevron')
            time.sleep(1)
            button.click()
            i = i + 1
        except:
            i = i + 1     
    driver.quit()
    return imgurlset

def getImg(imgurl):
    headers= {'user-agent':'Mozilla/5.0'}
    ins_pic=requests.get(imgurl,headers=headers).content
    dirname="E://insimage//"
    filename = dirname+str(time.time())+'.jpg'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    if not os.path.exists(filename):
        with open(filename,'wb') as f:
            f.write(ins_pic)
            print('文件保存成功')
    else:
        print('文件已存在')

def main():
    url = "https://www.instagram.com/p/Bd4KSSXl5CP/?taken-by=wj_2009"
    global imgurllist
    global imgurlset
    imgurllist = getimgurl(url,imgurllist)
    imgurlset = set(imgurllist)
    print("图片链接获取成功")

if __name__ == "__main__":
    imgurllist = []
    imgurlset = ()
    main()
    print(str(imgurlset))
    p = Pool()
    for i in imgurlset:
        p.apply_async(getImg,args=(i,))
    p.close()
    p.join()
    print('程序完成!')
