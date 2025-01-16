from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # Ensuring uniqueness
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Product({self.id}, {self.name}, {self.description})"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}
