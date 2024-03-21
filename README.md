# restaurant-tripadvisor-scraper

do  pip install -r requirements.txt

run using restaurant.py

to change location to scrape chnage url in 
```
driver.get("https://www.tripadvisor.co.nz/Restaurants-g255118-Christchurch_Canterbury_Region_South_Island.html")
```
will get all restaurants from url and scrape name,address, postcode, number,website and email, import to cvs and print


if script crashes on opening it first, re run it as it has now been asked to do CAPTCHA until script works 
will not ask for CAPTCHA on first try

NOTE:
code only works with trip advisor and it not able to scrape all restaurants from url given, gives timeout error. dont know how to fix it.
i have been able to scrape 1342 out of 3248, so it can scrape a decent ammount.
