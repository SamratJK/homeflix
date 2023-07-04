from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for
)

import os
from uuid import uuid4

from homeflix.auth import login_required
from homeflix.db import get_db


bp = Blueprint("video", __name__)


@bp.route("/")
def index():
    db = get_db()
    videos = db.execute(
        "SELECT v.id, v.title, v.body, v.created"
        " FROM video v ORDER BY created DESC"
    ).fetchall()
    videos = videos if videos else []
    return render_template("video/index.html", videos=videos)


@bp.route("/add", methods=("GET", "POST"))
@login_required
def add():
    if request.method == "POST":
        title = request.form["title"]
        file = request.files["file"]
        error = None

        if not title or not file:
            error = "missing required fild"

        if error is not None:
            flash(error)

        else:
            body = str(uuid4())

            video_dir = os.path.join(current_app.static_folder, "videos")
            file_path = os.path.join(video_dir, f"{body}.mp4")
            file.save(file_path)

            db = get_db()
            db.execute(
                "INSERT INTO video (title, body) VALUES(?,?)", (title, body)
            )
            db.commit()

    return render_template("video/add.html")


def get_video(id):
    return get_db().execute("SELECT * FROM video where id = ?", (id,)).fetchone()


@bp.route("/<id>/delete", methods=("post",))
@login_required
def delete(id):
    db = get_db()

    db.execute('DELETE from video WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('video.index'))



@bp.route("/page/<id>", methods=("get",))
def page(id):
    video = get_video(id)
    return render_template(
        "video/page.html", videoname=video["body"], title=video["title"]
    )
