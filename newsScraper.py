from bs4 import BeautifulSoup
import requests

requests.adapters.DEFAULT_RETRIES = 1

def urlHelper (url, debug = False):
    try:
        if str(requests.get(url).status_code)[0] == "2":
            return len(url[8:].split("/"))
        else:
            return 0
    except requests.exceptions.ConnectionError as e:
        if debug == 1:
            print(e)
        return 0
    except requests.exceptions.MissingSchema as e:
        if debug == 1:
            print(e)
        return 0

def urlFilter(url, debug = False):
    blacklist = ['info-pages']
    for term in blacklist:
        if term in url:
            return False
    return True

def processURL (url):
    print('opening link %s'%(url))
    resp = requests.get(url, headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'})
    if str(resp.status_code)[0] != "2":
        print("Encountered some kind of something: %s"%(resp.text))
    articleList = riplinks(resp.text, url)
    print(articleList)
    return articleList

def riplinks (html, url):
    articleList = []
    print('ripping links')
    soup = BeautifulSoup(html, features="html.parser")
    for a in soup.find_all('a', href=True):
        if url+a['href'] not in articleList and urlHelper(url+a['href'], debug=True) > 3:
            if urlFilter(url+a['href']):
                articleList.append(url+a['href'])
    print('%i found.'%(len(articleList)))
    return articleList

def doall (site):
	print('starting')
	result = processURL(site)
	return result

#forTest doall("https://www.reuters.com")