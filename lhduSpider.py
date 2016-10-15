#!-*- coding: utf-8 -*-
"""
HDU
"""

import urllib
import urllib2
import httplib
import cookielib
from bs4 import BeautifulSoup
import codecs
import re
import os
import zlib

# information
OnlineJudges = {
        "hdu":{
            "url": "http://acm.hdu.edu.cn",
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
extension_type['C'] = '.c'
extension_type['C#'] = '.cs'

if __name__ == '__main__':
    # HDU
    hdu_dir = "hdu"
    try:
        os.mkdir(hdu_dir)
    except OSError as e:
        print (e.message)

    headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            "Connection": "keep-alive",
            "Host": "acm.hdu.edu.cn",
            "Cookie": "", # Your cookie here
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"
            }

    cj = cookielib.LWPCookieJar()    
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    # Simulate Login Failed
    """
    postData = {
            'username': OnlineJudges['hdu']['user_id'],
            'userpass': OnlineJudges['hdu']['passwd'],
            'login': 'Sign+In'
            }
    
    url = OnlineJudges["hdu"]["url"] + "/userloginex.php?action=login&cid=0&notice=0"
    postData = urllib.urlencode(postData)
    request = urllib2.Request(url, postData, headers)
    response = urllib2.urlopen(request)
    html = response.read()
    html = zlib.decompress(html, 16 + zlib.MAX_WBITS)
    """ 
    
    url = OnlineJudges["hdu"]["url"] + "/userstatus.php?user=" + OnlineJudges["hdu"]["user_id"]    
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    html = response.read()
    html = zlib.decompress(html, 16 + zlib.MAX_WBITS)
    soup = BeautifulSoup(html, 'lxml')
    p = soup.findAll('p')
    contents = p[2].find('script').contents[0]
    problems_reobj = re.compile('p\(\d{4},\d+,\d+\)')
    solved_lists = [item[2:6] for item in problems_reobj.findall(contents)]

    for problem_id in solved_lists:
        problem_id = str(problem_id)
        
        print 'crawling problem ' + problem_id + ' ...'
        url = OnlineJudges["hdu"]["url"] + "/status.php?user=" + OnlineJudges["hdu"]["user_id"]+"&pid="+ problem_id + "&status=5"
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        
        html = response.read()
        html = zlib.decompress(html, 16 + zlib.MAX_WBITS)
        soup = BeautifulSoup(html, 'lxml')
        tables = soup.table.contents
    
        while '\n' in tables: # remove all '\n'
            tables.remove('\n')

        accpted_lists = tables[3].findAll('tr')[1:]
    
        count = 1
        for item in accpted_lists:
    
            tds = item.findAll('td')
            run_id = str(tds[0].text)
            submit_time = str(tds[1].text)
            judge_status = str(tds[2].text)
            pro_id = str(tds[3].text)
            exe_time = str(tds[4].text)
            exe_memory = str(tds[5].text)
            code_len = str(tds[6].text)
            relative_url = str(tds[6].a.attrs['href'])
            language = str(tds[7].text)
            author = str(tds[8].text)

            code_url = OnlineJudges["hdu"]["url"] + relative_url

            request = urllib2.Request(code_url, headers = headers)
            response = urllib2.urlopen(request)
    
            html = response.read()
            html = zlib.decompress(html, 16 + zlib.MAX_WBITS)
            soup = BeautifulSoup(html, 'lxml')
            src_code = soup.textarea.text
            
            info = "/* Problem ID: " + pro_id + \
                    "\n * Author: " + author + \
                "\n * Run ID: " + run_id + \
                "\n * Exe Time: " + exe_time + \
                "\n * Exe Memory: " + exe_memory + \
                "\n * Code Len: " + code_len + \
                "\n * Language: " + language + \
                "\n */\n\n"

            src_code = info + src_code
            src_file_name = hdu_dir + '/hdu' + pro_id + '_'+ str(count) + extension_type[language]
            if not os.path.exists(src_file_name):
                src_code_file = codecs.open(src_file_name, 'wb', 'utf-8')
                src_code_file.write(src_code)
                src_code_file.close()
            count = count + 1

    print "Crawled " + str(len(solved_lists)) + ' problems.'
