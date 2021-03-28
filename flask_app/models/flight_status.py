from flask_app import db

class Flight_status(db.Model):

    __tablename__ = "Flight_status"

    id = db.Column(db.Integer, primary_key=True)
    flight = db.Column(db.String(64), unique=True, nullable=False)
    airport_ori = db.Column(db.String(64), nullable=False)
    airport_des = db.Column(db.String(64), nullable=False)
    eta = db.Column(db.Integer, nullable=False)
    anal_result = db.Column(db.Integer, nullable=False)


