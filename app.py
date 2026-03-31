from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

FILE_NAME = "users.txt"


# Function to save user data
def save_user(username, password):
    with open(FILE_NAME, "a") as file:
        file.write(f"{username},{password}\n")


# Function to check if user already exists
def user_exists(username):
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(",")
                if stored_username == username:
                    return True
    except FileNotFoundError:
        pass
    return False


# Function to validate login
def validate_user(username, password):
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(",")
                if stored_username == username and stored_password == password:
                    return True
    except FileNotFoundError:
        pass
    return False


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if user_exists(username):
            message = "User already exists! Please login."
        else:
            save_user(username, password)
            message = "Registration successful! Now login."

    return render_template("register.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if validate_user(username, password):
            message = "Login successful!"
        else:
            message = "Invalid username or password!"

    return render_template("login.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)