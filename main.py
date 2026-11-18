import json
from db_config import database_connect

CLASSES = ["AC1", "AC2", "AC3", "SL", "CC", "2S"]
FARE = {"AC1": 2500, "AC2": 1800, "AC3": 1200, "SL": 500, "CC": 800, "2S": 400}


def show_table(cur):
    """Prints whatever the last SELECT gave us, one row per line."""
    names = [c[0] for c in cur.description]
    print("\n" + " | ".join(names))
    print("-" * 60)
    for row in cur.fetchall():
        print(" | ".join(str(x) for x in row))


def book_ticket(con, cur):
    name = input("Name: ")
    address = input("Address: ")
    phone = input("Phone: ")
    start = input("Boarding station: ").lower()
    end = input("Destination station: ").lower()
    tr_class = input("Class (AC1/AC2/AC3/SL/CC/2S): ").upper()
    if tr_class not in CLASSES:
        print("Wrong class!")
        return
    seats = int(input("Number of seats: "))

    # Find trains that stop at both stations (start first, then end)
    # and still have enough seats.
    cur.execute("SELECT tr_no, tr_name, stoppage FROM train_table")
    found = []
    for tr_no, tr_name, stoppage in cur.fetchall():
        stops = json.loads(stoppage)
        if start in stops and end in stops and stops.index(start) < stops.index(end):
            cur.execute(f"SELECT {tr_class} FROM availability_table WHERE tr_no = %s", (tr_no,))
            if cur.fetchone()[0] >= seats:
                found.append(tr_no)
                print(tr_no, tr_name)

    if not found:
        print("No train available.")
        return

    print("Fare per seat:", FARE[tr_class])
    choice = input("Enter the train number you want: ")
    if choice not in found:
        print("Wrong train number!")
        return

    price = seats * FARE[tr_class]
    cur.execute(
        "INSERT INTO customer_table (tr_no, customer_name, customer_phone, customer_address, "
        "boarding_station, destination_station, tr_class, no_seats, price, status) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'CONFIRMED')",
        (choice, name, phone, address, start, end, tr_class, seats, price),
    )
    pnr = cur.lastrowid  # the PNR that MySQL just made
    cur.execute(
        f"UPDATE availability_table SET {tr_class} = {tr_class} - %s WHERE tr_no = %s",
        (seats, choice),
    )
    con.commit()
    print("Ticket booked! Your PNR is", pnr, "| Total price:", price)


def view_ticket(cur):
    pnr = input("Enter PNR: ")
    cur.execute("SELECT * FROM customer_table WHERE pnr = %s", (pnr,))
    ticket = cur.fetchone()
    if ticket is None:
        print("Invalid PNR!")
        return
    print("\nPNR:", ticket[0])
    print("Train:", ticket[1])
    print("Name:", ticket[2])
    print("Phone:", ticket[3])
    print("Address:", ticket[4])
    print("From:", ticket[5].upper(), " To:", ticket[6].upper())
    print("Class:", ticket[7], " Seats:", ticket[8])
    print("Price:", ticket[9], " Status:", ticket[10])


def cancel_ticket(con, cur):
    pnr = input("Enter PNR: ")
    cur.execute(
        "SELECT tr_no, tr_class, no_seats, status FROM customer_table WHERE pnr = %s", (pnr,)
    )
    ticket = cur.fetchone()
    if ticket is None:
        print("Invalid PNR!")
        return
    tr_no, tr_class, seats, status = ticket
    if status == "CANCELLED":
        print("Already cancelled.")
        return
    if input("Cancel this ticket? (y/n): ").lower() != "y":
        return

    cur.execute("UPDATE customer_table SET status = 'CANCELLED' WHERE pnr = %s", (pnr,))
    # give the seats back
    cur.execute(
        f"UPDATE availability_table SET {tr_class} = {tr_class} + %s WHERE tr_no = %s",
        (seats, tr_no),
    )
    con.commit()
    print("Ticket cancelled.")


def add_train(con, cur):
    tr_no = input("Train number (5 digits): ")
    name = input("Train name: ").upper()
    stops = input("Stations in order, separated by commas: ").lower().split(",")
    stops = [s.strip() for s in stops]

    seat_count = {c: 0 for c in CLASSES}   # every class starts at 0 seats
    for c in input("Classes this train has (e.g. AC1,AC2): ").upper().split(","):
        c = c.strip()
        if c in CLASSES:
            seat_count[c] = int(input("Seats in " + c + ": "))
    has = [c for c in CLASSES if c in seat_count and seat_count[c] > 0]

    cur.execute(
        "INSERT INTO train_table VALUES (%s, %s, %s, %s)",
        (tr_no, name, json.dumps(stops), json.dumps(has)),
    )
    cur.execute(
        "INSERT INTO availability_table VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (tr_no, *[seat_count[c] for c in CLASSES]),
    )
    con.commit()
    print("Train added!")


def remove_train(con, cur):
    tr_no = input("Train number to remove: ")
    cur.execute("SELECT COUNT(*) FROM customer_table WHERE tr_no = %s", (tr_no,))
    if cur.fetchone()[0] > 0:
        print("Cannot remove: this train already has bookings.")
        return
    cur.execute("DELETE FROM availability_table WHERE tr_no = %s", (tr_no,))
    cur.execute("DELETE FROM train_table WHERE tr_no = %s", (tr_no,))
    con.commit()
    if cur.rowcount == 0:
        print("Train not found.")
    else:
        print("Train removed.")


def change_seats(con, cur):
    tr_no = input("Train number: ")
    tr_class = input("Class (AC1/AC2/AC3/SL/CC/2S): ").upper()
    if tr_class not in CLASSES:
        print("Wrong class!")
        return
    new = int(input("New number of seats: "))
    cur.execute(f"UPDATE availability_table SET {tr_class} = %s WHERE tr_no = %s", (new, tr_no))
    con.commit()
    print("Updated.")


con, cur = database_connect("localhost", "railway_user", "rail1234", "train")
if con is None:
    exit()

while True:
    print("\n1 Book  2 View ticket  3 Cancel  4 Customers  5 Trains  6 Seats")
    print("7 Add train  8 Remove train  9 Change seats  E Exit")
    key = input("Choose: ").strip().lower()

    try:
        if key == "1":
            book_ticket(con, cur)
        elif key == "2":
            view_ticket(cur)
        elif key == "3":
            cancel_ticket(con, cur)
        elif key == "4":
            cur.execute("SELECT * FROM customer_table")
            show_table(cur)
        elif key == "5":
            cur.execute("SELECT * FROM train_table")
            show_table(cur)
        elif key == "6":
            cur.execute("SELECT * FROM availability_table")
            show_table(cur)
        elif key == "7":
            add_train(con, cur)
        elif key == "8":
            remove_train(con, cur)
        elif key == "9":
            change_seats(con, cur)
        elif key == "e":
            print("Thank you!")
            break
        else:
            print("Invalid option!")
    except Exception as err:
        con.rollback()
        print("Something went wrong:", err)

cur.close()
con.close()