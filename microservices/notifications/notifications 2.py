from flask import Flask, request, jsonify
import redis
import json
import mysql.connector as mysql
from datetime import datetime
from flask_cors import CORS
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3500"}})

r = redis.Redis()



@app.route('/api/notifications/auction_end', methods= ['POST'])
def auction_end():
    """
    send an email to all the bidders and the seller
    that the auction window is closed.
    """
    data = request.get_json()

    # testing with placeholder
    recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    auction_name = "Hazzah"
    # testing with placeholder


    email_subject = f"The auction: {auction_name} has ended!"
    email_body = f'''
    <html>
        <body>
            <h1>The auction: {auction_name} has been closed</h1>
            <br>
            <p>To Buyers: The winner of the auction has been notified via a separate email!</p>
            <br>
            <p>To Seller: Your auction has a winner! The item is now in their shopping cart</p>
            <br>
            <p>Sincerely, TimePiece Traders</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)

@app.route('/api/notifications/favorite_list', methods= ['POST'])
def favorites_wish_list_item():
    """
    notify users when an item that matches their favorite/wish list criteria
    is listed for auction
    """
    data = request.get_json()


    # testing with placeholder
    recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    item_name = "Hazzah"
    # testing with placeholder


    email_subject = f"Favorites list alert!"
    email_body = f'''
    <html>
        <body>
            <h1>The item: {item_name} that matches your Favorite lists has been listed for auction!</h1>
            <br>
            <p>Please submit a bid to participate in this auction!</p>
            <br>
            <br>
            <p>Sincerely, TimePiece Traders</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)

@app.route('/api/notifications/high_bid', methods = ['POST'])
def new_high_bid():
    """
    notify the previous high bidder that they were outbid
    """
    data = request.get_json()
    recipients = data["user_email"]
    auction_name = "HUH"


    # testing with placeholder
    recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    auction_name = "Hazzah"
    # testing with placeholder


    email_subject = f"You have been out-bid for the auction: {auction_name}"
    email_body = f'''
    <html>
        <body>
            <h1>your previous high-bid for auction: {auction_name} has been out-bid</h1>
            <br>
            <p>Please submit a new bid higher than the current high-bid to secure your auction-win</p>
            <br>
            <br>
            <p>Sincerely, TimePiece Traders</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)



@app.route('/api/notifications/one_hour', methods = ['POST'])
def one_hour():
    """
    notify (send an email) to all the bidders on an item and the seller
    that the auction ends in 1 hour
    """
    data = request.get_json()

    # testing with placeholder
    recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    auction_name = "Hazzah"
    # testing with placeholder


    email_subject = f"One-Hour Alert for the Auction: {auction_name}"
    email_body = f'''
    <html>
        <body>
            <h1>The Auction: {auction_name} ends in 1 hour!</h1>
            <br>
            <p>To Buyers: This is the final reminder for the auction! Please re-evaluate your bids to be the grand-winner!</p>
            <p>To Seller: your patience is paying off. One more hour to go! :D </p>
            <br>
            <br>
            <p>Sincerely, TimePiece Traders</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)


@app.route('/api/notifications/one_day', methods = ['POST'])
def one_day():
    """
    notify (send an email) to all bidders on an item and the seller
    that the auction ends in 1 day
    """
    data = request.get_json()

    # testing with placeholder
    recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    auction_name = "Hazzah"
    # testing with placeholder


    email_subject = f"One-Day Alert for the Auction: {auction_name}"
    email_body = f'''
    <html>
        <body>
            <h1>The Auction: {auction_name} ends in 1 day!</h1>
            <br>
            <p>To Buyers: stay tuned!, we will notify you once more when the auction ends in 1 hour!</p>
            <p>To Seller: your auction will have a grand-winner in 1 day! :D </p>
            <br>
            <br>
            <p>Sincerely, TimePiece Traders</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)


@app.route('/api/notifications/winning_bid', methods = ['POST'])
def winning_bid():
    """
    notify (send an email) the user who had the final-high bid on the auction
    when the auction ends
    """
    data = request.get_json()

    # testing with placeholder
    recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    auction_name = "Hazzah"
    # testing with placeholder


    email_subject = f"CONGRATULATIONS You have won the auction: {auction_name}"
    email_body = f'''
    <html>
        <body>
            <h1>Your bid for the auction: {auction_name} has been finalized</h1>
            <br>
            <p>You are the winner of the auction! The item has been added to your shopping cart.</p>
            <p>You can checkout from the shopping cart whenever you wish.</p>
            <br>
            <br>
            <p>Sincerely, TimePiece Traders</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)

    



