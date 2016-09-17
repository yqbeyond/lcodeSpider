import urllib
import urllib2
import httplib
import cookielib
import BeautifulSoup
import codecs
import re
import os

# information
OnlineJudges = {
        "poj":{
            "url": "http://poj.org",
            "user_id": "spider", # enter your user id here
            "passwd": "123456" # passwd here
            },
        "hdu":{
            "url": "http://www.acm.hdu.edu.cn",
            "user_id": "spider", # enter your user id here
            "passwd": "123456" # passwd here
            },
        "zoj":{
            "url": "http://acm.zoj.edu.cn",
            "user_id": "spider", # enter your user id here
            "passwd": "123456" # passwd here
            }
        }

# escapses
escapes = {}
escapes['&lt;'] = "<"
escapes['&#60;'] = "<"
escapes['&gt;'] = ">"
escapes['&#62;'] = ">"
escapes['&#38;'] = "&"
escapes['&nbsp;'] = " "
escapes['&#166;'] = "|"
escapes['&brvbar;'] = "|"
escapes['&#34;'] = '"'

# file type extension accodring to compiler
extension_type = {}
extension_type['G++'] = '.cpp'
extension_type['GCC'] = '.c'
extension_type['Java'] = '.java'
extension_type['C++'] = '.cpp'

if __name__ == '__main__':
    # POJ
    poj_dir = "poj"
    try:
        os.mkdir(poj_dir)
    except:
        pass

    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "",
            "Host":"poj.org",
            "Pragma":"no-cache",
            "Referer": "http://poj.org/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"
            }
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    postData = {
            'user_id1': OnlineJudges['poj']['user_id'],
            'password1': OnlineJudges['poj']['passwd']
            }
    postData = urllib.urlencode(postData)
    url = OnlineJudges["poj"]["url"] + "/login"
    request = urllib2.Request(url, postData)
    response = urllib2.urlopen(request)
    
    url = OnlineJudges["poj"]["url"] + "/status?result=0&user_id=" + OnlineJudges["poj"]["user_id"]
    
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    soup = BeautifulSoup.BeautifulSoup(html)
    tables = soup.find('table', attrs = {'class': 'a'})
    items = tables.contents[1:]
    for item in items:
        if type(item) != BeautifulSoup.Tag:
            items.remove(item)         
    
    while tables:
        last_item = items[-1]
        tds = last_item.findAll('td')
        top = tds[0].contents[0]
        url = "http://poj.org/status?user_id="+OnlineJudges["poj"]["user_id"] + "&result=0&top=" + top
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            html = response.read()
            soup = BeautifulSoup.BeautifulSoup(html)
            tables = soup.find('table', attrs = {'class': 'a'})
            items += tables.contents[1:]
            
            for item in items:
                if type(item) != BeautifulSoup.Tag: 
                    items.remove(item)
        except:
            break
    count = 0
    for item in items:
   #     if type(item) == BeautifulSoup.Tag:
        tds = item.findAll('td')            
        solution_id = tds[0].contents[0]
        problem_id = tds[2].contents[0].contents[0]
        memory = tds[4].contents[0]
        time = tds[5].contents[0]
        compiler = tds[6].contents[0].contents[0]
        item_request_url = OnlineJudges['poj']['url'] + "/showsource?solution_id=" + solution_id
        item_request = urllib2.Request(item_request_url)
        item_response = urllib2.urlopen(item_request)
        item_html = item_response.read()
        item_soup = BeautifulSoup.BeautifulSoup(item_html)
        item_code = item_soup.find("pre")
        src_code = item_code.contents[0]
        if item_code:
            for escape in escapes:
                src_code = src_code.replace(escape, escapes[escape])
            
            info = u"/* Problem ID: " + problem_id + "\n * Author: " + OnlineJudges['poj']['user_id'] + "\n * Memory: " + memory + "\n * Time: " + time + "\n */\n\n"
            src_code = info + src_code
            print 'crawling problem ' + problem_id + '...'
            # print item_request_url
            # print compiler
            src_file_name = poj_dir + "/" + problem_id + extension_type[compiler]
            if not os.path.exists(src_file_name):
                count += 1
                src_code_file = codecs.open(src_file_name, 'wb', 'utf-8')
                src_code_file.write(src_code)
                src_code_file.close()
            else:
                print "file " + src_file_name + " all ready exists"

    print "\nFinished, Download " + str(count) + " files."
