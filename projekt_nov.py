import requests
import re
import os
import csv



resorts_baselink = 'http://www.skiresort.info/ski-resorts/'
directory = 'web_pages'
resorts_basename = 'resorts.html'
resorts_first_page = 'resorts1.html'
resorts1_filename = os.path.join(directory, resorts_first_page)
resorts_filename = os.path.join(directory, resorts_basename)
resorts_csv_filename = 'resorts.csv'



def download_url_to_string(url):
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException:
        print('failed to connect to url' + url)
        return
    pagecontent = r.text
    return pagecontent

def save_string_to_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return 

def save_frontpage_to_file(url, filename):
    pagecontent = download_url_to_string(url)
    save_string_to_file(pagecontent, filename)
    return

def read_file_to_string(filename):
    with open(filename, 'r', encoding='utf8') as file_in:
        text = file_in.read()
    return text


##def number_of_pages(page):
##    rx = re.compile(r'href="http://www.skiresort.info/ski-resorts/page/2/".*href="http://www.skiresort.info/ski-resorts/page/2/".*href="http://www.skiresort.info/ski-resorts/page/(?P<number>.*?)/',
##                    re.DOTALL)
##    block = re.search(rx, page)
##    number = block.groupdict()
##    return number

def save_pages_to_file(base_url, number_of_pages, filename):
    pagecontent = download_url_to_string(base_url)
    for i in range(2, number_of_pages + 1):
        pagecontent += download_url_to_string(base_url + 'page/{}/'.format(i))
    save_string_to_file(pagecontent, filename)
    return


#extracting resorts stats

def get_resorts_blocks(page):
    rx = re.compile(r'<div class="panel panel-default resort-list-item resort-list-item-image--big" id="resort(.*?)> Details </a> </div>',
                    re.DOTALL)
    resorts = re.findall(rx, page)
    return resorts


def get_dict_from_resort_stats_block(block):
    rx = re.compile(r'<a class="h3" href="http://www.skiresort.info/ski-resort/(.*?)">(?P<name>.*?)</a>(.*?)<div class="sub-breadcrumb"><a href="http://www.skiresort.info/ski-resorts/(.*?)/">'
                    r'(?P<continent>.*?)</a> <a href="http://www.skiresort.info/ski-resorts/(.*?)/">'
                    r'(?P<country>.*?)</a> <a href="http://www.skiresort.info/ski-resorts/(.*?)/">'
                    r'(?P<region>.*?)</a>(.*?)data-rank="'
                    r'(?P<rank>.*?)" style=(.*?)<td> <span >'
                    r'(?P<elevation difference>.*?)</span> (<span >'
                    r'(?P<base altitude>.*?)</span> - <span>'
                    r'(?P<peak altitude>.*?)</span>)(.*?)class="slopeinfoitem ">'
                    r'(?P<length>.*?)</span> <span class="slopeinfoitem blue">'
                    r'(?P<blue length>.*?)</span> <span class="slopeinfoitem red">'
                    r'(?P<red length>.*?)</span> <span class="slopeinfoitem black">'
                    r'(?P<black_length>.*?)</span>(.*?)<ul class="inline-dot"> <li>'
                    r'(?P<ski lifts>.*?) ski lifts</li>(.*?)icon-uE001-skipass"></i></span></td> <td>'
                    r'(?P<ski pass>.*?)</td>',
                    re.DOTALL)
    data = re.search(rx, block)
    resort_stats_dict = data.groupdict()
    return resort_stats_dict

def resorts_stats_from_file(filename):
    page = read_file_to_string(filename)
    blocks = get_resorts_blocks(page)
    resorts = [get_dict_from_resort_stats_block(block) for block in blocks]
    return resorts
    
#writing csv

def write_csv(fieldnames, rows, filename):
    with open(filename, 'w', encoding='utf8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return

def write_resorts_to_csv(resorts, filename):
    write_csv(resorts[0].keys(), resorts, filename)
    
resort_dict = resorts_stats_from_file(resorts_filename)
write_resorts_to_csv(resort_dict, resorts_csv_filename)

















