from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    contraseña = db.Column(db.String(200), nullable=False)
    contact= db.relationship("Contact")
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre_usuario": self.nombre_usuario,
            "email": self.email,
            "contraseña": self.contraseña
            }

class Contact(db.Model):
    __tablename__="contact"
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.Integer)
    email = db.Column(db.String(200), nullable=False, unique=True)
    direccion = db.Column(db.String(200))
    notas = db.Column(db.String(200))
    categoria = db.Column(db.String(200))
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre_usuario": self.nombre_usuario,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "notas": self.notas,
            "categoria": self.categoria    
    }