from flask import Flask, render_template, request, session, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from random import *
from flask_app.services.regression import *
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# flask_sqlalchemy 인스턴스 선언
db = SQLAlchemy()

# flask_migrate 인스턴스 선언
migrate = Migrate()

# factory화 수행
def create_app():
    
    # flask 구동 엔진 선언
    app = Flask(__name__)

    # 비밀번호 선언(세션 적용 시 사용)
    app.secret_key = "123456789987654321"

    # flask-db 연결
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite3"

    # 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # flask_sqlalchemy 구동 시작
    db.init_app(app)

    # flask_migrate 구동 시작
    migrate.init_app(app, db)

    # endpoint == "/" 일 경우 "login_form.html" 실행
    @app.route("/")
    def index():
        return render_template("login_form.html")


    # login 전체 절차(blueprint)
    from flask_app.views import login_proc
    app.register_blueprint(login_proc.bp_login_proc)


    # logout 전체 절차(blueprint)
    from flask_app.views import logout_proc
    app.register_blueprint(logout_proc.bp_logout_proc)


    # check_status 전체 절차(blueprint, ML 포함)
    from flask_app.views import check_status
    app.register_blueprint(check_status.bp_check_status)


    # check_customer 전체 절차(blueprint)
    from flask_app.views import check_customer
    app.register_blueprint(check_customer.bp_check_customer)


    # delete 전체 절차(blueprint)
    from flask_app.views import check_customer
    app.register_blueprint(check_customer.bp_delete_flight)


    # send_msg 전체 절차(blueprint)
    from flask_app.views import check_customer
    app.register_blueprint(check_customer.bp_send_msg)


    # 불러오기
    from flask_app.models.user import User
    from flask_app.models.weather import Weather 
    from flask_app.models.flight_status import Flight_status


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

