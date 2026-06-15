from flask import Flask, render_template_string, request, redirect, session
import bcrypt

app = Flask(__name__)
app.secret_key = "secretkey"

# Temporary database
users = {}

# Home Page
@app.route("/")
def home():
    if "user" in session:
        return f"""
        <h2>Welcome {session['user']}</h2>
        <a href='/logout'>Logout</a>
        """
    return redirect("/login")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Hash password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users[username] = hashed

        return "Registration Successful! <a href='/login'>Login</a>"

    return """
    <h2>Register</h2>
    <form method='POST'>
        Username: <input type='text' name='username'><br><br>
        Password: <input type='password' name='password'><br><br>
        <input type='submit' value='Register'>
    </form>
    """

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check user
        if username in users:
            if bcrypt.checkpw(password.encode('utf-8'), users[username]):
                session["user"] = username
                return redirect("/")

        return "Invalid Username or Password"

    return """
    <h2>Login</h2>
    <form method='POST'>
        Username: <input type='text' name='username'><br><br>
        Password: <input type='password' name='password'><br><br>
        <input type='submit' value='Login'>
    </form>
    <br>
    <a href='/register'>Register</a>
    """

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# Run app
if __name__ == "__main__":
    app.run(debug=True)
