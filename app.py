from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import timedelta

# Create Flask App
app = Flask(__name__)

# Secret Key (for sessions)
app.secret_key = "supersecretkey"

# Session timeout (5 minutes)
app.permanent_session_lifetime = timedelta(minutes=5)

# Dummy users (Login Credentials)
USER_CREDENTIALS = {
    "siddhart": "1927",
    "rishav": "5023"
}

# =========================
# Chatbot Logic
# =========================
def get_response(user_input):
    user_input = user_input.lower()

    if "fees" in user_input:
        return "Our monthly membership starts at ₹1500."

    elif "timing" in user_input:
        return "We are open from 5 AM to 10 PM."

    elif "trainer" in user_input:
        return "Yes, personal trainers are available."

    elif "location" in user_input:
        return "We are located opposite Royal Enfield, KIIT Square."

    elif "contact" in user_input:
        return "You can call us at 8539921928."

    elif "ceo" in user_input:
        return "Mr. Siddhart Pandey is the Founder and CEO of PowerFit Gym."

    else:
        return "Please ask about fees, timing, trainer, location, contact or CEO."


# =========================
# Home Route
# =========================
@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html")
    return redirect(url_for("login"))


# =========================
# Login Route
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session.permanent = True
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid credentials"

    return render_template("login.html")


# =========================
# Logout Route
# =========================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# =========================
# Chat API Route
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    if "user" not in session:
        return jsonify({"response": "Unauthorized"})

    user_message = request.json["message"]
    return jsonify({"response": get_response(user_message)})


# =========================
# Run App
# =========================
if __name__ == "__main__":
    app.run(debug=True)
