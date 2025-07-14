import flask

import models
import forms


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://coe:CoEpasswd@localhost:5432/coedb"

models.init_app(app)


@app.route("/")
def index():
    db = models.db
    notes = db.session.execute(
        db.select(models.Note).order_by(models.Note.title)
    ).scalars()
    return flask.render_template(
        "index.html",
        notes=notes,
    )


@app.route("/notes/create", methods=["GET", "POST"])
def notes_create():
    form = forms.NoteForm()
    if not form.validate_on_submit():
        print("Form not valid:", form.errors)
        return flask.render_template("notes-create.html", form=form, edit_mode=False)

    if form.validate_on_submit():
        note = models.Note()
        note.title = form.title.data
        note.description = form.description.data
        note.tags = []

        db = models.db
        for tag_name in form.tags.data:
            tag = db.session.execute(
                db.select(models.Tag).where(models.Tag.name == tag_name)
            ).scalars().first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
            note.tags.append(tag)

        db.session.add(note)
        db.session.commit()
        return flask.redirect(flask.url_for("index"))

    return flask.render_template("notes-create.html", form=form, edit_mode=False)


@app.route("/notes/edit/<int:note_id>", methods=["GET", "POST"])
def notes_edit(note_id):
    db = models.db
    note = db.session.get(models.Note, note_id)
    if not note:
        return "Note not found", 404

    form = forms.NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.description = form.description.data
        note.tags.clear()
        for tag_name in form.tags.data:
            tag = db.session.execute(
                db.select(models.Tag).where(models.Tag.name == tag_name)
            ).scalars().first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
            note.tags.append(tag)
        db.session.commit()
        return flask.redirect(flask.url_for("index"))

    form.tags.data = [tag.name for tag in note.tags]
    return flask.render_template("notes-create.html", form=form, edit_mode=True)


@app.route("/notes/delete/<int:note_id>", methods=["POST"])
def notes_delete(note_id):
    db = models.db
    note = db.session.get(models.Note, note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return flask.redirect(flask.url_for("index"))


@app.route("/tags/<tag_name>")
def tags_view(tag_name):
    db = models.db
    tag = (
        db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
        .scalars()
        .first()
    )
    notes = db.session.execute(
        db.select(models.Note).where(models.Note.tags.any(id=tag.id))
    ).scalars()

    return flask.render_template(
        "tags-view.html",
        tag_name=tag_name,
        notes=notes,
    )


@app.route("/tags/edit/<int:tag_id>", methods=["GET", "POST"])
def tags_edit(tag_id):
    db = models.db
    tag = db.session.get(models.Tag, tag_id)
    if not tag:
        return "Tag not found", 404

    form = forms.TagForm(obj=tag)
    if form.validate_on_submit():
        form.populate_obj(tag)
        db.session.commit()
        return flask.redirect(flask.url_for("index"))

    return flask.render_template("notes-create.html", form=form, edit_mode=True)


@app.route("/tags/delete/<int:tag_id>", methods=["POST"])
def tags_delete(tag_id):
    db = models.db
    tag = db.session.get(models.Tag, tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
    return flask.redirect(flask.url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
