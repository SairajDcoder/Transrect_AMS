from src.Transrect_AMS.database import db


class MachineInfo(db.Model):
    __tablename__ = 'machine_info'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    lifespan = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=True)


class MachinePartsInfo(db.Model):
    __tablename__ = 'machine_parts_info'

    id = db.Column(db.Integer, primary_key=True)
    machine_info_id = db.Column(db.Integer, db.ForeignKey(
        'machine_info.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    lifespan = db.Column(db.Integer, nullable=False)
