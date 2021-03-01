from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
from dateutil.tz import tz

# url = 'https://www.joinclubhouse.com/event/xq43QJD5' 
# url = 'https://www.joinclubhouse.com/event/mg8vAB9Z?fbclid=IwAR06WgBBfOY4t2qX2k0tCA3kHuc7W8JeuQLnQ315KG_xtWfrEnqvnwWCPY4'
# url = 'https://www.joinclubhouse.com/event/mWJY4QEB?fbclid=IwAR1lE6k8wyxXQQI2kMd9Q9rdRu_FVLIJhqn7Harj_nIgXNIGtzgLNqpys8Y'
# url = 'https://www.joinclubhouse.com/event/myon9OwO?fbclid=IwAR0y-FICVM5-8iyzuC7thhKmF49SwVg-n2jwwj8TvrTI9j31pYwpduY6RBY'

def parse_clubhouse_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def get_room_title(clubhouse_page):
    return clubhouse_page.find('div', class_="mt-1").text.strip()

def get_room_date(clubhouse_page):
    room_date = clubhouse_page.find('span', class_="font-light").text
    rooms_date_information = clubhouse_page.find_all("span", class_="font-semibold")
    room_day = rooms_date_information[0].text
    room_hour = rooms_date_information[1].text
    correct_date = room_date + " " + room_day + " " + room_hour
    timezone_info = {"PST": tz.gettz('America/Los_Angeles')}
    convert_to_polish_timezone = tz.gettz("Europe/Warsaw")
    current_datetime = parse(correct_date, tzinfos=timezone_info)
    current_datetime = current_datetime.astimezone(convert_to_polish_timezone)
    return current_datetime

def get_hosts_avatars(clubhouse_page):
    avatars = clubhouse_page.find_all("div", class_="mx-1")
    avatar_urls = []
    for avatar in avatars:
        specific_avatar = avatar.find("div", class_="rounded-ch")["style"]
        left_colon = avatar.find("div", class_="rounded-ch")["style"].find('(')
        right_colon = avatar.find("div", class_="rounded-ch")["style"].find(')')
        avatar_url = specific_avatar[left_colon+2:right_colon-1]
        avatar_urls.append(avatar_url)
    return avatar_urls

def get_hosts(clubhouse_page):
    hosts = clubhouse_page.find("div", class_='px-6').text.strip()
    hosts = hosts.replace("w/","").split(",")
    return hosts
    
def get_room_description(clubhouse_page):
    return clubhouse_page.select("div[class='mt-6']")[0].text.strip()

def get_clubhouse_room_info(url):
    
    clubhouse_page = parse_clubhouse_url(url)

    room_title = get_room_title(clubhouse_page)
    room_date = get_room_date(clubhouse_page)
    avatars = get_hosts_avatars(clubhouse_page)
    hosts = get_hosts(clubhouse_page)
    description = get_room_description(clubhouse_page)
    room_information = {
        "title": room_title, 
        "room_date": room_date, 
        "avatars": avatars,
        "hosts": hosts,
        "description": description
    }
    return room_information
  