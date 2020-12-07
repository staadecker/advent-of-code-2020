with open("input.txt","r") as f:
    passes = list(boarding_pass.strip() for boarding_pass in f.readlines())

highest_id = 0

all_seats = [0]*(127*8+7)

for b_pass in passes:
    row_code = b_pass[0:7]

    row = 0

    for row_character in row_code:
        row = row << 1
        if row_character == "B":
            row +=1

    column = 0
    column_code = b_pass[7:]

    for column_character in column_code:
        column = column << 1
        if column_character == "R":
            column+=1

    seat_id = row * 8 + column

    highest_id = max(highest_id, seat_id)

    all_seats[seat_id] = 1
    
print(highest_id)

prev_seat = 0

for seat_id, seat in enumerate(all_seats):
    if prev_seat and not seat:
        print(seat_id)
    prev_seat = seat
