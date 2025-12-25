from src.Transrect_AMS.database import db


class Inbox(db.Model):
    __tablename__ = 'inbox'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_name = db.Column(db.String(100), nullable=False)
    receiver_name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=True)
    time = db.Column(db.DateTime, server_default=db.func.now()
                     )
    unread = db.Column(db.Boolean, default=True)
    location = db.Column(db.String(100), nullable=False)
    payment_confirmation = db.Column(db.Boolean, default=False)

    machine_name = db.Column(
        db.String(100), nullable=True)
    estimated_amount = db.Column(db.Numeric(
        12, 2), nullable=True)

    def __repr__(self):
        return f"Message from {self.sender_name} at {self.time}, Payment Confirmation: {self.payment_confirmation}, Machine Name: {self.machine_name}, Estimated Amount: {self.estimated_amount}"
