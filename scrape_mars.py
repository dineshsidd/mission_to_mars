#!/usr/bin/env python
# coding: utf-8

# In[147]:
def scrape():
        
    from bs4 import BeautifulSoup
    from splinter import Browser
    # Webdriver to navigate between pages
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import requests
    import time
    # Regex
    import re
    import pandas as pd
    #To Get the Hostname from the URL
    from urllib.parse import urlparse

    scrape_results = {}
    # In[129]:
    url_news = "https://mars.nasa.gov/news/"
    # In[130]:
    response = requests.get(url_news)
    soup_news = BeautifulSoup(response.text,"html.parser")
    # ### NASA Mars News
    # In[131]:
    news_header = soup_news.find_all("div", class_="content_title")
    news_title = news_header[0].text.strip()
    news_body = soup_news.find_all("div", class_= "rollover_description_inner")
    news_detail = news_body[0].text.strip()
    news={}
    news["title"] = news_title
    news["detail"] = news_detail
    scrape_results["news"] = news

    # ### JPL Mars Space Images - Featured Image
    # In[158]:
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    driver.find_element_by_link_text('FULL IMAGE').click()
    time.sleep(2)
    driver.find_element_by_link_text('more info').click()
    driver.find_element_by_xpath("//img[@class='main_image']").click()
    # In[135]:
    featured_image = driver.current_url
    scrape_results["featured_image"] = featured_image
    # ### Mars Hemispheres
    # In[148]:
    driver = webdriver.Chrome('chromedriver.exe')
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemi_urls = []
    hemi_texts = []
    for x in range (1 ,5):
        driver.get(hemi_url)
        time.sleep(4)
        images = driver.find_element_by_xpath(f"//div[@class='collapsible results']/div[{x}]/a/img").click()
        response = requests.get(driver.current_url)
        hemi_soup = BeautifulSoup(response.text , "html.parser")
        img_wide = hemi_soup.find_all("img", class_="wide-image")
        final_url = "https://" + urlparse(driver.current_url).hostname + img_wide[0]["src"]
        hemi_urls.append( final_url)
        hemi_texts.append(hemi_soup.find("title").text.replace(" | USGS Astrogeology Science Center",""))
    # In[149]:
    scrape_results["hemi_urls"] = hemi_urls
    scrape_results["hemi_texts"] = hemi_texts

    # ### Mars Weather

    # In[150]:

    weather_url = "https://twitter.com/marswxreport?lang=en"
    weather_response = requests.get(weather_url)
    weather_soup = BeautifulSoup(weather_response.text , "html.parser")
    # In[151]:

    weather_array = weather_soup.findAll(text =re.compile('InSight'),limit=1 )[0].split("\n")
    for row in weather_array:
        print(row)
    scrape_results["weather"] = weather_array
    # ### Mars Facts

    # In[159]:
    facts_url = "http://space-facts.com/mars/"
    facts = pd.read_html(facts_url)
    facts[0].columns =["Fact","Value"]
    # In[160]:
    mars_facts = facts[0]
    scrape_results["facts"] = mars_facts
    # In[ ]:
    return scrape_results



