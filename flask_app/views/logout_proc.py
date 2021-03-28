from flask import (Flask, Blueprint, render_template, request, 
                  session, redirect, url_for, make_response)
from flask_app import db


# blueprint 선언
bp_logout_proc = Blueprint("logout_proc", __name__)

# 로그 아웃 과정
@bp_logout_proc.route("/logout_proc")
def logout_proc():
    
    session["logFlag"] = False
    session.pop("userId", None)
    session.clear

    return redirect(url_for("index"))