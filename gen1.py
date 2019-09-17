import re
import random
from model import *

pattern=re.compile(r"\d")
def qualifyGuessAddress(address):
    qualify=False
    if pattern.search(address) is not None:
        qualify=True
    if ("村" in address) and (address[-1:]!='村'):
        qualify=True
    return qualify

provinces = session.query(Province).all()
for province in provinces:
    print(f"Start {province.name}")
    cities = province.children
    cities = random.choices(cities, k=7)
    for city in cities:
        print(f"Start {city.name}")
        countries = city.children
        countries = random.choices(countries, k=5)
        for country in countries:
            print(f"Start {country.name}")
            towns = country.children
            towns = random.choices(towns, k=5)
            for town in towns:
                villages = town.children
                villages = random.choices(villages, k=5)
                four_address = ''.join((province.name, city.name, country.name, town.name))

                for village in villages:
                    try:
                        v_name = village.name
                        if v_name[-2:]=="社区":
                            v_name=v_name[0:-2]
                        res = guess(four_address, v_name, 10, False)
                        if res["guess_address_response"]["status"]!="1": break
                        datas = res["guess_address_response"]["data"]
                        for data in datas:
                            if data["town"]!=town.name:
                                continue
                            if not qualifyGuessAddress(data["guessAddress"]): continue
                            guess_address = data["guessAddress"]
                            if len(session.query(GuestAddress).filter(GuestAddress.name.like(f"%{guess_address}%")).all()) != 0:
                                print("duplicate found skipping")
                                continue
                            guest_address=GuestAddress(name=data["guessAddress"], village_id=village.village_id)
                            session.add(guest_address)
                            session.commit()
                            print(f"Stored \"{four_address}{guest_address.name}\"")
                            break
                            #time.sleep(0.01)
                    except:
                        break




