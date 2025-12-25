from src.Transrect_AMS.database import db


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    machine_name = db.Column(db.String(150), nullable=False)
    estimated_amount = db.Column(db.Float, nullable=False)
    account = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Transaction {self.transaction_id} - {self.account}, Machine: {self.machine_name}>'
