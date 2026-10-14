from flask import Flask, render_template, request, redirect, flash, jsonify
import mysql.connector
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "gym_secret_key_change_me"

# ---------- MySQL connection helper ----------
def get_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jai231206",
        database="gym_db"
    )

# ---------- MongoDB connection ----------
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["gym_db"]
workout_col = mongo_db["workout_plans"]
feedback_col = mongo_db["feedback"]
preset_col = mongo_db["presets"]


# ============================================================
# DASHBOARD
# ============================================================
@app.route("/")
def dashboard():
    db = get_mysql()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT COUNT(*) AS total FROM members")
    total_members = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM members WHERE status='Active'")
    active_members = cur.fetchone()["total"]

    cur.execute("SELECT IFNULL(SUM(amount),0) AS total FROM payments")
    total_revenue = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM plans")
    total_plans = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM trainers")
    total_trainers = cur.fetchone()["total"]

    cur.close()
    db.close()

    total_feedback = feedback_col.count_documents({})
    avg_result = list(feedback_col.aggregate([
        {"$group": {"_id": None, "avgRating": {"$avg": "$rating"}}}
    ]))
    avg_rating = round(avg_result[0]["avgRating"], 2) if avg_result else 0

    return render_template("dashboard.html",
                           total_members=total_members,
                           active_members=active_members,
                           total_revenue=total_revenue,
                           total_plans=total_plans,
                           total_trainers=total_trainers,
                           total_feedback=total_feedback,
                           avg_rating=avg_rating)


# ============================================================
# MEMBERS
# ============================================================
@app.route("/members")
def members():
    db = get_mysql()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM member_details ORDER BY member_id")
    members = cur.fetchall()

    cur.execute("SELECT plan_id, plan_name, price FROM plans ORDER BY plan_id")
    plans = cur.fetchall()

    cur.execute("SELECT trainer_id, name FROM trainers ORDER BY name")
    trainers = cur.fetchall()

    cur.close()
    db.close()

    return render_template("index.html",
                           members=members,
                           plans=plans,
                           trainers=trainers)


@app.route("/add_member", methods=["POST"])
def add_member():
    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form.get("email") or None
    plan_id = request.form["plan_id"] or None
    trainer_id = request.form.get("trainer_id") or None

    try:
        db = get_mysql()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO members (name, phone, email, join_date, plan_id, trainer_id)
            VALUES (%s, %s, %s, CURDATE(), %s, %s)
        """, (name, phone, email, plan_id, trainer_id))
        db.commit()
        cur.close()
        db.close()
        flash(f"Member '{name}' added successfully!")
    except mysql.connector.Error as e:
        flash(f"Error: {e}")
    return redirect("/members")


@app.route("/delete_member/<int:member_id>")
def delete_member(member_id):
    try:
        db = get_mysql()
        cur = db.cursor()
        cur.execute("DELETE FROM members WHERE member_id = %s", (member_id,))
        db.commit()
        cur.close()
        db.close()
        flash("Member deleted successfully!")
    except mysql.connector.Error as e:
        flash(f"Error: {e}")
    return redirect("/members")


# ============================================================
# PLANS
# ============================================================
@app.route("/plans")
def plans():
    db = get_mysql()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM plans ORDER BY plan_id")
    rows = cur.fetchall()
    cur.close()
    db.close()
    return render_template("plans.html", plans=rows)


@app.route("/add_plan", methods=["POST"])
def add_plan():
    plan_name = request.form["plan_name"]
    duration = request.form["duration"]
    price = request.form["price"]

    try:
        db = get_mysql()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO plans (plan_name, duration_months, price)
            VALUES (%s, %s, %s)
        """, (plan_name, duration, price))
        db.commit()
        cur.close()
        db.close()
        flash(f"Plan '{plan_name}' added successfully!")
    except mysql.connector.Error as e:
        flash(f"Error: {e}")
    return redirect("/plans")


