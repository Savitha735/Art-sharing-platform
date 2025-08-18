from flask import render_template, request, redirect, session
from . import auth_bp
from supabase_client import supabase
from gotrue.errors import AuthApiError


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        username= request.form["username"]

        try:
            res = supabase.auth.sign_up({
                "email": email,
                "password": password,
                  "options": {
                "data": {   # custom user metadata
                "username": username
            }}
            })

            # If sign up succeeded
            if res.user:
                return redirect("/auth/login")  # redirect to login page after signup
            else:
                return "Signup failed"

        except Exception as e:
            return f"Error: {str(e)}"

    # If GET request, show form
    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if res.user:
                session["user"] = res.user.email
                return redirect("/")
            else:
                return "Invalid login"

        except AuthApiError as e:
            return f"Auth error: {e.message}"
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/auth/login")
