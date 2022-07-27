import os
import re
from pathlib import Path
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
# Make sure Chore driver is downloaded in your python enviroment
driver = webdriver.Chrome()
driver.get("https://dermnetnz.org/image-library")
webEle = driver.find_elements(By.XPATH, '//div[@class="imageList__group"]//a')
print(len(webEle))
count = 1
print('Downloading Image...')
list =[]
imageName =[]
for ele in webEle:
    tempList = []
    pageUrl = ele.get_attribute("href")
    name = ele.find_element(By.XPATH,".//div/h6").text
    src = ele.find_element(By.XPATH,".//div/img").get_attribute("src")
    data = requests.get(src).content
    if not os.path.exists(os.path.abspath(__file__).replace('assignment1.py','')+'\\IconImage'):
        os.makedirs(os.path.abspath(__file__).replace('assignment1.py','')+'\\IconImage')
    file = Path(os.path.abspath(__file__).replace('assignment1.py','')+'\\IconImage\\'+str(count)+re.sub(r"[^a-zA-Z0-9]","",name)+'.jpg')
    file.touch(exist_ok=True)
    with open(os.path.abspath(__file__).replace('assignment1.py','')+'IconImage\\'+str(count)+re.sub(r"[^a-zA-Z0-9]","",name)+'.jpg', 'wb') as f:
        f.write(data)
    print('.',end='')

    tempList.append(name)
    tempList.append(pageUrl)
    imageName.append(str(count)+re.sub(r"[^a-zA-Z0-9]","",name)+'.jpg')
    list.append(tempList)
    count = count + 1
print('Downloading done...',end='\n')
driver.close()

df = pd.DataFrame(list)
writer = pd.ExcelWriter('list_of_diseases.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index=False,header=False)

workbook  = writer.book
worksheet = writer.sheets['Sheet1']
worksheet.set_default_row(95)
worksheet.set_column(0,3,30)

for index in range(0,294):
    worksheet.insert_image('C'+str(1+index), './/IconImage//'+imageName[index])
writer.save()
