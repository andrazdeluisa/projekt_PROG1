import requests
import re
import os
import csv




salaries_link = 'http://www.spotrac.com/nba/rankings/2016/cap-hits/'
stats_link = 'https://www.basketball-reference.com/leagues/NBA_2017_per_game.html'
double_doubles_link = 'http://www.espn.com/nba/statistics/player/_/stat/double-doubles/sort/doubleDouble/year/2017/qualified/false/count/'
directory = 'web_pages'
salaries_basename = 'salaries.html'
stats_basename = 'stats.html'
double_doubles_basename = 'dd.html'
salaries_filename = os.path.join(directory, salaries_basename)
stats_filename = os.path.join(directory, stats_basename)
double_doubles_filename = os.path.join(directory, double_doubles_basename)
salaries_csv_filename = 'salaries.csv'
stats_csv_filename = 'stats.csv'
double_doubles_csv_filename = 'dd.csv'


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

def save_frontpage_to_file_dd(url, filename):
    pagecontent = ''
    for i in range(13):
        pagecontent += download_url_to_string(url + '{}'.format(i*40 + 1))
    save_string_to_file(pagecontent, filename)
    return

def read_file_to_string(filename):
    with open(filename, 'r', encoding='utf8') as file_in:
        text = file_in.read()
    return text

#extracting players stats

def page_to_players_stats(page):
    rx = re.compile(r'<tr class="full_table" >(.*?)</tr>',
                    re.DOTALL)
    players = re.findall(rx, page)
    return players

def get_dict_from_player_stats_block(block):
    rx = re.compile(r'>(?P<index>.*?)<.*html">'
                    r'(?P<name>.*?)<.*stat="pos" >'
                    r'(?P<position>.*?)<.*stat="age" >'
                    r'(?P<age>.*?)<.*stat="team_id" >(<a .*html">)?'
                    r'(?P<team>.*?)<.*stat="g" >'
                    r'(?P<games>.*?)<.*stat="gs" >'
                    r'(?P<g_started>.*?)<.*stat="mp_per_g" >'
                    r'(?P<minutes>.*?)<.*stat="fg_per_g" >'
                    r'(?P<fg>.*?)<.*stat="fga_per_g" >'
                    r'(?P<fga>.*?)<.*stat="fg_pct" >'
                    r'(?P<fg_pct>.*?)<.*stat="ft_per_g" >'
                    r'(?P<ft>.*?)<.*stat="fta_per_g" >'
                    r'(?P<fta>.*?)<.*stat="ft_pct" >'
                    r'(?P<ft_pct>.*?)<.*stat="orb_per_g" >'
                    r'(?P<oreb>.*?)<.*stat="drb_per_g" >'
                    r'(?P<dreb>.*?)<.*stat="trb_per_g" >'
                    r'(?P<totreb>.*?)<.*stat="ast_per_g" >'
                    r'(?P<assists>.*?)<.*stat="stl_per_g" >'
                    r'(?P<steals>.*?)<.*stat="blk_per_g" >'
                    r'(?P<blocks>.*?)<.*stat="tov_per_g" >'
                    r'(?P<turnovers>.*?)<.*stat="pf_per_g" >'
                    r'(?P<pfouls>.*?)<.*stat="pts_per_g" >'
                    r'(?P<points>.*?)</td>',
                    re.DOTALL)
    data = re.search(rx, block)
    player_stats_dict = data.groupdict()
    return player_stats_dict

def players_stats_from_file(filename):
    page = read_file_to_string(filename)
    blocks = page_to_players_stats(page)
    players = [get_dict_from_player_stats_block(block) for block in blocks]
    return players

#exctracting players salaries

def page_to_players_salaries(page):
    rx = re.compile(r'<td class="rank-name player noborderright"'
                    r'(.*?)\s</span></td>',
                    re.DOTALL)
    players = re.findall(rx, page)
    return players

def get_dict_from_player_salary_block(block):
    rx = re.compile(r'class="team-name">'
                    r'(?P<name>.*?)<.*title="(Reserve Suspended)?">'
                    r'(?P<salary>.*?)\s',
                    re.DOTALL)
    data = re.search(rx, block)
    player_salary_dict = data.groupdict()
    return player_salary_dict

def players_salaries_from_file(filename):
    page = read_file_to_string(filename)
    blocks = page_to_players_salaries(page)
    players = [get_dict_from_player_salary_block(block) for block in blocks]
    return players

#extracting double doubles stats

def page_to_players_dd(page):
    rx = re.compile(r'<a href="http://www.espn.com/nba/player/_/id/'
                    r'(.*?)/td></tr>',
                    re.DOTALL)
    players = re.findall(rx, page)
    return players

def get_dict_from_player_dd_block(block):
    rx = re.compile(r'>(?P<name>.*?)</a>.*class="sortcell">'
                    r'(?P<dd>.*?)</td><td >'
                    r'(?P<td>.*?)<',
                    re.DOTALL)
    data = re.search(rx, block)
    player_dd_dict = data.groupdict()
    return player_dd_dict
    
def players_dd_from_file(filename):
    page = read_file_to_string(filename)
    blocks = page_to_players_dd(page)
    players = [get_dict_from_player_dd_block(block) for block in blocks]
    return players

#writing csv

def write_csv(fieldnames, rows, filename):
    with open(filename, 'w', encoding='utf8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return

def write_players_to_csv(players, filename):
    write_csv(players[0].keys(), players, filename)


















