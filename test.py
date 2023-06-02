import json

with open("class_skeleton.json", "r") as file:
    data = json.loads(file.read())
    print(type(data))
