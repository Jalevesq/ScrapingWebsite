from playwright.sync_api import sync_playwright
from undetected_playwright import stealth_sync

import pandas as pd
import time, random, datetime, os

from utils import checkFilePath
from private import file_path_to_save, websiteToScrape, user_agents, temporaryFolder, unfilteredFolder

category_links = []
all_data = []

def openWebsite(p):
    browser = p.chromium.launch(headless=False, slow_mo=50)
    random_user_agent = random.choice(user_agents)
    context = browser.new_context(user_agent=random_user_agent)
    stealth_sync(context)
    page = context.new_page()
    
    page.goto(websiteToScrape)
    page.wait_for_load_state("networkidle")
    return page, browser


def scrollPage(divs_inside_container):
    div = divs_inside_container[-1]
    div.scroll_into_view_if_needed()
    time.sleep(4)
    div = divs_inside_container[-5]
    div.scroll_into_view_if_needed()
    time.sleep(1)


def getImgUrl(div, page):
    url = "No URL found"
    desired_img_size = '360w'
    div_img = div.query_selector('img.product--image')
    if div_img:
        srcset = div_img.get_attribute('data-srcset')
    sources = srcset.split(', ')
    for source in sources:
        if desired_img_size in source:
            parts = source.split(' ')
            url = parts[0]
            url = "https:" + url
            break
    return url
def getAllProduct(page):
    total_product = 0
    current_product = 0
    while 1:
        page_data = []
        infinite_scroll_container = page.query_selector('#infiniteScrollContainer')
        divs_inside_container = infinite_scroll_container.query_selector_all('> div')

        scrollPage(divs_inside_container)
        if (total_product == len(divs_inside_container)):
            print("Rescroll !")
            continue
        
        total_product = len(divs_inside_container)
        while current_product < total_product:
            div = divs_inside_container[current_product]

            span_money = div.query_selector('span.money')
            p_title = div.query_selector('p.grid-product__title')
            img = getImgUrl(div, page)
            
            # Extract the content of the elements
            price = span_money.text_content() if span_money else "N/A"
            title = p_title.text_content() if p_title else "N/A"
            img = img.get_attribute('src') if img else "N/A"

            page_data.append((['N/A', title,'N/A',price, img]))
            all_data.append(['N/A', title,'N/A',price, img])
            current_product = current_product + 1
        save_product(page_data, file_path_to_save + temporaryFolder + "all_product.csv")


def save_product(data, filename):
    if os.path.isfile(filename):
        df = pd.DataFrame(data, columns=['Vendor', 'Title', 'Url', 'Price', 'Image'])
        df.to_csv(filename, mode='a', header=False, index=False)
        print(f"Data has been appended to {filename}")
    else:
        df = pd.DataFrame(data, columns=['Vendor', 'Title', 'Url', 'Price', 'Image'])
        df.to_csv(filename, index=False)
        print(f"Data has been saved to {filename}")


if __name__ == "__main__":
    if checkFilePath(file_path_to_save) is False:
        print("Please create the folder.")
        exit(1)
    with sync_playwright() as p:
        page, browser = openWebsite(p)
        # time.sleep(10)
        try:
            getAllProduct(page)
        except Exception as e:
            print(f"Unexpected Problem: {e}")
        save_product(all_data, file_path_to_save + unfilteredFolder + 'SugarDaddy_All_Products.csv')
        browser.close()  # Close the browser object


#########################################################
# from playwright.sync_api import sync_playwright
# import pandas as pd
# import time, random, datetime

# from utils import checkFilePath
# from private import file_path_to_save, websiteToScrape, user_agents, temporaryFolder, unfilteredFolder
# category_links = []
# browser = None

# all_data = []
# desired_size = '360w'


# def check_json(response):
#     print({"url": response.url})

# def openWebsite(p):
#     global browser  # Use the global browser variable
#     browser = p.chromium.launch(headless=False, slow_mo=50)
#     random_user_agent = random.choice(user_agents)
#     context = browser.new_context(user_agent=random_user_agent)
#     page = context.new_page()
    
#     # page.on("response", lambda response: check_json(response))
#     page.goto(websiteToScrape)
#     page.wait_for_load_state("networkidle")
#     return page


# def getAllProduct(page):
#     new_div = 0
#     old_div = -1
#     infinite_scroll_container = page.query_selector('#infiniteScrollContainer')
#     while new_div != old_div:
#         old_div = new_div
#         divs_inside_container = infinite_scroll_container.query_selector_all('> div')
        
#         last_div = divs_inside_container[-1]
#         last_div.scroll_into_view_if_needed()
#         time.sleep(3)
#         new_div = len(divs_inside_container)
#         print(new_div)
#         time.sleep(3)
#     for div in divs_inside_container:
#         span_money = div.query_selector('span.money')
#         p_title = div.query_selector('p.grid-product__title')
#         img = div.query_selector('img.product--image')
        
#         # Extract the content of the elements
#         money_content = span_money.text_content() if span_money else "N/A"
#         title_content = p_title.text_content() if p_title else "N/A"
#         img_src = img.get_attribute('src') if img else "N/A"

#         all_data.append(['N/A', title_content, money_content, img_src])


# def save_product(data, filename):
#     # Create a DataFrame from the all_data
#     df = pd.DataFrame(data, columns=['Vendor', 'Title', 'Price', 'Image'])
    
#     # Save the DataFrame to a CSV file
#     df.to_csv(filename)
    
#     # save in this path: /Users/jacob/Desktop/Projet/Python/Scraping/Data/ShackSnack + today's date under format: YYYY-MM-DD
#     print(f"Data has been saved to {filename}")

# if __name__ == "__main__":
#     if checkFilePath(file_path_to_save) is False:
#         print("Please create the folder.")
#         exit(1)
#     with sync_playwright() as p:
#         page = openWebsite(p)
#         # time.sleep(10)
#         try:
#             getAllProduct(page)
#         except Exception as e:
#             print(f"Unexpected Problem: {e}")
#         print("Going in save_product")
#         save_product(all_data, file_path_to_save + temporaryFolder + 'SugarDaddy_All_Products.csv')
#         browser.close()  # Close the browser object