@app.route("/delete_plan/<int:plan_id>")
def delete_plan(plan_id):
    try:
        db = get_mysql()
        cur = db.cursor()
        cur.execute("DELETE FROM plans WHERE plan_id = %s", (plan_id,))
        db.commit()
        cur.close()
        db.close()
        flash("Plan deleted successfully!")
    except mysql.connector.Error as e:
        flash(f"Error: {e}")
    return redirect("/plans")


# ============================================================
# TRAINERS
# ============================================================
@app.route("/trainers")
def trainers():
    db = get_mysql()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM trainers ORDER BY trainer_id")
    rows = cur.fetchall()
    cur.close()
    db.close()
    return render_template("trainers.html", trainers=rows)


@app.route("/add_trainer", methods=["POST"])
def add_trainer():
    name = request.form["name"]
    specialization = request.form["specialization"]
    phone = request.form["phone"]

    try:
        db = get_mysql()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO trainers (name, specialization, phone)
            VALUES (%s, %s, %s)
        """, (name, specialization, phone))
        db.commit()
        cur.close()
        db.close()
        flash(f"Trainer '{name}' added successfully!")
    except mysql.connector.Error as e:
        flash(f"Error: {e}")
    return redirect("/trainers")


@app.route("/delete_trainer/<int:trainer_id>")
def delete_trainer(trainer_id):
    try:
        db = get_mysql()
        cur = db.cursor()
        cur.execute("DELETE FROM trainers WHERE trainer_id = %s", (trainer_id,))
        db.commit()
        cur.close()
        db.close()
        flash("Trainer deleted successfully!")
    except mysql.connector.Error as e:
        flash(f"Error: {e}")
    return redirect("/trainers")


# ============================================================
# PAYMENTS
# ============================================================
@app.route("/payments")
def payments():
    db = get_mysql()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT p.payment_id, m.name AS member_name, p.amount,
               p.payment_date, p.mode
        FROM payments p
        JOIN members m ON p.member_id = m.member_id
        ORDER BY p.payment_date DESC
    """)
    rows = cur.fetchall()

    cur.execute("SELECT member_id, name FROM members ORDER BY name")
    member_list = cur.fetchall()

    cur.close()
    db.close()
    return render_template("payments.html", payments=rows, members=member_list)


