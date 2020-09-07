# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

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

    # Transform the table into a dataframe
    mars_fact_table = mars_df.to_html('mars_facts.html', header=False, index=False)

    # Put the Mars / Earth comparison data into its own table
    mars_earth_df = tables[1]

    # Transform the table into a dataframe
    mars_earth_table = mars_earth_df.to_html('mars_earth_facts.html', index=False)

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
                                    'img_url': soup.find(text='Original').parent['href']})

    hemisphere_dict = {"hemispheres": hemisphere_image_urls}

    # Close the browser after scraping
    browser.quit()

    scraped_data = [title, text, featured_image_url, hemisphere_dict]

    # Return results
    return scraped_data


