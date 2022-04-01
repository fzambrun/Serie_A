from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import pandas as pd

option = Options()
option.headless = False
driver = webdriver.Chrome(options=option)
driver.get(my_url)

matchday =[]
matchday_number=[]
errors = []
for day in range (1, 39):
    my_url= f'https://www.legaseriea.it/en/serie-a/archive/2020-21/UNICO/UNI/{day}'
    driver.get(my_url)  
    sleep(5)
    
    for i in range (4,14):
        match = ''
        try:
            for k in range (2,4):
                xpath = str('/html/body/main/div[1]/section[1]/section/div['+str(i)+']/div['+str(k)+']/h4')
                team = (driver.find_element_by_xpath(xpath).text)
                sil = team[0:3].upper()
                match = match + sil
            matchday.append(match)
            matchday_number.append(day)
        except:
            errors.append("matchday " + str(day) + " match " + str(i-3))
            continue

print('errors')
print(errors)
print('')
print("total " + str(len(matchday)))

matchday.insert(1,'HELROM')
matchday_number.insert(1,1)

new_strings = []
for string in matchday:
    new_string = string. replace("HEL", "VER")
    new_strings. append(new_string)
matchday = new_strings


season = []


for i in range (0,len(matchday)):
    try:
        url = f'https://www.legaseriea.it/en/serie-a/match-report/2016-17/UNICO/UNI/{matchday_number[i]}/{matchday[i]}'

        driver.get(url)
        sleep(5)

        #Get date
        date = WebDriverWait(driver,20).until(EC.element_to_be_clickable((
            By.XPATH, '/html/body/main/div[1]/section/div[1]/div[1]/span'))).text
        date = datetime.strptime(date, '%d/%m/%Y - %H:%M').strftime('%m/%d/%Y')

        #Get home and away team name ---> In fact, we already have this information
        home_team = driver.find_element_by_xpath(
                    '/html/body/main/div[1]/section/div[1]/h3[1]/span').text
        away_team = driver.find_element_by_xpath(
                    '/html/body/main/div[1]/section/div[1]/h3[2]/span').text

        #Get the text from the home and away score
        home_score = driver.find_element_by_xpath(
                    '/html/body/main/div[1]/section/div[1]/div[3]').text

        away_score = driver.find_element_by_xpath(
                    '/html/body/main/div[1]/section/div[1]/div[5]').text

        #Stats to scrapp

        stats = ['possession_%', 'shots_on_target', 'shots', 'passes',
                           'recovers' , 'corners', 'offsides', 'yellow_cards',
                           'red_cards', 'fouls_made']

        #Add the home_ to the above stats to differ it from the away team stats
        home_stats_name = []
        for i in range (0,10):
            stat = "home_" + stats[i]
            home_stats_name.append(stat)

        #possession is a txt with the % character so it has to be sliced
        home_possession_ = driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[2]/div[2]').text
        home_possession_ = int(home_possession_[0:2])

        #Get the rest of the stats as ints
        home_shots_on_target = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[6]/div[2]').text)
        home_shots = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[5]/div[2]').text)
        home_passes = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[20]/div[2]').text)
        home_recovers = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[26]/div[2]').text)
        home_corners = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[19]/div[2]').text)
        home_offsides = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[18]/div[2]').text)
        home_yellow_cards = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[22]/div[2]').text)
        home_red_cards = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[24]/div[2]').text)
        home_fouls_made =int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[13]/div[2]').text)

        #Create a list with the home team stats values
        home_stats_values = [home_possession_,home_shots_on_target,home_shots,home_passes,home_recovers
                             ,home_corners,home_offsides,home_yellow_cards,home_red_cards,home_fouls_made]

        #Creates a dict with with key and its value for the home team
        home_stats = {}
        for key in home_stats_name:
            for value in home_stats_values:
                home_stats[key] = value
                home_stats_values.remove(value)
                break

        #Now all the same steps but for the away team

        away_stats_name = []
        for i in range (0,10):
            stat = "away_" + stats[i]
            away_stats_name.append(stat)

        away_possession_ = driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[2]/div[4]').text
        away_possession_ = int(away_possession_[0:2])

        away_shots_on_target = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[6]/div[4]').text)
        away_shots = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[5]/div[4]').text)
        away_passes = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[20]/div[4]').text)
        away_recovers = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[26]/div[4]').text)
        away_corners = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[19]/div[4]').text)
        away_offsides = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[18]/div[4]').text)
        away_yellow_cards = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[22]/div[4]').text)
        away_red_cards = int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[24]/div[4]').text)
        away_fouls_made =int(driver.find_element_by_xpath(
                    '//*[@id="statistiche-comparate"]/div[13]/div[4]').text)

        away_stats_values = [away_possession_,away_shots_on_target,away_shots,away_passes,away_recovers,
                             away_corners,away_offsides,away_yellow_cards,away_red_cards,away_fouls_made]
        away_stats = {}
        for key in away_stats_name:
            for value in away_stats_values:
                away_stats[key] = value
                away_stats_values.remove(value)
                break 

        #Get all data for one match in one list that will be added to the dataframe
        match = [date, home_team, away_team, home_score, away_score, home_stats['home_possession_%'], away_stats['away_possession_%'],
                     home_stats['home_shots_on_target'], away_stats['away_shots_on_target'], home_stats['home_shots'], away_stats['away_shots'],
                     home_stats['home_passes'], away_stats['away_passes'],
                     home_stats['home_recovers'], away_stats['away_recovers'],
                     home_stats['home_corners'], away_stats['away_corners'], home_stats['home_offsides'], away_stats['away_offsides'],
                     home_stats['home_yellow_cards'], away_stats['away_yellow_cards'], home_stats['home_red_cards'], away_stats['away_red_cards'],
                     home_stats['home_fouls_made'], away_stats['away_fouls_made']]

        #adding the match stats to the season list
        season.append(match)
        
    except:
        errors.append(str(matchday_number[i]) + "match " + str(matchday[i]))
        continue

columns = ['date', 'home_team', 'away_team', 'home_score', 'away_score', 'home_possession_%','away_possession_%',
                 'home_shots_on_target', 'away_shots_on_target', 'home_shots', 'away_shots',
                 'home_passes', 'away_passes',
                 'home_recovers', 'away_recovers',
                 'home_corners', 'away_corners', 'home_offsides', 'away_offsides',
                 'home_yellow_cards', 'away_yellow_cards', 'home_red_cards','away_red_cards',
                 'home_fouls_made','away_fouls_made']

dataset = pd.DataFrame(season,columns=columns)

dataset.to_csv('Serie_A_2020-21.csv', index=False)

print(erros)