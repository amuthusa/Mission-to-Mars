#import dependency like splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path' : '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    #get news title and news summary
    news_title, news_summary = mars_news(browser)
    #create a dictionary with scraped data
    data = {
        "news_title": news_title,
        "news_summary": news_summary,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data

def mars_news (browser):
    #visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #add a delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #get the html 
    html = browser.html
    #parse the html context
    soup = BeautifulSoup(html, 'html.parser')
    try :
        #get one slide_element using ul class item_list and li class slide
        slide_element = soup.select_one('ul.item_list li.slide')

        #get the title of the article using dev with class content_title
        news_title = slide_element.find("div", class_="content_title").get_text()

        #get the news article's summary
        news_summary = slide_element.find("div", class_="article_teaser_body").get_text()
        
        return news_title, news_summary
    except AttributeError:
        return None, None

# ### Featured Images

def featured_image(browser):
    #vist url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #get by id for full_image
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    #find the more info button and click that
    browser.is_element_present_by_text('more_info', wait_time=1)
    #more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    #parse the resulting html page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    try:
        #find relative image url
        img_url_rel = soup.select_one("figure.lede a img").get("src")

        #create url using base and extracted image url
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
        return img_url
    except AttributeError:
        return None


def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
        df.columns = ['description', 'value']
        df.set_index('description', inplace=True)
        return df.to_html()
    except BaseException:
        return None


if __name__ == "__main__":
    #if running as script print the scraped data
    print (scrape_all())