import re

with open("input.txt","r") as f:
    data= f.read().strip()

data = data.split("\n\n")
required = {"byr","iyr","eyr","hgt","hcl","ecl","pid"}
eyecolors = {"amb","blu","brn","gry","grn","hzl","oth"}

p = []

for row in data:
    row = re.split("[ \n]", row)
    fields={}
    for field in row:
        [name, value] = field.split(":")
        fields[name]=value
    p.append(fields)

numvalid = 0
for i in p:
    if not required <= i.keys():
        continue
    

    if not 1920<= int(i["byr"]) <= 2002:
        continue

    if "iyr" not in i or (not 2010 <= int(i["iyr"]) <= 2020):
        continue

    if "eyr" not in i or (not 2020 <= int(i["eyr"]) <= 2030):
        continue

    if "hgt" not in i:
        continue

    height = i["hgt"]
    hunits = height[-2:]
    
    if hunits == "cm":
        if not 150<=int(height[:-2])<=193:
            continue
    elif hunits == "in":
        if not 59<=int(height[:-2])<=76:
            continue
    else:
        continue

    c = i["hcl"]
    if c[0] != "#":
        continue
    code = c[1:]
    if len(code) != 6:
        continue
    for chara in code:
        if not (97 <= ord(chara) <=102 or 48 <= ord(chara) <=57):
            continue
    if i["ecl"] not in eyecolors:
        continue
    if len(i["pid"]) != 9 or not i["pid"].isnumeric():
        continue

    numvalid+=1

print(numvalid)
