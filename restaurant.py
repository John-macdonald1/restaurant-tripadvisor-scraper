from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

with open('restaurants.csv', 'w', encoding='utf-8') as file:
    file.write('Restaurant Name, Address, Contact Number, Website, Email \n')

driver = webdriver.Chrome()
driver.get("https://www.tripadvisor.co.nz/Restaurants-g1811027-Auckland_North_Island.html")
time.sleep(4)

restaurants_data = []

for page in range(1):
    restaurants = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='biGQs _P fiohW alXOW NwcxK GzNcM ytVPx UTQMg RnEEZ ngXxk']/a")))
    for restaurant in restaurants:
        restaurant_url = restaurant.get_attribute('href')
        restaurants_data.append((restaurant_url))

    next_button = driver.find_element(By.XPATH, "//div[@class='xkSty']/div/a")
    if not next_button.is_enabled():
        break
    next_button.click()
    time.sleep(5)

print('URLs scraped, now adding addresses to csv file')

for restaurant_url in restaurants_data:
    driver.get(restaurant_url)
    time.sleep(5)
    address_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='MZcyw']/following-sibling::a")))
    name = driver.find_element(By.XPATH, "//div[@class='acKDw w O']/h1").text
    number = driver.find_element(By.XPATH,'''//span[@class='AYHFM']/a''').text
    website = driver.find_element(By.XPATH,'''//a[@class='YnKZo Ci Wc _S C AYHFM']''').get_attribute('href')
    address = address_element.text.strip()
    try:
            email = driver.find_element(By.XPATH, '//a[contains(@href,"mailto:")]').get_attribute('href')
    except NoSuchElementException:
            email = "No email provided"
    with open('restaurants.csv', 'a', encoding='utf-8') as file:
            file.write(f'"{name}", "{address}", "{number}", "{website}", "{email}" \n')

driver.quit()
print("Scraping done")