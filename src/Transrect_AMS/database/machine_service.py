from src.Transrect_AMS.database import db


class MachineService(db.Model):
    __tablename__ = 'machine_services'

    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey(
        'machines.id'), nullable=False)
    last_service = db.Column(db.Date, nullable=False)
    next_service = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Machine {self.machine_id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "machine_id": self.machine_id,
            "last_service": self.last_service.strftime('%Y-%m-%d') if self.last_service else None,
            "next_service": self.next_service.strftime('%Y-%m-%d') if self.next_service else None
        }
