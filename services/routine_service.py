from db.connection import get_connection


def create_routine(user_id: int, title: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO routines (user_id, routine_name) VALUES (%s, %s) RETURNING * """,
        (user_id, title))

    routine = cursor.fetchone()
    conn.commit()
    conn.close()

    return routine


def get_routines(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT r.id, r.routine_name,COALESCE(rl.status, FALSE) as status FROM routines r
                    LEFT JOIN routine_logs rl ON r.id = rl.routine_id AND rl.date = CURRENT_DATE
                    WHERE r.user_id = %s """,
                    (user_id,))

    routines = cursor.fetchall()
    conn.close()

    return routines


def toggle_routine(user_id: int, routine_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # check if exists
    cursor.execute("""SELECT * FROM routine_logs WHERE routine_id = %s AND user_id = %s AND date = CURRENT_DATE """,
        (routine_id, user_id))

    record = cursor.fetchone()

    if record:
        # toggle
        cursor.execute( """UPDATE routine_logs SET status = NOT status WHERE id = %s
            RETURNING * """,
            (record["id"],))
    else:
        # create new
        cursor.execute("""INSERT INTO routine_logs (routine_id, user_id, date, status) VALUES (%s, %s, CURRENT_DATE, TRUE)
            RETURNING *
            """,
            (routine_id, user_id)
        )

    updated = cursor.fetchone()
    conn.commit()
    conn.close()

    return updated