import os

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from csv import writer
import user_agent
import fileHandling
import glob
import matplotlib.image as mpimg
from PIL import Image

url = 'https://www.wjs.co.in/#products'

options = webdriver.ChromeOptions()
options.add_argument(user_agent.userAgent)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# driver = webdriver.Chrome(service=Service(ChromeDriverManger().install()), options=options)
driver = webdriver.Chrome(executable_path=user_agent.executablePath)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
         Object.defineProperty(navigator, 'webdriver', {
         get: () => undefined
         })
      """
})

driver.get(url)
driver.implicitly_wait(10)
time.sleep(4)
source = driver.page_source

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(source)

soup = BeautifulSoup(source, features='html.parser')

list = soup.find('div', class_='topnav').select_one('li:nth-child(3)').find('ul').find_all('a')
# list=list.find_all('a')

product_type_list = []
for i in list:
    product = i.get('href')
    product_type_list.append(product)

# print(product_type_list)
headers = {
    'user-agent': user_agent.userAgent,
}


# convert link to image

def link_to_image(image_link):
    res = requests.get(image_link, headers=headers, stream=True)
    filename = image_link.split("/")[-1]
    isExist = os.path.exists('./lighting_Art_images')
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs('./lighting_Art_images')
    # print(filename)
    if res.status_code == 200:
        res.raw.decode_content = True
        with open(r'.\lighting_Art_images\\' + filename, 'wb') as f:
            # shutil.copyfileobj(res.raw, f)
            f.write(res.content)


def image_grid(columns, space, images,name):
    rows = len(images) // columns
    if len(images) % columns:
        rows += 1
    width_max = max([Image.open(image).width for image in images])
    height_max = max([Image.open(image).height for image in images])
    background_width = width_max * columns + (space * columns) - space
    background_height = height_max * rows + (space * rows) - space
    background = Image.new('RGBA', (background_width, background_height), (255, 255, 255, 255))

    x = 0
    y = 0
    for i, image in enumerate(images):
        img = Image.open(image)
        x_offset = int((width_max-img.width)/2)
        y_offset = int((height_max-img.height)/2)
        background.paste(img, (x+x_offset, y+y_offset))
        x += width_max + space
        if (i+1) % columns == 0:
            y += height_max + space
            x = 0
    background.save(name+'.png')


for i in product_type_list:

    print("------------{}-----------".format(i), '\n')
    item_name = str(i).split('/')[-2]
    print(item_name)
    values = [" ", item_name]

    with open(r'.\Lighting_Art.csv', 'a', encoding='utf8', newline='') as f:
        write = writer(f)
        write.writerow(values)

    driver.get(i)
    driver.implicitly_wait(10)
    time.sleep(4)

    product_type_source = driver.page_source

    '''with open('individual_user.html', 'w', encoding='utf-8') as f:
        f.write(product_type_source)'''

    product_soup = BeautifulSoup(product_type_source, features="html.parser")

    products = product_soup.find_all('div', class_='ngg-gallery-thumbnail')
    product_images_link = []
    for product in products:
        link = product.find('img').get('src')
        product_images_link.append(link)
        srNo = len(product_images_link)
        # print(type(link))
        #C:\Users\Lenovo\PycharmProjects\pythonProject
        values = [srNo, link]
        with open(r'.\Lighting_Art.csv', 'a', encoding='utf8',
                  newline='') as f:
            write = writer(f)
            write.writerow(values)

        link_to_image(link)
    print(len(product_images_link))
    images = []
    images_path=[]
    for img_path in glob.glob(r'.\lighting_Art_images\*.jpg'):
        images_path.append(img_path)
        images.append(mpimg.imread(img_path))
        #print(type(img_path))
        #print(type(mpimg.imread(img_path)))

    print('all images:')
    print(images_path)

    image_grid(columns=5, space=20,images=images_path,name=item_name)
    images.clear()
    images_path.clear()
   # print('cleared images :\n')
    #print(images_path)

    # clear directory
    files = glob.glob(r'.\lighting_Art_images\*')
    for f in files:
        os.remove(f)

#remove directory
os.rmdir(r'.\lighting_Art_images')