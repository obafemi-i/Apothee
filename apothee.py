from playwright.sync_api import sync_playwright, TimeoutError as playWrightTimeoutError
from requests_html import HTMLSession
import pandas as pd


s = HTMLSession()
l=[]

def get_link():
    url = 'https://apotheekdedeyne.be/pharmareserve/'
    req = s.get(url, headers={'User-Agent':'Mozilla/5.0'})

    links = req.html.find('ul.links li a')
    linkd = [g.attrs['href'] for g in links]

    linkd.pop()
    away = ['https://apotheekdedeyne.be/pharmareserve/product/search/?category=6-thuiszorg-en-ehbo','https://apotheekdedeyne.be/pharmareserve/product/search/?category=5-natuur-geneeskunde', 'https://apotheekdedeyne.be/pharmareserve/product/search/?category=4-50', 'https://apotheekdedeyne.be/pharmareserve/product/search/?category=3-zwangerschap-en-kinderen', 'https://apotheekdedeyne.be/pharmareserve/product/search/?category=2-afslanken-voeding-en-vitamines','https://apotheekdedeyne.be/pharmareserve/product/search/?category=1-schoonheid-verzorging-en-hygine','https://apotheekdedeyne.be/pharmareserve/product/search/?category=307-geneesmiddelen', 'https://apotheekdedeyne.be/pharmareserve/product/apotheek_specials', 'https://apotheekdedeyne.be/pharmareserve/product/apotheek_specials/?category=4', 'https://apotheekdedeyne.be/pharmareserve/product/apotheek_specials/?category=1' ]

    anew =[ele for ele in linkd if ele not in away]
    return anew

sites = get_link()

def main(url_link):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()

        page = context.new_page()

        page.goto(url_link)
        html = page.url
        req = s.get(html, headers={'User-Agent':'Mozilla/5.0'})
        category = req.html.find('div.category_breadcrumb', first=True).text.replace('>','').strip().split('  ')[0]
        sub = req.html.find('div.category_breadcrumb', first=True).text.replace('>','').strip().split('  ')[1]

        next = req.html.find('div.products-img a')
        nex = [g.attrs['href'] for g in next]
        new = [value for value in nex if value != "#"]
        for e in new:
            prod = e
            requ = s.get(e, headers={'User-Agent':'Mozilla/5.0'})
            price = requ.html.find('span.price-new', first=True).text.replace('€','').strip()
            try:
                cnk = requ.html.find('div.model', first=True).text.split(' ')[1]
                merken = requ.html.find('div.model a', first=True).text
            except AttributeError:
                cnk = requ.html.find('div.clearfix', first=True).text
                merken = 'N/A'
            item = requ.html.find('h2#prod_title', first=True).text
            try:
                thumb = requ.html.find('a.popup img', first=True).attrs['src']
            except AttributeError:
                thumb = 'N/A'
            try:
                full_img = requ.html.find('a.popup', first=True).attrs['href']
            except AttributeError:
                full_img = 'N/A'
            try:
                sw = req.html.find('div#detail_refund div.clearfix')[0].text
                p = req.html.find('div#detail_refund div.clearfix')[1].text
                rem = [sw,p]
            except AttributeError:
                rem = 'N/A'
            except IndexError:
                rem = 'N/A'

            try:
                geb =req.html.find('div#detail_usage', first=True).text
            except AttributeError:
                geb = 'N/A'

            try:
                awr = req.html.find('div#detail_indication', first=True).text
            except AttributeError:
                awr = 'N/A'

            try:
                if (req.html.find('span.label', first=True).text.strip()) == 'Voorschrift Verplicht':
                    var = 'True'
            except AttributeError:
                var = 'False'

            l_dict = {
                'Category':category,
                'Subcategory':sub,
                'Item_Name':item,
                'Image_Thumbnail':thumb,
                'Full_Image':full_img,
                'Price':price,
                'CNK':cnk,
                'Merken':merken,
                'Product_Link':prod,
                'Remgeld':rem,
                'Gebruik' :geb,
                'Aanwijzingen':awr,
                'Voorschrift Verplicht' : var
            }

            l.append(l_dict)
            print(f'{item} extracted')

        while True:
            try:
                page.get_by_role("link", name=">").click()
                html = page.url
                req = s.get(html, headers={'User-Agent':'Mozilla/5.0'})
                category = req.html.find('div.category_breadcrumb', first=True).text.replace('>','').strip().split('  ')[0]
                sub = req.html.find('div.category_breadcrumb', first=True).text.replace('>','').strip().split('  ')[1]

                next = req.html.find('div.products-img a')
                nex = [g.attrs['href'] for g in next]
                new = [value for value in nex if value != "#"]
                for e in new:
                    prod = e
                    requ = s.get(e, headers={'User-Agent':'Mozilla/5.0'})
                    price = requ.html.find('span.price-new', first=True).text.replace('€','').strip()
                    try:
                        cnk = requ.html.find('div.model', first=True).text.split(' ')[1]
                        merken = requ.html.find('div.model a', first=True).text
                    except AttributeError:
                        cnk = requ.html.find('div.clearfix', first=True).text
                        merken = 'N/A'
                    item = requ.html.find('h2#prod_title', first=True).text
                    try:
                        thumb = requ.html.find('a.popup img', first=True).attrs['src']
                    except AttributeError:
                        thumb = 'N/A'
                    try:
                        full_img = requ.html.find('a.popup', first=True).attrs['href']
                    except AttributeError:
                        full_img = 'N/A'
                    try:
                        sw = req.html.find('div#detail_refund div.clearfix')[0].text
                        p = req.html.find('div#detail_refund div.clearfix')[1].text
                        rem = [sw,p]
                    except AttributeError:
                        rem = 'N/A'
                    except IndexError:
                        rem = 'N/A'

                    try:
                        geb =req.html.find('div#detail_usage', first=True).text
                    except AttributeError:
                        geb = 'N/A'

                    try:
                        awr = req.html.find('div#detail_indication', first=True).text
                    except AttributeError:
                        awr = 'N/A'

                    try:
                        if (req.html.find('span.label', first=True).text.strip()) == 'Voorschrift Verplicht':
                            var = 'True'
                    except AttributeError:
                        var = 'False'

                    l_dict = {
                        'Category':category,
                        'Subcategory':sub,
                        'Item_Name':item,
                        'Image_Thumbnail':thumb,
                        'Full_Image':full_img,
                        'Price':price,
                        'CNK':cnk,
                        'Merken':merken,
                        'Product_Link':prod,
                        'Remgeld':rem,
                        'Gebruik' :geb,
                        'Aanwijzingen':awr,
                        'Voorschrift Verplicht' : var
                    }

                    l.append(l_dict)
                    print(f'{item} extracted')

            except playWrightTimeoutError:
                break
        # ---------------------
        context.close()
        browser.close()



for site in sites:
    main(site)
    
df = pd.DataFrame(l)
df.to_csv('Apothee.csv', index=False)
