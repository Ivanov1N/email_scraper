from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re


# Creating a deque for the scaned pages of the input address and also two sets for the collected emails and scraped pages
user_url = str(input('Please, enter URL to scrape for mails: '))
urls = deque([user_url])
scraped_urls = set()
emails = set()
count = 0

# Utilizing the parsing process
try:
    while len(urls):
        count += 1
        if count == 100: #The number of pages to search can be modified.
            break
        url = urls.popleft()
        scraped_urls.add(url)
        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)

        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        print ('[%d] Processing %s' % (count, url))
        
        # Get request and handle anticipated errors
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        # Collecting only strings with an email pattern
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)

        # Setting up BeautifulSoup and scraping
        soup = BeautifulSoup(response.text, features="lxml")

        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)

# An option to cancel the search
except KeyboardInterrupt:
    print ('[-] Closing!')

# Show only the collected strings with length on an email
for mail in emails:
    if len(mail) > 8:
        print (mail)
            









            
        
