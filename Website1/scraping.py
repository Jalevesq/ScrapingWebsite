from playwright.sync_api import sync_playwright
from undetected_playwright import stealth_sync

import pandas as pd
import time, random, datetime, os, re

from utils import checkFilePath
from private import file_path_to_save, websiteToScrape, user_agents, temporaryFolder, unfilteredFolder


def openWebsite(p):
    browser = p.chromium.launch(headless=True, slow_mo=1000)
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
    srcset = ""
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


def getUrl(div):
    url = "Url not found"
    div_url = div.query_selector('a.grid-product__image-link')
    if div_url:
        url = div_url.get_attribute('href')
        url = websiteToScrape + url
    return url

def getAllProduct(page, category_links):
    all_data = []
    for category in category_links:
        response = input(f"Do you want to scrape: {category}")
        if response == 'n': # Some page are not real category page.
            continue
        category_data = []
        page.goto(websiteToScrape + category)
        total_product = 0
        current_product = 0
        while 1:
            page_data = []
            infinite_scroll_container = page.query_selector('#infiniteScrollContainer')
            divs_inside_container = infinite_scroll_container.query_selector_all('> div')

            scrollPage(divs_inside_container)
            if (total_product == len(divs_inside_container)):
                print("Did not find new product, end of this category")
                break
            
            total_product = len(divs_inside_container)
            while current_product < total_product:
                div = divs_inside_container[current_product]

                span_money = div.query_selector('span.money')
                p_title = div.query_selector('p.grid-product__title')
                
                # Extract the content of the elements
                price = span_money.text_content() if span_money else "N/A"
                title = p_title.text_content() if p_title else "N/A"
                img = getImgUrl(div, page)
                url =  getUrl(div)

                page_data.append((['N/A', title, url ,price, img]))
                current_product = current_product + 1
            category_data.extend(page_data)
            all_data.extend(page_data)
            save_product(page_data, file_path_to_save + temporaryFolder + category.split('/')[-1] + ".csv")
        save_product(category_data, file_path_to_save + unfilteredFolder + category.split('/')[-1] + ".csv")
    return all_data


def save_product(data, filename):
    if not data:
        print("data is empty. nothing to save.")
        return
    if os.path.isfile(filename):
        df = pd.DataFrame(data, columns=['Vendor', 'Title', 'Url', 'Price', 'Image'])
        df.to_csv(filename, mode='a', header=False, index=False)
        print(f"Data has been appended to {filename}")
    else:
        df = pd.DataFrame(data, columns=['Vendor', 'Title', 'Url', 'Price', 'Image'])
        df.to_csv(filename, index=False)
        print(f"Data has been saved to {filename}")

def getHref(page):
    li_elements = page.query_selector_all('ul.menu-bar__inner > li.menu-bar__item')
    href_list = []
    for li in li_elements:
        a_element = li.query_selector('a.menu-bar__link')
        if a_element:
            href_value = a_element.get_attribute('href')
            href_list.append(href_value)

    if href_list:
        href_list.pop()
        href_list = href_list[2:]
    return href_list


if __name__ == "__main__":
    all_data = []
    if checkFilePath(file_path_to_save) is False:
        print("Please create the folder.")
        exit(1)
    with sync_playwright() as p:
        page, browser = openWebsite(p)
        category_links = getHref(page)
        # time.sleep(10)
        try:
            all_data = getAllProduct(page, category_links)
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