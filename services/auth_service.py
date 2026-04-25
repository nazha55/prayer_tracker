from db.connection import get_connection
from utils.security import create_token, hash_password, verify_password


def register_user(data):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE email = %s",(data.email,)
    )
    if cursor.fetchone():
        conn.close()
        return {"error": "User already exists"}

    hashed_password = hash_password(data.password)

    cursor.execute("""INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id""",
                (data.name, data.email, hashed_password))

    user_id = cursor.fetchone()["id"]

    conn.commit()
    conn.close()

    token = create_token(user_id, data.email)

    return {"token": token}


def login_user(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s",(data.email,))
    user = cursor.fetchone()

    conn.close()

    if not user:
        return {"error": "Invalid credentials"}

    if not verify_password(data.password, user["password"]):
        return {"error": "Invalid credentials"}

    token = create_token(user["id"], user["email"])

    return {"token": token}