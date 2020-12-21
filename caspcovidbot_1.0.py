from bs4 import BeautifulSoup
import requests
import datetime
import tweepy


source = requests.get("https://www.worldometers.info/coronavirus/country/malaysia/").text
worldometers_soup = BeautifulSoup(source, "lxml")

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


def get_stats(soup):
    stat_list = []  # [total cases, total deaths, recovered, new cases, new deaths]
    statistics = soup.find_all("div", class_="maincounter-number")
    for i in statistics:
        i = i.text.replace("\n", "").replace(",", "")
        stat_list.append(i)

    statistics = soup.find("li", class_="news_li")
    stat_list.append(int(statistics.text.split()[0].replace(",", "")))  # new cases
    stat_list.append(int(statistics.text.split()[4].replace(",", "")))  # new deaths

    return stat_list


def update_stats(stat_list):
    with open("stats.txt", "w") as file:
        date = str(datetime.datetime.now()).split(" ")[0]
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        file.write(date.strftime('%b %d,%Y') + "\n")

        file.write("New cases : {}".format(stat_list[3]) + "\n")
        file.write("New deaths : {}".format(stat_list[4]) + "\n")
        file.write("Total active cases : {}".format(str(int(stat_list[0]) - int(stat_list[1])
                                                        - int(stat_list[2]))) + "\n")
        file.write("Total cases : {}".format(stat_list[0]) + "\n")
        file.write("Total deaths : {}".format(stat_list[1]) + "\n")
        file.write("Total recovered : {}".format(stat_list[2]) + "\n")
        file.write("""
        
Stay safe!
        """
)


def update_status():
    api = tweepy.API(auth)
    with open("stats.txt", "r") as file:
        api.update_status(file.read())


update_stats(get_stats(worldometers_soup))
update_status()
