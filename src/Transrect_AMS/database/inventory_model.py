from src.Transrect_AMS.database import db


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Inventory {self.item_name} - Qty: {self.quantity} - Amount: {self.amount}>'
