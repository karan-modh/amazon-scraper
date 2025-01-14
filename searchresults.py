from requests.api import head
from selectorlib import Extractor
import requests 
import json 
from time import sleep


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('search_results.yml')

def scrape(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.in/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url=url, headers=headers)
    # r = requests.get(url, headers=headers, proxies=proxies)
    
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)

# product_data = []
amazon_search_link = "https://www.amazon.in/s?k="
key = input("\nEnter your search word:\n")
amazon_search_link += key

with open('search_results_output.jsonl','w') as outfile:    
    data = scrape(amazon_search_link) 
    if data:
        for product in data['products']:
            product['search_url'] = amazon_search_link
            print("Saving Product: %s"%product['title'])
            json_object = json.dumps(product, indent=4)
            outfile.write(json_object)
            sleep(1)
    