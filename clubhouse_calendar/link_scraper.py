from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
from dateutil.tz import tz

# url = 'https://www.joinclubhouse.com/event/xq43QJD5' 
# url = 'https://www.joinclubhouse.com/event/mg8vAB9Z?fbclid=IwAR06WgBBfOY4t2qX2k0tCA3kHuc7W8JeuQLnQ315KG_xtWfrEnqvnwWCPY4'
# url = 'https://www.joinclubhouse.com/event/mWJY4QEB?fbclid=IwAR1lE6k8wyxXQQI2kMd9Q9rdRu_FVLIJhqn7Harj_nIgXNIGtzgLNqpys8Y'
url = 'https://www.joinclubhouse.com/event/myon9OwO?fbclid=IwAR0y-FICVM5-8iyzuC7thhKmF49SwVg-n2jwwj8TvrTI9j31pYwpduY6RBY'

def get_clubhouse_room_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    room_title = soup.find('div', class_="mt-1").text
    room_date = soup.find('span', class_="font-light").text
    room_time = soup.find("span", class_="font-semibold uppercase").text
    room_day = soup.find("span", class_="font-semibold").text
    print(room_date)
    #print(room_time)
    #print(room_day)

    rooms = soup.find_all("span", class_="font-semibold")
    room_day = rooms[0].text
    room_hour = rooms[1].text
    correct_date = room_date + " " + room_day + " " + room_hour
    print(correct_date)
    timezone_info = {"PST": tz.gettz('America/Los_Angeles')}
    convert_to_polish_timezone = tz.gettz("Europe/Warsaw")
    a = parse(correct_date, tzinfos=timezone_info)
    print(f"thot {a}")
    a = a.astimezone(convert_to_polish_timezone)
    print(a)

    
    avatars = soup.find_all("div", class_="mx-1")
    avatar_urls = []
    for avatar in avatars:
        specific_avatar = avatar.find("div", class_="rounded-ch")["style"]
        left_colon = avatar.find("div", class_="rounded-ch")["style"].find('(')
        right_colon = avatar.find("div", class_="rounded-ch")["style"].find(')')
        avatar_url = specific_avatar[left_colon+2:right_colon-1]
        avatar_urls.append(avatar_url)

    print(avatar_urls)
    
    hosts = soup.find("div", class_='px-6')
    hosts = hosts.text.strip()
    print(hosts)
    hosts = hosts.replace("w/","").split(",")
    print(hosts)

    description = soup.find("div", class_ = "mt-6").text
    description = soup.select("div[class='mt-6']")[0].text.strip()
    print(description)
    
    return room_title.strip()



print(get_clubhouse_room_info(url))
  