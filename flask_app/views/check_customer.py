from flask import (Flask, Blueprint, render_template, request, 
                  session, redirect, url_for, make_response)
from flask_app import db

# blueprint 선언
bp_check_customer = Blueprint("check_customer", __name__)

@bp_check_customer.route("/check_customer", methods=["POST", "GET"])
def check_customer():

    if request.method == "GET":
        return render_template("main_check_customer.html")

    # 데이터를 전달받을 때
    elif request.method == "POST":

        flight_search = request.form["flight_search"]

        from flask_app.models.flight_status import Flight_status
        flight_info = Flight_status.query.filter_by(flight = flight_search).first()

        ## DB에 flight_info가 없다면
        if flight_info is None:
            result = "항공편 정보가 없습니다. 다시 입력해주십시오."
            return render_template("main_check_customer.html", result = result)
        
        ## DB에 flight_info가 있다면
        else:

            # 데이터 풀기
            flight = flight_info.flight
            airport_ori = flight_info.airport_ori
            airport_des = flight_info.airport_des
            prediction = flight_info.anal_result


            # 데이터 해석하기
            if prediction == 0:
                predict_result_meaning = "결항"
            elif prediction == 1:
                predict_result_meaning = "지연"
            else:
                predict_result_meaning = "정상"

            doc = {
                    "flight": flight,
                    "airport_ori": airport_ori,
                    "airport_des": airport_des,
                    "prediction": predict_result_meaning,
                    }

            return render_template("main_check_customer.html", doc = doc)


# blueprint 선언
bp_delete_flight = Blueprint("delete_flight", __name__)

@bp_delete_flight.route("/check_customer/<flight>")
def delete_flight(flight):

    from flask_app.models.flight_status import Flight_status

    delete_flight = Flight_status.query.filter_by(flight = flight).first()
        
    # DB 저장 등록
    db.session.delete(delete_flight)

    # 반영하기
    db.session.commit()

    return redirect(url_for("check_customer.check_customer"))




import json
import requests

# blueprint 선언
bp_send_msg = Blueprint("send_msg", __name__)


@bp_send_msg.route("/send_msg/<flight>")
def send_msg(flight):

    # 1. 항공편 조회하기
    from flask_app.models.flight_status import Flight_status

    flight_info = Flight_status.query.filter_by(flight = flight).first()

    # 2. 항공편 예상 정보 조회하기
    
    
    # 데이터 풀기
    flight = flight_info.flight
    airport_ori = flight_info.airport_ori
    airport_des = flight_info.airport_des
    prediction = flight_info.anal_result
    
    # 데이터 해석하기
    if flight_info.anal_result == 0:
        status = "결항"
    elif flight_info.anal_result == 1:
        status = "지연"
    else:
        status = "정상"

    if airport_ori == "RKSS":
        airport_ori_korean = "김포국제공항"
    elif airport_ori == "RKPC":
        airport_ori_korean = "제주국제공항"
    elif airport_ori == "RKPK":
        airport_ori_korean = "김해국제공항"

    if airport_des == "RKSS":
        airport_des_korean = "김포국제공항"
    elif airport_des == "RKPC":
        airport_des_korean = "제주국제공항"
    elif airport_des == "RKPK":
        airport_des_korean = "김해국제공항"

    # 3. 카톡 보내기

    # POST /v2/api/talk/memo/default/send HTTP/1.1
    # Host: kapi.kakao.com
    # Authorization: Bearer {ACCESS_TOKEN}

    # url_token = "https://kauth.kakao.com/oauth/token"

    # code = "0x5E_F3SjF9atxrWns5QVAGTTARsBAFMNQJBkDLSxJpLvjWdXP9Gm6aZa1J9ad8GNjUUdQo9c5oAAAF4eApQnA"

    # data_token = {
    # "grant_type":"authorization_code",
    # "client_id":"4a616087b1e8515fa16f16602b7d1773",
    # "redirect_url":"https://companycustomermanage.herokuapp.com/",
    # "code":code
    # }

    # response_token = requests.post(url_token, data=data_token)

    # token = response_token.json()

    # print(token)

    token = "OA-6VkcPdl-cSKPHdXXnb1roChp_1ybiPVnfEgorDKYAAAF4fM8AHg"

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    # 사용자 토큰
    headers = {
        # "Authorization": "Bearer " + token["access_token"]
        "Authorization": "Bearer " + token
    }


    data = {
        "template_object" : json.dumps({ "object_type" : "text",
                                        "text" : f"[대한항공 - 운항 안내] \n\n ▶ {status} 안내: 17시 출발 예정이었던 {flight}편({airport_ori_korean}발 {airport_des_korean}행)은 {status} 출발 예정입니다. \n\n ▶ {status} 사유: 도착 공항 기상 악화. \n\n ▶ 재안내: 기상 상황이 개선되는대로 문자를 통해 탑승수속 및 탑승구 정보를 안내드리겠습니다.  \n\n ▶ 이용에 불편을 드려 대단히 죄송합니다.",     
                                        "link": {"web_url": "www.naver.com"}
        })
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)

    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
        result_msg = "전송 완료"
    
        ## DB에 flight_info가 없다면
        if flight_info is None:
            result = "항공편 정보가 없습니다."
            return render_template("main_check_customer.html", result = result)
        
        ## DB에 flight_info가 있다면
        else:

            # # 데이터 풀기
            # flight = flight_info.flight
            # airport_ori = flight_info.airport_ori
            # airport_des = flight_info.airport_des
            # prediction = flight_info.anal_result


            # 데이터 해석하기
            if prediction == 0:
                predict_result_meaning = "결항"
            elif prediction == 1:
                predict_result_meaning = "지연"
            else:
                predict_result_meaning = "정상"

            doc = {
                    "flight": flight,
                    "airport_ori": airport_ori,
                    "airport_des": airport_des,
                    "prediction": predict_result_meaning,
                    }

            result_msg = "안내 문자 전송 완료"
            result_alert = "문자 전송이 완료되었습니다."

            return render_template("main_check_customer.html", doc = doc, result_msg = result_msg, result_alert = result_alert)
        # return redirect(url_for("check_customer.check_customer"))

    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))
        return redirect(url_for("check_customer.check_customer"))
        # return render_template("main_check_customer.html", doc = doc, result_msg = result_msg)
