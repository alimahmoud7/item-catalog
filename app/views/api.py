from app.models import session, Field, MOOC, User
from flask import jsonify, Blueprint

api = Blueprint('api', __name__)


# JSON Endpoints
@api.route('/api/categories')
def categories_json():
    """Return all fields and moocs"""
    fields = session.query(Field).all()
    fields_list = []
    for field in fields:
        moocs = session.query(MOOC).filter_by(field_id=field.id).all()
        moocs_list = [mooc.serialize for mooc in moocs]
        field_moocs = field.serialize
        field_moocs['items'] = moocs_list
        fields_list.append(field_moocs)

    return jsonify(Categories=fields_list)


@api.route('/api/fields')
def fields_json():
    """Return all fields"""
    fields = session.query(Field).all()
    return jsonify(Fields=[field.serialize for field in fields])


@api.route('/api/moocs')
def moocs_json():
    """Return all moocs"""
    moocs = session.query(MOOC).all()
    return jsonify(MOOCs=[mooc.serialize for mooc in moocs])


@api.route('/api/moocs/<int:mooc_id>')
def mooc_json(mooc_id):
    """Return a specific mooc"""
    mooc = session.query(MOOC).filter_by(id=mooc_id).first()
    if mooc is None:
        return jsonify({'error': 'This MOOC does not exist!'})
    return jsonify(MOOC=[mooc.serialize])
