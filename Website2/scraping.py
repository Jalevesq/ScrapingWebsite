from playwright.sync_api import sync_playwright
import pandas as pd
import time, random, datetime, os
from private import websiteToScrape, file_path_to_save, user_agents
from myDecorator import check_information_decorator


def openWebsite(p):
    browser = p.chromium.launch(headless=True, slow_mo=50)
    random_user_agent = random.choice(user_agents)
    context = browser.new_context(user_agent=random_user_agent)
    page = context.new_page()
    page.goto(websiteToScrape)
    page.wait_for_load_state("networkidle")
    return page, browser


def getCategory(page):
    category_links = []
    ul_element = page.wait_for_selector('#nt_menu_id')        
    li_elements = ul_element.query_selector_all('li')
    for li_element in li_elements:
        a_element = li_element.query_selector('a')
        if a_element:
            href = a_element.get_attribute('href')
            if href:
                category_links.append(websiteToScrape + href)
    return category_links


def getImgUrl(div, page):
    div_img = div.query_selector('.product-image')  # Get the div with lazy loading classes
    url = "No URL found"
    bgset_value = ""
    desired_img_size = '360w'
    # Wait for the 'lazyloadt4sed' class to be added to the image
    try:
        div_img.wait_for_selector('.lazyloadt4sed', state='attached', timeout=10000)
    except:
        return url
    pr_lazy_img = div_img.query_selector('.pr_lazy_img')  # Get the pr_lazy_img inside div_img
    if pr_lazy_img:
        # Once the image is loaded, extract the data-bgset attribute
        bgset_value = pr_lazy_img.get_attribute('data-bgset')
    sources = bgset_value.split(', ')
    for source in sources:
        if desired_img_size in source:
            parts = source.split(' ')
            url = parts[0]
            url = "https:" + url
            break
    return url


def initNewPage(page):
    time.sleep(2)
    page.evaluate(f'window.scrollBy(0, 0);')
    page.reload()
    viewport_height = page.evaluate('window.innerHeight')
    page.evaluate(f'window.scrollBy(0, {viewport_height} / 2);')


def waitForPage(page):
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception as e:
        print(f"Wait_for_load_state error: {e}")
        return False
    return True


def next_page(page_data, category_data, link):
    ul = page.query_selector("#shopify-section-collection_page > div.products-footer.tc.mt__40.mb__60.use_pagination_default > nav > ul")
    try:
        ul.wait_for_selector("li:has(a.next.page-numbers)", timeout=5000)
        li = ul.query_selector("li:has(a.next.page-numbers)")
        save_product(page_data, file_path_to_save + "temp/" + link.split('/')[-1] + ".csv") # Recovery save in decorator?
        category_data.extend(page_data)
        li.click()
    except Exception:
        print(f"[Exception Hidden] End of category: {link}")
        return category_data, False
    return category_data, True

def getProductUrl(div):
    url = div.query_selector('a.db')
    if url:
        url = url.get_attribute('href')
        url = websiteToScrape + url
    else:
        url = "No Product URL Found"
    return url

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
            print(info)
            page_data.append([info['vendor'], info['title'], info['url'], info['price'], info['img']])
        category_data, isNextPage = next_page(page_data, category_data, link)
        if isNextPage is False:
            break
    return category_data


def getAllProduct(page, category_links):
    all_data = []
    # Demander si je veux scrape [link] ou passer au prochain ?
    for link in category_links:
        category_data = iterateCategory(link, page)
        all_data.extend(category_data)
        save_product(category_data, file_path_to_save + link.split('/')[-1] + ".csv")
    save_product(all_data, file_path_to_save + "all_test.csv")


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
