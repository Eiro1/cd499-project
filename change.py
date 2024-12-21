import json

with open('course.json', 'r') as file:
    data = json.load(file)

for c in data['courses']:
    c['url'] = "https://www.queensu.ca/academic-calendar/search/?P="+c['name'][0:4]+"%20"+c['name'][4:]

with open("course.json", 'w') as file:
    json.dump(data, file, indent=2)


