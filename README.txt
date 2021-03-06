1. 목표: 머신러닝을 이용한 항공편 운항 예측 및 고객 관리



2. 고려 사항
2-1. 사용 주체: 항공사 직원
2-2. 알림: 항공편 지연 및 결항 시, 해당 항공편 탑승객에게 해당 내용이 전달될 수 있는 메신저 사용 필요
2-3. 간편성: 직관적이고 사용하기 편리한 홈페이지 제작 필요



3. 제작: 3 종류 페이지
3-1. 로그인
 - 목적: 항공사 담당 직원만 항공편 정보에 접근하고 메시지를 전송하도록 보안 설정

3-2. 운항 관리
 - 목적: 머신러닝을 이용한 항공편 지연 및 결항 여부 예측
 - 예측 방법: 도착 공항 기상 정보(활주로 시정(RVR), 바람 세기(wind), 구름 양(cloud))를 활용한 지연 및 결항 예측

3-3. 고객 관리
 - 목적: 지연 및 결항 항공편 탑승객에게 운항 안내 메시지 전송 및 정보 삭제
 - 전송 방법: 카카오톡 메시지 전송



4. 구현
4-1. 로그인
 4-1-1. 현시
 - 입력창: 아이디, 비밀번호
 - 버튼: 로그인

 4-1-2. 기능
 - 입력창: 아이디와 비밀번호 입력
 - 버튼: 클릭 시 운항관리 페이지로 이동



4-2. 운항 관리
 4-2-1. 현시
 - 소개: 페이지 소개
 - 입력창: 항공편 정보(항공편명, 출발 공항, 도착 공항, 도착 예정 시간)
 - 버튼: 예측하기
 - 예측 결과: 2문장

 4-2-2. 기능
 - 소개: 없음
 - 입력창: 직접 입력(항공편명, 도착 예정 시간), 선택 입력(출발 공항, 도착 공항)
 - 버튼: 클릭 시 예측 결과 명시(동일 페이지)



4-3. 고객 관리
 4-3-1. 현시
 - 소개: 페이지 소개
 - 입력창: 항공편명
 - 버튼: 조회하기
 - 조회 결과: 2문장

 4-3-2. 기능
 - 소개: 없음
 - 입력창: 직접 입력
 - 버튼: 클릭 시 조회 결과 명시(동일 페이지)
 - 조회 결과: 표 명시(항공편 정보 4가지, 버튼(문자 보내기), 버튼(삭제))



5. 데이터 흐름
 5-1. 로그인
  ① (front-end) 아이디 및 비밀번호 입력
  ② (front-end) "로그인" 버튼 클릭
  ③ (back-end) 아이디 및 비밀번호 서버로 전달
  ④ (back-end) "로그인 "DB에서 아이디 조회하기 
  ⑤ (back-end) 아이디 존재하면, 입력 비밀번호와 DB 비밀번호 일치 여부 확인하기 
  ⑥ (back-end) 일치하면, 운항 관리 페이지로 이동하기

 5-2. 운항 관리
  ① (front-end) 항공편(4가지) 정보 입력 또는 선택
  ② (front-end) "예측하기" 버튼 클릭
  ③ (back-end) 4가지 정보 서버로 전달
  ④ (back-end) 도착 예정 시간(ETA)을 기준으로 "공항 기상 정보" DB에서 데이터 조회하기 
  ⑤ (back-end) 공항 기상 데이터(RVR, wind, cloud)를 머신러닝 모델에 입력하여 예측(predict)하기
  ⑥ (back-end) 5가지 정보(기존 4가지 데이터 + 예측 결과)를 "항공편 정보" DB에 저장
  ⑦ (back-end) 예측 결과 데이터를 front-end로 전송하기
  ⑧ (front-end) 예측 결과 데이터가 존재하면, 운항 관리 페이지 내 "예측하기" 버튼 하단에 결과 현시하기 

 5-3. 고객 관리
  5-3-1. 항공편 정보
  ① (front-end) 항공편명 입력
  ② (front-end) "조회하기" 버튼 클릭
  ③ (back-end) 항공편명 정보 서버로 전달
  ④ (back-end) "항공편 정보" DB에서 편명 조회하기 
  ⑤ (back-end) 4가지 정보(편명, 출발 공항, 도착 공항, 운항 예측) front-end로 전송하기
  ⑥ (back-end) 서버에서 전달된 4가지 정보를 표 형태로 현시하기
  ⑦ (back-end) 예측 결과 데이터를 front-end로 전송하기
  ⑧ (front-end) 예측 결과 데이터가 존재하면, 운항 관리 페이지 내 "예측하기" 버튼 하단에 결과 현시하기
  
  5-3-2. 문자 보내기 버튼
  ① (front-end) "안내문자 전송" 버튼 클릭
  ② (back-end) 항공편명 정보 서버로 전달 
  ③ (back-end) "항공편 정보" DB에서 편명 조회하기 
  ④ (back-end) 카톡 보내기(코드 구현)
  ⑤ (front-end) 성공 시, 고객 관리 페이지 내 "안내문자 전송" 버튼 내용을 "안내문자 전송 완료"로 변경하기

  5-3-3. 삭제 버튼
  ① (front-end) "Delete" 버튼 클릭
  ② (back-end) 항공편명 정보 서버로 전달 
  ③ (back-end) "항공편 정보" DB에서 편명 레코드(record) 삭제하기 
  ④ (front-end) 성공 시, 고객 관리 페이지 내 표 삭제하기