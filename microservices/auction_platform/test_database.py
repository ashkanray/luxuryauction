import mysql.connector


def insert_data(user_id, item_id, start_time, end_time):
    db = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database="mysql",
        port=4099
    )

    cursor = db.cursor()

    sql = "INSERT INTO Auctions (user_id, item_id, start_time, end_time) VALUES (%s, %s, %s, %s)"
    val = (user_id, item_id, start_time, end_time)

    cursor.execute(sql, val)

    db.commit()

    print(cursor.rowcount, "record inserted.")

# test
# insert_data(14, 14, '2023-11-19 16:47:00', '2023-11-19 17:50:00')


def query_data(user_id, item_id):
    db = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database="mysql",
        port=4099
    )

    cursor = db.cursor()

    sql = "SELECT * FROM Auctions WHERE user_id = %s AND item_id = %s"
    val = (user_id, item_id)

    cursor.execute(sql, val)

    result = cursor.fetchall()

    for row in result:
        print(row)


# test
query_data(3, 9)


def get_live_auctions():
    db = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database="mysql",
        port=4099
    )

    cursor = db.cursor()

    sql = "SELECT * FROM Auctions WHERE status = 'live'"

    cursor.execute(sql)

    results = cursor.fetchall()

    # for row in result:
    #     print(row)
    live_auctions = [dict(zip(cursor.column_names, result))
                     for result in results]

    print(live_auctions)

# test
# get_live_auctions()
