import requests  
from lxml import html  
import sys  
import urlparse

response = requests.get('https://www.futurelearn.com/courses/italian-for-literature?lr=1') ## replace with the website you want

parsed_body = html.fromstring(response.text)

# Grab links to all images
images = parsed_body.xpath('//img/@src')  
if not images:  
    sys.exit("Found No Images")

# Convert any relative urls to absolute urls
images = [urlparse.urljoin(response.url, url) for url in images]  
print 'Found %s images' % len(images)

# Only download first x 10
for url in images[0:10]:## 100 will scrape 100 pictures
    r = requests.get(url)
    f = open('pics2/%s' % url.split('/')[-1], 'w') ## add the folder name

    f.write(r.content)
    f.close()
