from src.Transrect_AMS.database import db


class Machine(db.Model):
    __tablename__ = 'machines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    purchase_date = db.Column(db.Date, nullable=False)
    lifespan = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=True)

    parts = db.relationship('Part', backref='machine',
                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Machine {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
            # include other fields if needed
        }


class Part(db.Model):
    __tablename__ = 'parts'

    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey(
        'machines.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    lifespan = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Part {self.name} of Machine {self.machine_id}>'
