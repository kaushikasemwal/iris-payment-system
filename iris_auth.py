import sqlite3
import numpy as np
from scipy.spatial.distance import cosine
from iris_model import extract_iris_vector

DB_PATH = r"C:\Users\maitr\OneDrive\Documents\Kaushika\worspace\__MACOSX\eye"

def register_user(name, image_path, stripe_customer_id):
    """Registers a new user with their iris scan."""
    iris_vector = extract_iris_vector(image_path)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (name, iris_vector, stripe_customer_id) VALUES (?, ?, ?)", 
                   (name, iris_vector.tobytes(), stripe_customer_id))

    conn.commit()
    conn.close()
    print(f"✅ User {name} registered successfully!")

def authenticate_iris(image_path):
    """Authenticates a user by comparing iris vectors."""
    iris_vector = extract_iris_vector(image_path)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, iris_vector, stripe_customer_id FROM users")
    users = cursor.fetchall()
    conn.close()

    for user in users:
        stored_vector = np.frombuffer(user[2], dtype=np.float32)
        distance = cosine(iris_vector, stored_vector)

        if distance < 0.3:  # Threshold for similarity
            print(f"✅ User {user[1]} authenticated!")
            return user[3]  # Return Stripe customer ID

    print("❌ Authentication failed!")
    return None
