import requests
from bs4 import BeautifulSoup as bs
import time, timeit

def shopify_keywords():
    print("\nSite options (feel free to try other shopify sites):\ncncpts\nbdgastore\nus.bape\n")
    site = input("Please choose a site: ")

    keywords = input("Please enter keywords (seperate by commas): ").lower().split()
    print('Searching for products with the following keywords: {}'.format(keywords))

    session = requests.session()
    url = "https://{}.com/sitemap_products_1.xml?".format(site)
    response = session.get(url)
    soup = bs(response.content, 'html.parser')

    all_found_urls = []
    for urls_found in soup.find_all("url"):
        for keyword_search in urls_found.find_all("image:image"):
            if all(i in keyword_search.find("image:title").text.lower() for i in keywords):
                print("Matched keywords! -> " + keyword_search.find("image:title").text)
                found_url = "Found URL: " + urls_found.find("loc").text
                all_found_urls.append(urls_found.find("loc").text + ".xml")
                print(found_url)

    for found_products in all_found_urls:
        response = session.get(found_products)
        soup = bs(response.content, 'html.parser')
        product_name = soup.find('hash').find('title').text
        product_tags = soup.find('tags').text
        print('-'*80, '\nProduct name: {}. Tags: {}\n'.format(product_name, product_tags), '-'*80)

        for variants in soup.find_all('variant'):
            size_id = variants.find('id', {'type': 'integer'}).text
            shoe_size = variants.find('title').text
            shoe_stock = variants.find('inventory-quantity', {"type": "integer"}).text
            print("Size: {}. ID: {}. Stock: {}".format(shoe_size, size_id, shoe_stock))
            if int(shoe_stock) >= 1:
                print("ATC LINK: https://{}.com/cart/{}:1".format(site, size_id))

# runs the script BRO
if __name__ == '__main__':
    shopify_keywords()





