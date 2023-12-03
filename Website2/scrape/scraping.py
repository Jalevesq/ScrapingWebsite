from playwright.sync_api import sync_playwright
import pandas as pd
import time, os

from private import file_path_to_save, temporaryFolder, unfilteredFolder
from myDecorator import check_information_decorator
from initPage import openWebsite, initNewPage
from utils import waitForPage, checkFilePath
from getter import getCategory, getImgUrl, getProductUrl

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


def next_page(page_data, category_data, link):
    save_product(page_data, file_path_to_save + temporaryFolder + link.split('/')[-1] + ".csv") # Recovery save in decorator?
    category_data.extend(page_data)
    ul = page.query_selector("#shopify-section-collection_page > div.products-footer.tc.mt__40.mb__60.use_pagination_default > nav > ul")
    try:
        ul.wait_for_selector("li:has(a.next.page-numbers)", timeout=5000)
        li = ul.query_selector("li:has(a.next.page-numbers)")
        li.click()
    except Exception:
        print(f"[Exception Hidden] End of category: {link}")
        return category_data, False
    return category_data, True


@check_information_decorator
def getInfo(div, page):
    current_y = page.evaluate('window.scrollY')
    div_top = div.bounding_box()['y']
    if div_top != current_y:
        page.evaluate(f'window.scroll({current_y}, {div_top});')
    vendor = div.query_selector('.product-brand a').inner_text()
    title = div.query_selector('.product-title a').inner_text()
    price = div.query_selector('span.price').inner_text().strip() # .strip: remove newline at the end
    url = getProductUrl(div)
    img = getImgUrl(div, page)
    return {
        'vendor': vendor,
        'title': title,
        'url': url,
        'price': price,
        'img': img,
    }


def iterateCategory(link, page):
    page.goto(link)
    category_data = []
    while (1):
        initNewPage(page)
        if waitForPage(page) is False: # Will reload the page until it load, Bad practice because never stop if problem ?
            continue 
        div_collections = page.query_selector('div#shopify-section-collection_page')
        divs_with_data_page = div_collections.query_selector_all('div[data-page]')
        page_data = []
        for div in divs_with_data_page:
            info = getInfo(div, page)
            page_data.append([info['vendor'], info['title'], info['url'], info['price'], info['img']])
        category_data, isNextPage = next_page(page_data, category_data, link)
        if isNextPage is False:
            break
    return category_data


def getAllProduct(page, category_links):
    all_data = []
    # Demander si je veux scrape [link] ou passer au prochain ?
    for link in category_links:
        user = input(f"Do you want to scrape: {link}")
        if user == 'n':
            continue
        category_data = iterateCategory(link, page)
        all_data.extend(category_data)
        print(category_data)
        save_product(category_data, file_path_to_save + unfilteredFolder + link.split('/')[-1] + ".csv")
    save_product(all_data, file_path_to_save + unfilteredFolder + "all_product.csv")


if __name__ == "__main__":
    if not checkFilePath(file_path_to_save):
        print(f"Please make sure that the folder you have set in private.py exists.")
        exit(1)
    with sync_playwright() as p:
        page, browser = openWebsite(p)
        time.sleep(3)
        category_links = getCategory(page)
        time.sleep(2)
        try:
            getAllProduct(page, category_links)
        except Exception as e:
            print(f"Unexpected Problem: {e}")
        browser.close()  # Close the browser object
