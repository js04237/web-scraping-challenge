# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json

# Chrome webdriver setup
def init_browser():
    return Browser("chrome", 'chromedriver.exe', headless=True)

def scrape_data():

    browser = init_browser()

    # Scrape the NASA Mars News page
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    latest = soup.find('div', class_='image_and_description_container')

    # Get the latest article title and description
    for article in latest:
        title = {"latest_article_title" : latest.find('h3').text}
        text = {"latest_article_text" : latest.find('div', class_='article_teaser_body').text}

    # Scrape the NASA Mars Weather
     
    url = 'https://mars.nasa.gov/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hightemp = {"high": (soup.find_all("div", {"class":"col high"})[0]).find('div', {'class': 'val'}).text.strip('\n')}
    lowtemp = {"low": (soup.find_all("div", {"class":"col low"})[0]).find('div', {'class': 'val'}).text.strip('\n')}

    # Scrape the NASA Jet Propulation Lab website to get the latest featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Click on the links to navigate to the desired page
    try:
        browser.links.find_by_partial_text('FULL IMAGE').click()
        try:
            browser.links.find_by_partial_text('more info').click()
        except:
            print('Button 2 Not Found')
    except:
        print('Button Not Found')

    # Find the featured image url from the soup
    image = soup.find('a', class_='fancybox')["data-fancybox-href"]
    featured_image_url = {"featured_image_url" : "https://www.jpl.nasa.gov" + image}

    # Scrape the Mars page of the Space Facts website
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the facts from the soup
    results = soup.find("section", id="secondary")

    # Read the data into a Pandas table
    tables = pd.read_html(url)

    # Put Mars facts into its own table
    mars_df = tables[0]

    # Put the Mars / Earth comparison data into its own table
    mars_earth_df = tables[1]

    # Scrape the website for high res images of each hemisphere
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Get a list of the links to images of each hemisphere
    hemisphere_link_list = []

    for link in soup.find_all('a', class_="itemLink product-item"):
        if (link.get('href')) not in hemisphere_link_list:
            hemisphere_link_list.append(link.get('href'))

    # Concatenate the hemisphere link list to the url root to create full urls
    url_list = []

    for i in range(len(hemisphere_link_list)):
        url_list.append("https://astrogeology.usgs.gov" + hemisphere_link_list[i])

    # Visit each url in the url_list to get a link to the high quality image of each hemisphere and create a list to hold the links and the hemisphere name
    hemisphere_image_urls = []

    for url in url_list:
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemisphere_image_urls.append({'title': soup.find('h2', class_="title").text[:-9],
                                    'img_url': soup.find(text='Sample').parent['href']})

    hemisphere_dict = {"hemispheres": hemisphere_image_urls}

    # Close the browser after scraping
    browser.quit()

    # Change the mars fact table from a a dataframe format to a json format so it can be laoded into mongo
    df_to_table = []
    df_to_table = json.loads(mars_df.T.to_json())

    # Load the data into mongo
    scraped_data = [title, text, featured_image_url, hemisphere_dict, df_to_table, hightemp, lowtemp]

    # Return results
    return scraped_data


