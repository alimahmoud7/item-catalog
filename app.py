from database_setup import Base, Field, MOOC
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from flask import Flask, render_template, request, url_for, redirect, jsonify

engine = create_engine('sqlite:///top_mooc.db')

# Make a connection between class definitions and the corresponding tables within database
Base.metadata.bind = engine

# Establish a link of connection between code execution and the engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


# JSON Endpoints
@app.route('/api/categories')
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


@app.route('/api/fields')
def fields_json():
    """Return all fields"""
    fields = session.query(Field).all()
    return jsonify(Fields=[field.serialize for field in fields])


@app.route('/api/moocs')
def moocs_json():
    """Return all moocs"""
    moocs = session.query(MOOC).all()
    return jsonify(MOOCs=[mooc.serialize for mooc in moocs])


@app.route('/api/moocs/<int:mooc_id>')
def mooc_json(mooc_id):
    """Return a specific mooc"""
    mooc = session.query(MOOC).filter_by(id=mooc_id).first()
    if mooc is None:
        return jsonify({'error': 'This MOOC does not exist!'})
    return jsonify(MOOC=[mooc.serialize])


# Normal Routing
@app.route('/')
@app.route('/fields/')
def index():
    """Show all CS fields with latest MOOCs"""
    fields = session.query(Field).order_by(asc(Field.name)).all()
    moocs = session.query(MOOC).order_by(desc(MOOC.id)).all()
    return render_template('index.html', fields=fields, moocs=moocs)


@app.route('/fields/new', methods=['GET', 'POST'])
def new_field():
    """Add a new CS field"""
    if request.method == 'POST':
        if request.form.get('name'):
            field = Field(name=request.form.get('name'))
            session.add(field)
            session.commit()
        return redirect(url_for('index'))

    return render_template('new_field.html')


@app.route('/fields/<int:field_id>/edit', methods=['GET', 'POST'])
def edit_field(field_id):
    """Edit a CS field"""
    field = session.query(Field).filter_by(id=field_id).first()

    # Check if field doesn't exist in database
    if field is None:
        return jsonify({'error': 'This Field does not exist!'})

    if request.method == 'POST':
        if request.form.get('name'):
            field.name = request.form.get('name')
            session.add(field)
            session.commit()
        return redirect(url_for('index'))

    return render_template('edit_field.html', field=field)


@app.route('/fields/<int:field_id>/delete', methods=['GET', 'POST'])
def delete_field(field_id):
    """Delete a CS field"""
    field = session.query(Field).filter_by(id=field_id).first()

    # Check if field doesn't exist in database
    if field is None:
        return jsonify({'error': 'This Field does not exist!'})

    if request.method == 'POST':
        session.delete(field)
        session.commit()

        # Delete Field MOOCs too
        moocs = session.query(MOOC).filter_by(field_id=field.id).all()
        for mooc in moocs:
            session.delete(mooc)
            session.commit()

        return redirect(url_for('index'))

    return render_template('delete_field.html', field=field)


@app.route('/fields/<int:field_id>/')
@app.route('/fields/<int:field_id>/moocs/')
def show_moocs(field_id):
    """Show all MOOCs with a specific field"""
    field = session.query(Field).filter_by(id=field_id).first()

    # Check if field doesn't exist in database
    if field is None:
        return jsonify({'error': 'This Field does not exist!'})

    moocs = session.query(MOOC).filter_by(field_id=field_id).order_by(asc(MOOC.title)).all()
    return render_template('moocs.html', field=field, moocs=moocs)


@app.route('/fields/<int:field_id>/moocs/new', methods=['GET', 'POST'])
def new_mooc(field_id):
    """Add new MOOC"""
    field = session.query(Field).filter_by(id=field_id).first()

    # Check if field doesn't exist in database
    if field is None:
        return jsonify({'error': 'This Field does not exist!'})

    if request.method == 'POST':
        if request.form.get('title') and request.form.get('provider') and request.form.get('url'):
            mooc = MOOC(title=request.form.get('title'), provider=request.form.get('provider'),
                        creator=request.form.get('creator'), level=request.form.get('level'),
                        url=request.form.get('url'), description=request.form.get('description'),
                        image=request.form.get('image'), field=field)
            session.add(mooc)
            session.commit()
        return redirect(url_for('show_moocs', field_id=field_id))

    return render_template('new_mooc.html', field=field)


@app.route('/fields/<int:field_id>/moocs/<int:mooc_id>/edit', methods=['GET', 'POST'])
def edit_mooc(field_id, mooc_id):
    """Edit a MOOC"""
    field = session.query(Field).filter_by(id=field_id).first()
    mooc = session.query(MOOC).filter_by(id=mooc_id, field_id=field_id).first()

    # Check if field doesn't exist in database
    if mooc is None or field is None:
        return jsonify({'error': 'This MOOC does not exist!'})

    if request.method == 'POST':
        if request.form.get('title'):
            mooc.title = request.form.get('title')
        if request.form.get('provider'):
            mooc.provider = request.form.get('provider')
        if request.form.get('creator'):
            mooc.creator = request.form.get('creator')
        if request.form.get('level'):
            mooc.level = request.form.get('level')
        if request.form.get('url'):
            mooc.url = request.form.get('url')
        if request.form.get('description'):
            mooc.description = request.form.get('description')
        if request.form.get('image'):
            mooc.image = request.form.get('image')
        return redirect(url_for('show_moocs', field_id=field_id))

    return render_template('edit_mooc.html', mooc=mooc, field=field)


@app.route('/fields/<int:field_id>/moocs/<int:mooc_id>/delete', methods=['GET', 'POST'])
def delete_mooc(field_id, mooc_id):
    """Delete a MOOC"""
    field = session.query(Field).filter_by(id=field_id).first()
    mooc = session.query(MOOC).filter_by(id=mooc_id, field_id=field_id).first()

    # Check if field doesn't exist in database
    if mooc is None or field is None:
        return jsonify({'error': 'This MOOC does not exist!'})

    if request.method == 'POST':
        session.delete(mooc)
        session.commit()
        return redirect(url_for('show_moocs', field_id=field_id))

    return render_template('delete_mooc.html', mooc=mooc, field=field)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
