from flask import request, jsonify
from models import db, Character


def register_characters_routes(app):

    @app.route("/characters", methods=["GET", "POST"])
    def characters_collection():
        if request.method == "GET":
            characters = db.session.scalars(db.select(Character)).all()
            result = [u.serialize() for u in characters]
            return jsonify(result)
        elif request.method == "POST":
            data = request.json
            charcter = Character(**data)
            db.session.add(charcter)
            db.session.commit()
            result = charcter.serialize()
            return jsonify(result), 201

    @app.route("/characters/<int:character_id>", methods=["GET", "DELETE"])
    def charcter_item(character_id):
        charcter = db.session.get(Character, character_id)
        if not charcter:
            return {"error": "Character not found"}, 404
        if request.method == "GET":
            result = charcter.serialize()
            return jsonify(result)
        elif request.method == "DELETE":
            db.session.delete(charcter)
            db.session.commit()
            return "", 204