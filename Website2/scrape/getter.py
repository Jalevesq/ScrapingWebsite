from private import websiteToScrape

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

def getProductUrl(div):
    url = div.query_selector('a.db')
    if url:
        url = url.get_attribute('href')
        url = websiteToScrape + url
    else:
        url = "No Product URL Found"
    return url