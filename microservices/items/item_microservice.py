from flask import Flask, request, jsonify

from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3500"}})


class APIResponse:
    """ Define a class for structuring API responses"""

    def __init__(self, data, status):
        self.data = data
        self.status = status

    def to_flask_response(self):
        return jsonify(self.data), self.status


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=6001,  # the port exposed in Docker
        user="user",
        password="password",
        database="mysql"
    )


@app.route('/api/item/add_item', methods=['POST'])
def add_item():
    """
    Add a new item.
    Expects a JSON with 'user_id', 'item_name', 'description', 'watch_reference_number', 
    'watch_model', 'watch_year', 'brand', 'item_condition', 'auction_won', 
    'starting_price', 'bid_amount', 'auction_start', 'auction_deadline'.
    """
    data = request.get_json()
    required_fields = ['user_id', 'item_name', 'description', 'watch_reference_number',
                       'watch_model', 'watch_year', 'brand', 'item_condition', 'auction_won',
                       'starting_price', 'bid_amount', 'auction_start', 'auction_deadline']
    if not all(field in data for field in required_fields):
        return APIResponse("Missing parameters", 400).to_flask_response()

    # Extract fields from data
    values = tuple(data[field] for field in required_fields)

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = """
    INSERT INTO items (user_id, item_name, description, watch_reference_number, 
                       watch_model, watch_year, brand, item_condition, auction_won, 
                       starting_price, bid_amount, auction_start, auction_deadline)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql_query, values)
    db_connection.commit()
    item_id = cursor.lastrowid
    cursor.close()
    db_connection.close()
    return APIResponse({"item_id": item_id}, 200).to_flask_response()


@app.route('/api/item/update_item', methods=['POST'])
def update_item():
    """ Update an item """
    data = request.get_json()
    item_id = data.get('item_id')
    if not item_id:
        return APIResponse("Missing item_id", 400).to_flask_response()

    update_fields = []
    values = []
    for field in ['bid_amount', 'starting_price', 'item_name', 'description', 'watch_model', 'watch_reference_number', 'item_condition', 'auction_start', 'auction_deadline']:
        if field in data:
            update_fields.append(f"{field} = %s")
            values.append(data[field])

    if not update_fields:
        return APIResponse("No update parameters provided", 400).to_flask_response()

    values.append(item_id)  # Append item_id for WHERE clause

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = f"UPDATE items SET {', '.join(update_fields)} WHERE id = %s"
    cursor.execute(sql_query, tuple(values))
    db_connection.commit()
    cursor.close()
    db_connection.close()

    return APIResponse({}, 200).to_flask_response()


@app.route('/api/item/delete_item', methods=['DELETE'])
def delete_item():
    """ Delete an item """
    data = request.get_json()
    item_id = data['item_id']

    if not item_id:
        return APIResponse("Missing parameters", 400)

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "DELETE FROM items WHERE item_id = %s"
    cursor.execute(sql_query, (item_id,))
    db_connection.commit()
    cursor.close()
    db_connection.close()
    return APIResponse({}, 200).to_flask_response()


@app.route('/api/item/get_item', methods=['GET'])
def get_item():
    """ Get an item by id """
    item_id = request.args.get('id')
    if not item_id:
        return APIResponse("Missing parameters", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "SELECT * FROM items WHERE id = %s"
    cursor.execute(sql_query, (item_id,))
    item_data = cursor.fetchone()
    cursor.close()
    db_connection.close()
    if not item_data:
        return APIResponse("Item not found", 404).to_flask_response()
    return APIResponse(item_data, 200).to_flask_response()


@app.route('/api/item/search', methods=['GET'])
def search_items():
    search_query = request.args.get('query')
    if not search_query:
        return APIResponse("Missing search query", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    sql_query = "SELECT * FROM items WHERE item_name REGEXP %s OR description REGEXP %s OR brand REGEXP %s"
    cursor.execute(sql_query, (search_query, search_query, search_query))
    results = cursor.fetchall()

    cursor.close()
    db_connection.close()

    return APIResponse(results, 200).to_flask_response()


@app.route('/api/item/filter_by_brand', methods=['GET'])
def filter_by_brand():
    brand_query = request.args.get('brand')
    if not brand_query:
        return APIResponse("Missing brand query", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    sql_query = "SELECT * FROM items WHERE brand = %s"
    cursor.execute(sql_query, (brand_query,))
    results = cursor.fetchall()

    cursor.close()
    db_connection.close()

    return APIResponse(results, 200).to_flask_response()


@app.route('/api/item/add_brand', methods=['POST'])
def add_brand():
    data = request.get_json()
    brand_name = data['brand_name']

    if not brand_name:
        return APIResponse("Missing brand name", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "INSERT INTO brands (brand_name) VALUES (%s)"
    cursor.execute(sql_query, (brand_name,))
    db_connection.commit()
    brand_id = cursor.lastrowid
    cursor.close()
    db_connection.close()

    return APIResponse({}, 200).to_flask_response()


@app.route('/api/item/update_brand', methods=['POST'])
def update_brand():
    data = request.get_json()
    brand_id = data['brand_id']
    new_brand_name = data['new_brand_name']

    if not all([brand_id, new_brand_name]):
        return APIResponse("Missing parameters", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "UPDATE brands SET brand_name = %s WHERE brand_id = %s"
    cursor.execute(sql_query, (new_brand_name, brand_id))
    db_connection.commit()
    cursor.close()
    db_connection.close()

    return APIResponse({}, 200).to_flask_response()


@app.route('/api/item/delete_brand', methods=['DELETE'])
def delete_brand():
    data = request.get_json()
    brand_id = data['brand_id']

    if not brand_id:
        return APIResponse("Missing brand ID", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "DELETE FROM brands WHERE brand_id = %s"
    cursor.execute(sql_query, (brand_id,))
    db_connection.commit()
    cursor.close()
    db_connection.close()

    return APIResponse(f"Successfully deleted brand ID {brand_id}", 200)


@app.route('/api/item/get_brands', methods=['GET'])
def get_brands():
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "SELECT * FROM brands"
    cursor.execute(sql_query)
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return APIResponse(results, 200).to_flask_response()


@app.route('/api/item/add_purchase', methods=['POST'])
def add_purchase():
    data = request.get_json()
    user_id = data['user_id']
    item_id = data['item_id']
    status = data['status']
    purchase_date = data['purchase_date']

    if not all([user_id, item_id, status, purchase_date]):
        return APIResponse("Missing parameters", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "INSERT INTO user_purchases (user_id, item_id, status, purchase_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql_query, (user_id, item_id, status, purchase_date))
    db_connection.commit()
    purchase_id = cursor.lastrowid
    cursor.close()
    db_connection.close()

    return APIResponse({}, 200).to_flask_response()


@app.route('/api/item/update_purchase', methods=['POST'])
def update_purchase():
    data = request.get_json()
    purchase_id = data['purchase_id']
    new_status = data['new_status']

    if not all([purchase_id, new_status]):
        return APIResponse("Missing parameters", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "UPDATE user_purchases SET status = %s WHERE purchase_id = %s"
    cursor.execute(sql_query, (new_status, purchase_id))
    db_connection.commit()
    cursor.close()
    db_connection.close()

    return APIResponse(f"Successfully updated purchase ID {purchase_id}", 200).to_flask_response()


@app.route('/api/item/delete_purchase', methods=['DELETE'])
def delete_purchase():
    data = request.get_json()
    purchase_id = data['purchase_id']

    if not purchase_id:
        return APIResponse("Missing purchase ID", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "DELETE FROM user_purchases WHERE purchase_id = %s"
    cursor.execute(sql_query, (purchase_id,))
    db_connection.commit()
    cursor.close()
    db_connection.close()

    return APIResponse(f"Successfully deleted purchase ID {purchase_id}", 200).to_flask_response()


# Add item to user_purchases.
# Frontend: Buy Now, Checkout
# Auction Microservice: Listen for messages from auction microservice to add item to user_purchases
#   build endpoint & rabbitmq consumer


if __name__ == "__main__":
    app.run(port=3901, debug=True, host='0.0.0.0')
