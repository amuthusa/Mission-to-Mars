#import dependency like splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path' : '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

#visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

#add a delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

#get the html 
html = browser.html
#parse the html context
soup = BeautifulSoup(html, 'html.parser')
#get one slide_element using ul class item_list and li class slide
slide_element = soup.select_one('ul.item_list li.slide')
slide_element

#get the title of the article using dev with class content_title
news_title = slide_element.find("div", class_="content_title").get_text()
news_title

#get the news article's summary
news_summary = slide_element.find("div", class_="article_teaser_body").get_text()
news_summary

# ### Featured Images

#vist url
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

#get by id for full_image
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

#find the more info button and click that
browser.is_element_present_by_text('more_info', wait_time=1)
more_info_elem = browser.find_link_by_partial_text('more info')
more_info_elem.click()

#parse the resulting html page
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

#find relative image url
img_url_rel = soup.select_one("figure.lede a img").get("src")
img_url_rel

#create url using base and extracted image url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns = ['description', 'value']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()