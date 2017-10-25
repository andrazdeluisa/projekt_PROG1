import requests
import re
import os
import csv




salaries_link = 'http://www.spotrac.com/nba/rankings/2016/cap-hit/'
stats_link = 'https://www.basketball-reference.com/leagues/NBA_2017_per_game.html'
directory = 'web_pages'
salaries_basename = 'salaries.html'
stats_basename = 'stats.html'
salaries_filename = os.path.join(directory, salaries_basename)
stats_filename = os.path.join(directory, stats_basename)


def download_url_to_string(url):
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException:
        print('failed to connect to url' + url)
        return
    pagecontent = r.text
    return pagecontent

def save_string_to_file(text, filename):
    with open(filename, 'w') as file_out:
        file_out.write(text)
    return 

def save_frontpage_to_file(url, filename):
    pagecontent = download_url_to_string(url)
    save_string_to_file(pagecontent, filename)
    return


def read_file_to_string(filename):
    with open(filename, 'r') as file_in:
        text = file_in.read()
    return text




















