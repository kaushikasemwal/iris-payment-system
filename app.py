from flask import Flask, request, jsonify
from flask_cors import CORS
from iris_auth import register_user, authenticate_iris
from stripe_payment import process_payment

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Iris Payment API!"})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data["name"]
    image_path = data["image_path"]
    stripe_customer_id = data["stripe_customer_id"]

    register_user(name, image_path, stripe_customer_id)
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    image_path = data["image_path"]
    
    customer_id = authenticate_iris(image_path)
    if customer_id:
        return jsonify({"authenticated": True, "customer_id": customer_id}), 200
    return jsonify({"authenticated": False}), 401

@app.route('/pay', methods=['POST'])
def pay():
    data = request.json
    customer_id = data["customer_id"]
    amount = data["amount"]

    payment_status = process_payment(customer_id, amount)
    return jsonify({"message": "Payment Successful", "status": payment_status}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)  # Updated for deployment
