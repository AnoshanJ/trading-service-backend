from flask import Flask, jsonify, request
import os

app = Flask(__name__)

trades = []
debug_mode = os.getenv('FLASK_DEBUG_MODE', 'False').lower() == 'true'
app.config['DEBUG'] = debug_mode


# Helper function to generate IDs
def generate_id():
    return len(trades) + 1


# Endpoint to get all trades
@app.route('/trading/trades', methods=['GET'])
def get_trades():
    return jsonify({'trades': trades})


# Endpoint to add a new trade
@app.route('/trading/trades', methods=['POST'])
def add_trade():
    data = request.get_json()
    trade = {
        'id': generate_id(),
        'stock_symbol': data['stock_symbol'],
        'price': data['price'],
        'quantity': data['quantity'],
        'trade_type': data['trade_type']  # 'buy' or 'sell'
    }
    trades.append(trade)


# Endpoint to get a trade by ID
@app.route('/trading/trades/<int:trade_id>', methods=['GET'])
def get_trade(trade_id):
    for trade in trades:
        if trade['id'] == trade_id:
            return jsonify(trade)
    return '', 404


# Endpoint to delete a trade by ID
@app.route('/trading/trades/<int:trade_id>', methods=['DELETE'])
def delete_trade(trade_id):
    global trades
    trades = [trade for trade in trades if trade['id'] != trade_id]
    return '', 204


# Endpoint to update a trade by ID
@app.route('/trading/trades/<int:trade_id>', methods=['PUT'])
def update_trade(trade_id):
    data = request.get_json()
    for trade in trades:
        if trade['id'] == trade_id:
            trade['price'] = data.get('price', trade['price'])
            trade['quantity'] = data.get('quantity', trade['quantity'])
            return jsonify(trade)
    return '', 404


if __name__ == '__main__':
    app.run()
