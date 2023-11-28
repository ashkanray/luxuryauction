import time
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta


# connect to database
mysql_connection = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="mysql",
    port=4099
)


def auto_change_auction_status():
    """
    Check all auctions and update their status based on the current time
    """
    print("Checking auction status...")  # Added this print statement

    now = datetime.now()

    # update auction status in mysql database
    with mysql_connection.cursor() as cursor:
        # start auctions
        sql = "UPDATE Auctions SET status = 'live' WHERE start_time <= %s AND status = 'pending'"
        cursor.execute(sql, (now,))
        # end auctions
        sql = "UPDATE Auctions SET status = 'closed' WHERE end_time <= %s AND status = 'live'"
        cursor.execute(sql, (now,))
        mysql_connection.commit()

    print("Auction status checked.")  # Added this print statement


# create scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=auto_change_auction_status,
                  trigger="interval", seconds=60)
scheduler.start()

# Keep the script running.
while True:
    time.sleep(1)
