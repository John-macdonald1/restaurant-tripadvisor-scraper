from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import re
import time
chrome_options = Options()
chrome_options.add_argument("--headless")
with open('restaurants.csv', 'w', encoding='utf-8') as file:
    file.write('Restaurant Name, Address, Postcode, Contact Number, Website, Email \n')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.tripadvisor.co.nz/Restaurants-g255118-Christchurch_Canterbury_Region_South_Island.html")
time.sleep(4)
restaurants_data = []
for page in range(200):
    restaurants = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='biGQs _P fiohW alXOW NwcxK GzNcM ytVPx UTQMg RnEEZ ngXxk']/a")))
    for restaurant in restaurants:
        restaurant_url = restaurant.get_attribute('href')
        restaurants_data.append((restaurant_url))
    try:
        next_button = driver.find_element(By.XPATH, "//div[@class='xkSty']/div/a")
        next_button.click()
    except NoSuchElementException:
        break
    time.sleep(5)
print('URLs scraped, now adding addresses to csv file')
for restaurant_url in restaurants_data:
    driver.get(restaurant_url)
    time.sleep(1)
    name = WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='acKDw w O']/h1"))).text
    address_element = driver.find_element(By.XPATH, "//span[@class='MZcyw']/following-sibling::a")
    address = address_element.text.strip()
    address_parts = address.split(',')
    postcode_match = re.search(r'\b\d{4}\b', address[::-1])
    if postcode_match:
        postcode = postcode_match.group(0)[::-1] 
    else:
        postcode = "No postcode provided"
    try:
        number_element = driver.find_element(By.XPATH, '//span[@class="AYHFM"]/a')
        number_text = number_element.text.strip()
        if "Improve this listing" in number_text:
            number = "No number provided"
        else:
            number = number_text
    except NoSuchElementException:
        number = "No number provided"
    try:
        website = driver.find_element(By.XPATH,'''//a[@class='YnKZo Ci Wc _S C AYHFM']''').get_attribute('href')   
    except:
        website = "No website provided"    
    try:
            email = driver.find_element(By.XPATH, '//a[contains(@href,"mailto:")]').get_attribute('href')
    except NoSuchElementException:
            email = "No email provided"
    with open('restaurants.csv', 'a', encoding='utf-8') as file:
            file.write(f'"{name}", "{address}", "{postcode}", "{number}", "{website}", "{email}" \n')
file.close()
driver.quit()
print("Scraping done")
