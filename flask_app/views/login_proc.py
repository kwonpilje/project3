from flask import (Flask, Blueprint, render_template, request, 
                  session, redirect, url_for, make_response)
from flask_app import db


# blueprint 선언
bp_login_proc = Blueprint("login_proc", __name__)

# 로그인 정보 전달 받기 및 페이지 이동
@bp_login_proc.route("/login_proc", methods=["POST", "GET"])
def login_proc():

    # 데이터를 전달받을 때
    if request.method == "POST":

        # 전달받은 데이터 풀기 및 변수 선언하기
        userId = request.form["id"]
        userPwd = request.form["pwd"]

        # 데이터 입력하지 않았을 경우
        if len(userId) == 0 or  len(userPwd) == 0:
            return "userId 또는 userPwd가 존재하지 않습니다."
        
        # 데이터 입력한 경우 
        else:
            from flask_app.models.user import User
            
            # DB에서 데이터 불러오기
            user_info = User.query.filter_by(username = userId).first()
            
            # 아이디가 없을 경우: 자동 회원가입
            if user_info is None:
                
                # DB 저장할 데이터 선언하기
                new_user = User(username = userId, password = userPwd)

                # DB 저장 등록
                db.session.add(new_user)

                # 반영하기
                db.session.commit()

                return render_template("login_form.html")
            

            # 아이디가 있을 경우
            else:
                # 입력한 정보와 DB 정보 비교 및 확인하기(정보 일치할 경우)
                if userId == user_info.username and userPwd == user_info.password:
                    
                    # 세션 등록하기(login 정보, id, userId)
                    session["logFlag"] = True
                    session["idx"] = user_info.id
                    session["userId"] = userId

                    # 메인 페이지로 접속하기
                    return redirect(url_for("check_status.check_status"))
                
                else:
                    # 입력한 정보와 DB 정보 비교 및 확인하기(정보 불일치할 경우)
                    return redirect(url_for("login_form"))

    else:
        return "잘못된 접근입니다."