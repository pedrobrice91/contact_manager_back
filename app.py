from flask import Flask, request, jsonify
from models import db, User, Contact
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///proyect.db"
db.init_app(app)
Migrate(app, db)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "<h1>Hola soy el backend<h1/>"

@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User()
    if data:
        email = data["email"]
        if email:
            user.email = email
        else:
            return jsonify({"msg": "Email no puede estar vacío"}), 400
        user.nombre_usuario = data["nombre_usuario"]
        user.contraseña = data["contraseña"]
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "Usuario creado", "data": user.serialize()}), 200
    else:
        return jsonify({"msg": "No hay cuerpo en la consulta"}), 400

@app.route("/contact", methods=["POST"])
def create_contact():
    data = request.get_json()
    contact = Contact()
    if data:
        email = data["email"]
        if email:
            contact.email = email
        else:
            return jsonify({"msg": "Email no puede estar vacío"}), 400
        contact.nombre_usuario = data["nombre_usuario"]
        contact.telefono = data["telefono"]
        contact.direccion = data["direccion"]
        contact.notas = data["notas"]
        contact.categoria = data["categoria"]
        db.session.add(contact)
        db.session.commit()
        return jsonify({"msg": "Contacto creado", "data": contact.serialize()}), 200
    else:
        return jsonify({"msg": "No hay cuerpo en la consulta"}), 400

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    contacts = list(map(lambda contact: contact.serialize(), contacts))
    return jsonify(contacts)

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users)

@app.route("/contact/search", methods=["GET"])
def search_contact():
    nombre = request.args.get("nombre")
    telefono = request.args.get("telefono")
    query = Contact.query

    if nombre:
        query = query.filter(Contact.nombre_usuario.ilike(f"%{nombre}%"))
    if telefono:
        query = query.filter(Contact.telefono.ilike(f"%{telefono}%"))

    results = query.all()
    if results:
        return jsonify([contact.serialize() for contact in results]), 200
    else:
        return jsonify({"msg": "No se encontraron contactos"}), 404

@app.route("/contact/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({"msg": "Contacto no encontrado"}), 404

    data = request.get_json()
    if data.get("nombre_usuario"):
        contact.nombre_usuario = data["nombre_usuario"]
    if data.get("telefono"):
        contact.telefono = data["telefono"]
    if data.get("direccion"):
        contact.direccion = data["direccion"]
    if data.get("notas"):
        contact.notas = data["notas"]
    if data.get("categoria"):
        contact.categoria = data["categoria"]

    db.session.commit()
    return jsonify({"msg": "Contacto actualizado", "data": contact.serialize()}), 200

@app.route("/contact/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({"msg": "Contacto no encontrado"}), 404

    db.session.delete(contact)
    db.session.commit()
    return jsonify({"msg": f"Contacto {contact_id} eliminado"}), 200

if __name__ == "__main__":
    app.run(host="localhost", port=5050, debug=True)