def send_email(recipients, email_subject, email_body):
    """
    to send emails based on the email addresses that I obtained

    """
    # email_rdy = MIMEText(email_body)
    email_rdy = MIMEMultipart()

    email_rdy["Subject"] = email_subject
    email_rdy['From'] = "kingboggerbob@gmail.com"
    pw = "dybsolarponjdsin"

    ## CHECK
    email_rdy['To'] = ', '.join(recipients)
    email_rdy.attach(MIMEText(email_body, "html"))


    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email_rdy['From'], pw)
        server.sendmail(email_rdy['From'], recipients, email_rdy.as_string())
        





# customer support => one get endpoint, one post endpoint (acquiring customer feedback, posting email reponses from admin)
def customer_supppppprrtttt( HELP):
  
    # TODO
    pass

@app.route( methods = ['POST'])
def customer_email_display():
    # TODO
    pass

@app.route(methods = ['GET'])
def uhh():
    # TODO
    pass


# customer feedback
# => customer support issues

    


## define message format, message body etc...
# postman
# twillio


def connect_db():
    """ Function to connect to MySQL database hosted in Docker container """
    cnx = mysql.connect(
        user='user', 
        password='password', 
        database='mysql',
        host='localhost', 
        port=3306
    )
    return cnx


def execute_db_query(query, args=(), one=False):
    """ Function to perform sanitized database queries """
    db_cnx = connect_db()
    cursor = db_cnx.cursor(dictionary=True)
    cursor.execute(query, args)

    if query.lower().startswith("select"):
        rows = cursor.fetchall()
    else:
        rows = None

    db_cnx.commit()
    cursor.close()
    if rows:
        if one:
            return rows[0]
        return rows
    return None



#####Eric's example

# class APIResponse:
#     """ Define a class for structuring API responses"""
#     def __init__(self, data, status):
#         self.data = data
#         self.status = status


# @app.route('/api/accounts/admin/list', methods=['GET'])
# def get_users():
#     """ Get all users for admins to view """  
#     # create Admin instance and get all users
#     admin = Admin()
#     api_response = admin.list_users()
#     return api_response.data, api_response.status







if __name__ == "__main__":
    # run notifications Flask service on port 3900
    app.run(port=7777, debug=True, host='0.0.0.0')

    # testing_basic_email_send("bigcheddarchees@gmail.com")
    # # testing with placeholder
    # recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    # auction_name = "Hazzah"
    # # testing with placeholder


    # email_subject = f"You have been out-bid for auction: {auction_name}"
    # email_body = f'''
    # <html>
    #     <body>
    #         <h1>your previous high-bid for auction: {auction_name} has been out-bid</h1>
    #         <br>
    #         <p>Please submit a new bid higher than the current high-bid to secure your auction-win</p>
    #         <br>
    #         <p>Sincerely, TimePiece Traders</p>
    #         <br>
    #         <p>This is an automated email. Please don't respond to this email</p>

    #     </body>
    # </html>
    # '''

    # send_email(recipients, email_subject, email_body)







# # this works (TESTING & TROLLING PURPOSES)
# def testing_basic_email_send(email_to):

#     email_from = "kingboggerbob@gmail.com"
#     # pw = "tlqkf1234"
#     pw = "dybsolarponjdsin"

#     # plain text string to be sent as email message
#     email_string = "Would you like to buy a brand new ToyYoda for $9.72?! Click in the link below!\nhttps://poopsenders.com/"
    

#     # context = ssl.create_default_context()

#     with smtplib.SMTP("smtp.gmail.com", 587) as server:
#         server.starttls()
#         server.login(email_from, pw)

#         # send mail
#         server.sendmail(email_from, email_to, email_string)


#     # with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as server:
#     #     server.login(email_from, pw)

#     #     # send mail
#     #     server.sendmail(email_from, email_to, email_string)