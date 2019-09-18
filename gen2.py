from sqlalchemy.sql import func
from model import *






def fulfill():
    num = 0
    while(session.query(Entry).count()<1000):
        addr = session.query(GuestAddress).order_by(func.random()).first()
        village = addr.parent
        town = village.parent
        country = town.parent
        city = country.parent
        province = city.parent
        entry = Entry(name =get_name(), phone=get_phone(), province=province.name,city=city.name,country=country.name,town=town.name,detail_address=addr.name)
        entry = process_omit(entry)
        entry.composed_string = compose_string(entry)
        print(entry.composed_string)
        session.add(entry)
        session.commit()
        num+=1
        pass

# import json
# input=[]
# answer=[]
# for entry in random.choices(session.query(Entry).all(),k=5):
#     input.append(entry.composed_string)
#     answer.append({
#         "姓名": entry.name,
#         "手机": entry.phone,
#         "地址": [
#             entry.province, entry.city, entry.country, entry.town, entry.detail_address
#         ]
#     })
#
# print("\n".join(input))
# print(json.dumps(answer,ensure_ascii=False))

def mark_dataset():
    while True:
        guest_id = int(input("ID: "))
        guest_address = session.query(GuestAddress).filter(GuestAddress._id==guest_id).first()
        village = guest_address.parent
        town = village.parent
        country = town.parent
        city = country.parent
        province = city.parent
        entry = EntryVar2(name=get_name(), phone=get_phone(), parent_id=guest_id,  province=province.name,city=city.name,country=country.name,town=town.name)
        print(guest_address.name)
        entry.road = input("路: ")
        entry.house_number = input("门牌号: ")
        entry.detail_address = input("详细地址: ")
        session.add(entry)
        session.commit()



if __name__=='__main__':
    import json
    input_data=[]
    answer=[]
    for entry in session.query(Entry).all():
        entry.composed_string = entry.compose_string()
        input_data.append(f"1!{entry.composed_string}\n")
        answer.append({
                "姓名": entry.name,
                "手机": entry.phone,
                "地址": [
                    entry.province, entry.city, entry.country, entry.town, entry.detail_address
                ]
        })
    session.commit()
    for entry2 in session.query(EntryVar2).all():
        input_data.append(f"2!{entry2.composed_string}\n")
        answer.append({
                "姓名": entry2.name,
                "手机": entry2.phone,
                "地址": [
                    entry2.province, entry2.city, entry2.country, entry2.town, entry2.road, entry2.house_number,
                    entry2.detail_address
                ]
        })
    session.commit()

    for entry3 in session.query(EntryVar3).all():
        input_data.append(f"3!{entry3.composed_string}\n")
        answer.append({
            "姓名": entry3.name,
            "手机": entry3.phone,
            "地址": [
                entry3.province, entry3.city, entry3.country, entry3.town, entry3.road, entry3.house_number,
                entry3.detail_address
            ]
        })
    session.commit()
    with open("input.txt", "w") as input_file:
        input_file.writelines(input_data)
    with open("answer.txt", "w") as answer_file:
        answer_file.write(json.dumps(answer, ensure_ascii=False))
