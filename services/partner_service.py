from db.connection import get_connection


def link_partner(user_id: int, partner_email: str):
    conn = get_connection()
    cursor = conn.cursor()

    # find partner
    cursor.execute("SELECT id FROM users WHERE email = %s",(partner_email,))
    partner = cursor.fetchone()

    if not partner:
        conn.close()
        return {"error": "User not found"}

    partner_id = partner["id"]

    # update both users
    cursor.execute("UPDATE users SET partner_id = %s WHERE id = %s",(partner_id, user_id))
    cursor.execute("UPDATE users SET partner_id = %s WHERE id = %s",(user_id, partner_id))

    conn.commit()
    conn.close()

    return {"message": "Partner linked successfully"}


def get_partner_dashboard(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # get partner
    cursor.execute("SELECT partner_id FROM users WHERE id = %s",(user_id,))
    result = cursor.fetchone()

    if not result or not result["partner_id"]:
        conn.close()
        return {"error": "No partner linked"}

    partner_id = result["partner_id"]

    # get both prayer data
    cursor.execute("""SELECT user_id, fajr, dhuhr, asr, maghrib, isha FROM prayer_logs
        WHERE user_id IN (%s, %s) AND date = CURRENT_DATE """, (user_id, partner_id))

    prayers = cursor.fetchall()

    # get routines
    cursor.execute("""SELECT r.user_id, r.routine_name,COALESCE(rl.status, FALSE) as status FROM routines r
                LEFT JOIN routine_logs rl ON r.id = rl.routine_id AND rl.date = CURRENT_DATE
                WHERE r.user_id IN (%s, %s)
                """,(user_id, partner_id))

    routines = cursor.fetchall()

    conn.close()

    return {"prayers": prayers,"routines": routines
    }