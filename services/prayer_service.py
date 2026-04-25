from db.connection import get_connection

def get_today_prayers(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if record exists
    cursor.execute("""SELECT * FROM prayer_logs WHERE user_id = %s AND date = CURRENT_DATE """,
        (user_id,))

    record = cursor.fetchone()

    # If not exists → create empty row
    if not record:
        cursor.execute( """INSERT INTO prayer_logs (user_id, date) VALUES (%s, CURRENT_DATE) RETURNING * """,
            (user_id,))
        record = cursor.fetchone()
        conn.commit()

    conn.close()
    return record


def update_prayer(user_id: int, prayer: str, status: str):
    conn = get_connection()
    cursor = conn.cursor()

    # dynamic column update (safe because controlled input)
    query = f"""UPDATE prayer_logs SET {prayer} = %s WHERE user_id = %s AND date = CURRENT_DATE RETURNING * """

    cursor.execute(query, (status, user_id))
    updated = cursor.fetchone()

    conn.commit()
    conn.close()

    return updated