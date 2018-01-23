import requests
import re
import os
import csv




salaries_link = 'http://www.spotrac.com/nba/rankings/2016/cap-hits/'
stats_link = 'https://www.basketball-reference.com/leagues/NBA_2017_per_game.html'
double_doubles_link = 'http://www.espn.com/nba/statistics/player/_/stat/double-doubles/sort/doubleDouble/year/2017/qualified/false/count/'
team_stats_link = 'https://www.basketball-reference.com/leagues/NBA_2017.html'
directory = 'web_pages'
salaries_basename = 'salaries.html'
stats_basename = 'stats.html'
double_doubles_basename = 'dd.html'
team_stats_basename = 'team_stats.html'
salaries_filename = os.path.join(directory, salaries_basename)
stats_filename = os.path.join(directory, stats_basename)
double_doubles_filename = os.path.join(directory, double_doubles_basename)
team_stats_filename = os.path.join(directory, team_stats_basename)
salaries_csv_filename = 'salaries.csv'
stats_csv_filename = 'stats.csv'
double_doubles_csv_filename = 'dd.csv'
team_stats_csv_filename = 'team_stats.csv'


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
    rx = re.compile(r'>(?P<Index>.*?)<.*html">'
                    r'(?P<Name>.*?)<.*stat="pos" >'
                    r'(?P<Position>.*?)<.*stat="age" >'
                    r'(?P<Age>.*?)<.*stat="team_id" >(<a .*html">)?'
                    r'(?P<Team>.*?)<.*stat="g" >'
                    r'(?P<GP>.*?)<.*stat="gs" >'
                    r'(?P<GS>.*?)<.*stat="mp_per_g" >'
                    r'(?P<MIN>.*?)<.*stat="fg_per_g" >'
                    r'(?P<FG>.*?)<.*stat="fga_per_g" >'
                    r'(?P<FGA>.*?)<.*stat="fg_pct" >'
                    r'(?P<FG_PCT>.*?)<.*stat="ft_per_g" >'
                    r'(?P<FT>.*?)<.*stat="fta_per_g" >'
                    r'(?P<FTA>.*?)<.*stat="ft_pct" >'
                    r'(?P<FT_PCT>.*?)<.*stat="orb_per_g" >'
                    r'(?P<OREB>.*?)<.*stat="drb_per_g" >'
                    r'(?P<DREB>.*?)<.*stat="trb_per_g" >'
                    r'(?P<TOTREB>.*?)<.*stat="ast_per_g" >'
                    r'(?P<AST>.*?)<.*stat="stl_per_g" >'
                    r'(?P<STL>.*?)<.*stat="blk_per_g" >'
                    r'(?P<BLK>.*?)<.*stat="tov_per_g" >'
                    r'(?P<TO>.*?)<.*stat="pf_per_g" >'
                    r'(?P<PF>.*?)<.*stat="pts_per_g" >'
                    r'(?P<PTS>.*?)</td>',
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
                    r'(?P<Name>.*?)<.*title="(Reserve Suspended)?">'
                    r'(?P<Salary>.*?)\s',
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
    rx = re.compile(r'>(?P<Name>.*?)</a>.*class="sortcell">'
                    r'(?P<DD>.*?)</td><td >'
                    r'(?P<TD>.*?)<',
                    re.DOTALL)
    data = re.search(rx, block)
    player_dd_dict = data.groupdict()
    return player_dd_dict
    
def players_dd_from_file(filename):
    page = read_file_to_string(filename)
    blocks = page_to_players_dd(page)
    players = [get_dict_from_player_dd_block(block) for block in blocks]
    return players

#extracting team stats

def page_to_team_stats(page):
    rx = re.compile(r'<tr class="full_table" ><th scope="row" class="left " data-stat="team_name" >'
                    r'(.*?)/td></tr>',
                    re.DOTALL)
    teams = re.findall(rx, page)
    a = len(teams)
    return teams[: a//2]

def get_dict_from_team_stats_block(block):
    rx = re.compile(r'/2017.html">(?P<TeamName>.*?)</a>.*<td class="right " data-stat="wins" >'
                    r'(?P<Wins>.*?)</td><td class="right " data-stat="losses" >'
                    r'(?P<Losses>.*?)</td><td class="right " data-stat="win_loss_pct" >',
                    re.DOTALL)
    data = re.search(rx, block)
    team_stats_dict = data.groupdict()
    return team_stats_dict

def team_stats_from_file(filename):
    page = read_file_to_string(filename)
    blocks = page_to_team_stats(page)
    teams = [get_dict_from_team_stats_block(block) for block in blocks]
    return teams

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


















