from flask import (Flask, Blueprint, render_template, request, 
                  session, redirect, url_for, make_response)
from flask_app import db
from random import *
from flask_app.services.regression import *
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# blueprint 선언
bp_check_status = Blueprint("check_status", __name__)


@bp_check_status.route("/check_status", methods=["POST", "GET"])
def check_status():
        
        if request.method == "GET":
            return render_template("main_check_status.html")

        # 데이터를 전달받을 때
        elif request.method == "POST":

            def unpack_data_input():

                # 전달받은 데이터 풀기 및 변수 선언하기
                flight = request.form["flight"]
                airport_ori = request.form["airport_ori"].split("(")[0]
                airport_des = request.form["airport_des"].split("(")[0]
                eta = request.form["eta"]

                return flight, airport_ori, airport_des, eta

            flight, airport_ori, airport_des, eta = unpack_data_input()

            # DB 저장할 데이터 선언하기
            from flask_app.models.user import User
            from flask_app.models.weather import Weather 
            from flask_app.models.flight_status import Flight_status

            new_weather = Weather(time = str(eta), rvr = randrange(3), wind = randrange(3), cloud = randrange(3))
            # DB 저장 등록
            db.session.add(new_weather)
            # 반영하기
            db.session.commit()


            # DB에서 데이터 불러오기
            weather_info = Weather.query.filter_by(time = str(eta)).first()

            # DB 풀기 및 변수 생성하기
            def unpack_data_weather():

                # 전달받은 데이터 풀기 및 변수 선언하기
                rvr_des = weather_info.rvr
                wind_des = weather_info.wind
                cloud_des = weather_info.cloud

                return rvr_des, wind_des, cloud_des

            rvr_des, wind_des, cloud_des = unpack_data_weather()
            
            


            # 데이터 입력하지 않았을 경우
            if len(flight) == 0 or len(airport_ori) == 0 or len(airport_des) == 0 or len(eta) == 0:
                
                result = "정보가 누락되었습니다. 다시 입력해주세요."

                return render_template("main_check_status.html", result)
        

            # 데이터 입력한 경우 
            else:

                print(f"rvr_des: {rvr_des}")
                print(f"wind_des: {wind_des}")
                print(f"cloud_des: {cloud_des}")

                print(f"flight: {flight}")
                print(f"airport_ori: {airport_ori}")
                print(f"airport_des: {airport_des}")
                print(f"eta: {eta}")

                ## machinelearning
                # 2-1. 훈련 데이터 불러오기
                df = pd.read_csv('flight_data_copy_csv_practice.csv')

                # 2-2. 데이터 분리하기
                target = "target"

                X_train = df.drop(columns=target)
                y_train = df[target]

                # 2-3. randomforest 인스턴스 선언하기
                model_rf = RandomForestClassifier(random_state=1)

                # 2-4. 학습하기
                model_rf.fit(X_train, y_train)

                test_dict = {"rvr": rvr_des, "wind": wind_des, "cloud": cloud_des}
                X_test = pd.DataFrame(test_dict, index=[0])
                
                prediction = model_rf.predict(X_test)
                print(f"prediction: {prediction[0]}")
                prediction_int = int(prediction[0])

                # DB에 저장하기
                # DB 저장할 데이터 선언하기
                new_flight_status = Flight_status(flight = flight, airport_ori = airport_ori,
                                                  airport_des = airport_des, eta = eta,
                                                  anal_result = prediction_int)
                # DB 저장 등록
                db.session.add(new_flight_status)
                
                # 반영하기
                db.session.commit()

                # prediction 숫자 해석하기
                if prediction_int == 0:
                    predict_result_meaning = "결항"
                elif prediction_int == 1:
                    predict_result_meaning = "지연"
                else:
                    predict_result_meaning = "정상"

                return render_template("main_check_status.html", prediction = predict_result_meaning, flight = flight)