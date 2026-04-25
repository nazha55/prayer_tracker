from db.connection import get_connection


def get_prayer_history(user_id: int, days: int = 30):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute( f"""SELECT date,fajr, dhuhr, asr, maghrib, isha FROM prayer_logs
            WHERE user_id = %s AND date >= CURRENT_DATE - INTERVAL '{days} days'
            ORDER BY date ASC""",(user_id,))

    rows = cursor.fetchall()
    conn.close()

    # transform data for heatmap
    result = []

    for row in rows:
        prayers = [
            row["fajr"],
            row["dhuhr"],
            row["asr"],
            row["maghrib"],
            row["isha"]
        ]

        # calculate score
        score = sum(2 if p == "on_time" else 1 if p == "late" else 0 for p in prayers)
        result.append({
            "date": str(row["date"]),
            "score": score  # 0 to 5
        })

    return result