@app.route("/add_payment", methods=["POST"])
def add_payment():
    member_id = request.form["member_id"]
    amount = request.form["amount"]
    mode = request.form["mode"]

    try:
        db = get_mysql()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO payments (member_id, amount, payment_date, mode)
            VALUES (%s, %s, CURDATE(), %s)
        """, (member_id, amount, mode))
        db.commit()
        cur.close()
        db.close()
        flash(f"Payment of Rs.{amount} recorded successfully!")
    except mysql.connector.Error as e:
        flash(f"Error: {e}")
    return redirect("/payments")


# ============================================================
# WORKOUTS
# ============================================================
@app.route("/workouts")
def workouts():
    plans = list(workout_col.find().sort("created_at", -1))
    goals = [p["goal"] for p in preset_col.find({}, {"goal": 1}).sort("goal", 1)]

    db = get_mysql()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT member_id, name FROM members ORDER BY name")
    member_list = cur.fetchall()

    cur.execute("SELECT trainer_id, name FROM trainers ORDER BY name")
    trainer_list = cur.fetchall()
    cur.close()
    db.close()

    return render_template("workouts.html",
                           plans=plans,
                           members=member_list,
                           trainers=trainer_list,
                           goals=goals)


@app.route("/get_presets/<goal>")
def get_presets(goal):
    preset = preset_col.find_one({"goal": goal})
    if preset:
        return jsonify({
            "goal": preset["goal"],
            "exercises": preset["exercises"],
            "difficulty": preset.get("difficulty", "N/A")
        })
    return jsonify({"exercises": []}), 404


@app.route("/add_workout", methods=["POST"])
def add_workout():
    member_id = int(request.form["member_id"])
    trainer_id = int(request.form["trainer_id"])
    goal = request.form["goal"]
    day = request.form["day"]
    exercises_raw = request.form["exercises"]

    exercises = [e.strip() for e in exercises_raw.split(",") if e.strip()]

    try:
        from datetime import date
        workout_col.insert_one({
            "member_id": member_id,
            "trainer_id": trainer_id,
            "goal": goal,
            "plan": [
                {"day": day, "exercises": exercises}
            ],
            "created_at": str(date.today())
        })
        flash("Workout plan assigned successfully!")
    except Exception as e:
        flash(f"Error: {e}")
    return redirect("/workouts")


# ============================================================
# PRESETS ADMIN
# ============================================================
@app.route("/presets")
def presets():
    all_presets = list(preset_col.find().sort("goal", 1))
    return render_template("presets.html", presets=all_presets)


@app.route("/add_preset", methods=["POST"])
def add_preset():
    goal = request.form["goal"]
    exercises_raw = request.form["exercises"]
    difficulty = request.form["difficulty"]
    exercises = [e.strip() for e in exercises_raw.split(",") if e.strip()]

    try:
        preset_col.insert_one({
            "goal": goal,
            "exercises": exercises,
            "difficulty": difficulty
        })
        flash(f"Preset '{goal}' added successfully!")
    except Exception as e:
        flash(f"Error: {e}")
    return redirect("/presets")


@app.route("/delete_preset/<preset_id>")
def delete_preset(preset_id):
    try:
        preset_col.delete_one({"_id": ObjectId(preset_id)})
        flash("Preset deleted successfully!")
    except Exception as e:
        flash(f"Error: {e}")
    return redirect("/presets")


# ============================================================
# FEEDBACK
# ============================================================
@app.route("/feedback")
def feedback():
    fb = list(feedback_col.find().sort("date", -1))
    avg_list = list(feedback_col.aggregate([
        {"$group": {"_id": None, "avgRating": {"$avg": "$rating"}}}
    ]))
    average = round(avg_list[0]["avgRating"], 2) if avg_list else 0

    db = get_mysql()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT member_id, name FROM members ORDER BY name")
    member_list = cur.fetchall()
    cur.close()
    db.close()

    return render_template("feedback.html",
                           feedback=fb,
                           average=average,
                           members=member_list)


@app.route("/add_feedback", methods=["POST"])
def add_feedback():
    member_id = int(request.form["member_id"])
    rating = int(request.form["rating"])
    comments = request.form["comments"]

    try:
        from datetime import date
        feedback_col.insert_one({
            "member_id": member_id,
            "rating": rating,
            "comments": comments,
            "date": str(date.today())
        })
        flash("Feedback submitted successfully!")
    except Exception as e:
        flash(f"Error: {e}")
    return redirect("/feedback")


# ============================================================
# ADMIN
# ============================================================
@app.route("/admin")
def admin():
    db = get_mysql()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM audit_log ORDER BY audit_id DESC LIMIT 20")
    logs = cur.fetchall()

    from datetime import date
    current_month = date.today().strftime("%Y-%m")
    cur.execute("""
        SELECT COUNT(*) AS cnt, IFNULL(SUM(amount), 0) AS total
        FROM payments
        WHERE DATE_FORMAT(payment_date, '%%Y-%%m') = %s
    """, (current_month,))
    revenue = cur.fetchone()

    cur.close()
    db.close()

    return render_template("admin.html",
                           logs=logs,
                           current_month=current_month,
                           revenue=revenue)


@app.route("/run_expire")
def run_expire():
    try:
        db = get_mysql()
        cur = db.cursor()
        cur.callproc("expire_memberships")
        db.commit()
        cur.close()
        db.close()
        flash("Expiration check complete — audit log updated.")
    except mysql.connector.Error as e:
        flash(f"Error: {e}")
    return redirect("/admin")


@app.route("/revenue/<month>")
def revenue(month):
    try:
        db = get_mysql()
        cur = db.cursor(dictionary=True)
        cur.callproc("monthly_revenue", [month])
        row = None
        for result in cur.stored_results():
            row = result.fetchone()
        cur.close()
        db.close()
        if row:
            flash(f"Revenue for {month}: Rs.{row['total_revenue']} ({row['payment_count']} payments)")
        else:
            flash(f"No data for {month}")
    except Exception as e:
        flash(f"Error: {e}")
    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)