import requests
from bs4 import BeautifulSoup

def extract_number_from_string(string):
    return int("".join(char for char in string if char.isdigit()))

def extract_point_data(row):
    data = list(map(lambda elem: elem.text, row.select("tbody > h2")))
    return {
        "points_taken": extract_number_from_string(data[0]),
        "points_neutralized": extract_number_from_string(data[1])
    }

def extract_favorite_data(row):
    favorites_table = row.select("tbody")[1]
    favorite_weapon_tr, favorite_boost_tr = favorites_table.select("tr")[0], favorites_table.select("tr")[2]

    return {
        "weapon": {
            "name": favorite_weapon_tr.find("h3").text,
            "times_chosen": extract_number_from_string(favorite_weapon_tr.find("p").text)
        },
        "boost": {
            "name": favorite_boost_tr.find("h3").text,
            "times_chosen": extract_number_from_string(favorite_boost_tr.find("p").text)
        }
    }

def extract_upgrades_data(row):
    upgrades_table = row.select("tbody")[1]
    upgrades_tr = upgrades_table.select("tr")[1]

    upgrade_elems = list(map(lambda x: x.text, upgrades_tr.select("td > p")))
    upgrades_data = {}

    for i in upgrade_elems:
        split_i = i.split(":")
        upgrades_data[split_i[0].replace(" ", "_").lower()] = split_i[1].strip()

    return upgrades_data

def extract_weapon_data(rows):
    pistol_trs = rows[0].select("tbody")[0].find_all("tr")
    shotgun_trs = rows[0].select("tbody")[1].find_all("tr")
    assault_trs = rows[1].select("tbody")[0].find_all("tr")
    sniper_trs = rows[1].select("tbody")[1].find_all("tr")

    return {
        "pistol": extract_general_stats(pistol_trs),
        "shotgun": extract_general_stats(shotgun_trs),
        "assault": extract_general_stats(assault_trs),
        "sniper": extract_general_stats(sniper_trs)
    }

def extract_general_stats(trs):
    stats_data = {}

    for tr in trs:
        data = tr.select("td")
        stats_data[data[0].text.replace(" ", "_").lower()] = data[1].text.strip()

    return stats_data

def get_stats(user):
    page = requests.get(f"https://stats.takepoint.io/user/{user}")
    soup = BeautifulSoup(page.content, "html.parser")

    rows = soup.select("#pageContainer > .row")

    data_model = extract_point_data(rows[0])
    data_model["favorite"] = extract_favorite_data(rows[0])
    data_model["upgrades"] = extract_upgrades_data(rows[0])
    data_model["weapons"] = extract_weapon_data([rows[1], rows[2]])

    data_model["stats"] = extract_general_stats(rows[0].select("tbody")[0].find_all("tr")) # Merges two dictionaries

    return data_model
