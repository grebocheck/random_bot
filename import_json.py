import json

with open('gays.json', 'r', encoding="utf-8") as jsonFile:
    pythonJSON = json.load(jsonFile)
jsonFile.close()

# for a in pythonJSON:
#     print(str(a))
#     print(pythonJSON[a])
#     for b in pythonJSON[a]:
#         pass
#         print(str(b))


def group_list():
    mass = []
    for a in pythonJSON:
        mass.append(str(a).split(' ')[1])
    return mass


def stud_list(group):
    mass = []
    try:
        for a in pythonJSON[f"група {group}"]:
            mass.append(str(a))
    except:
        for a in pythonJSON[f"Група {group}"]:
            mass.append(str(a))
    return mass

# print(group_list())
# print(stud_list("ОН-11мн"))