import re

with open("input.txt","r") as f:
    input_data = f.readlines()

input_data = list(map(lambda row: list(filter(lambda x: x!="",re.split(r"[^\d^\w]",row))), input_data))

print(input_data[0])

valid = 0

for [mini,maxi,parameter,password] in input_data:
    if (password[int(mini)-1] == parameter) != (password[int(maxi)-1] == parameter):
        valid +=1

print(valid)
