from flask_app import db

class Regression_train(db.Model):

    __tablename__ = "Regression_train"

    id = db.Column(db.Integer, primary_key=True)
    rvr_reg = db.Column(db.Integer, nullable=False)
    wind_reg = db.Column(db.Integer, nullable=False)
    cloud_reg = db.Column(db.Integer, nullable=False)
    target = db.Column(db.Integer, nullable=False)