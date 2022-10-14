# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set executable path which launches browser

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Assign URl and instruct browser to visitthe mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser

html = browser.html
news_soup = soup(html, 'html.parser')

# Assign slide_elm as variable to look for the <div /> tag and other desecendent <div/> element
# This is our parent element. This means that this element holds all of the other elements within it,
# and we'll reference it when we want to filter search results even further. The . is used for selecting 
# classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag with the class of list_text. 
# CSS works from right to left, such as returning the last item on the list instead of the first. Because of this, 
# when using select_one, the first matching element returned will be a <li />
# element with a class of slide and all nested elements within it.

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# In this line of code, we chained .find onto our previously assigned variable, 
# slide_elem. When we do this, we're saying, "This variable holds a ton of 
# information, so look inside of that information to find this specific data."
# The data we're looking for is the content title, which we've specified by saying, 
# "The specific data is in a <div /> with a class of 'content_title'."

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# IMPORTANT
# There are two methods used to find tags and attributes with BeautifulSoup:

# .find() is used when we want only the first class and attribute we've specified.
# .find_all() is used when we want to retrieve all of the tags and attributes.
# For example, if we were to use .find_all() instead of .find() when pulling the summary, we would retrieve 
# all of the summaries on the page instead of just the first one.

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# Visit the space image site
url = 'https://spaceimages-mars.com/'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# It's important to note that the value of the src will be different every time the page is updated, 
# so we can't simply record the current 
# value—we would only pull that image each time the code is executed, 

# instead of the most recent one.# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

#Use pandas to pull in table from HTML
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


#Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html()

df.to_html()


# In[22]:


browser.quit()

