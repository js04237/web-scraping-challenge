# web-scraping-challenge

The application does the following:
    
    1. Scrapes data from the following websites:
        
        https://mars.nasa.gov/news/
        https://mars.nasa.gov/
        https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
        https://space-facts.com/mars/
        https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

        The scraping in done with splinter, beautifulsoup4, and chromewebdriver.

    2. Stores the data in a Mongo database.

        The data is stored using PyMongo.

    3. Renders the data in a new website.

        The website is rendering using flask, jinja, and html.