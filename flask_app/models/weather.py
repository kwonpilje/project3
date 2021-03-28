from flask_app import db

class Weather(db.Model):

    __tablename__ = "Weather"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(64), nullable=False)
    rvr = db.Column(db.Integer, nullable=False)
    wind = db.Column(db.Integer, nullable=False)
    cloud = db.Column(db.Integer, nullable=False)

