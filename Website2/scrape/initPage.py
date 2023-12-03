import random, time
from private import user_agents, websiteToScrape

def openWebsite(p):
    browser = p.chromium.launch(headless=True, slow_mo=50)
    random_user_agent = random.choice(user_agents)
    context = browser.new_context(user_agent=random_user_agent)
    page = context.new_page()
    page.goto(websiteToScrape)
    page.wait_for_load_state("networkidle")
    return page, browser

def initNewPage(page):
    time.sleep(2)
    page.evaluate(f'window.scrollBy(0, 0);')
    page.reload()
    viewport_height = page.evaluate('window.innerHeight')
    page.evaluate(f'window.scrollBy(0, {viewport_height} / 2);')