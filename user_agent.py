from selenium import webdriver
op=webdriver.ChromeOptions()
executablePath=r'C:\Users\Lenovo\Downloads\chromedriver.exe'
#" chromedriver path :C:\Users\Lenovo\Downloads\chromedriver.exe "
driver=webdriver.Chrome(executable_path=executablePath)
userAgent=driver.execute_script("return navigator.userAgent")
print(userAgent)
