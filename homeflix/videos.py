from flask import (
        Blueprint,
        flash,
        g,
        redirect,
        render_template,
        request,
        url_for,
)

from werkzeug.exceptions import abort

from homeflix.auth import login_required
from homeflix.db import get_db


bp = Blueprint('video', __name__)


@bp.route("/")
def index():
    db = get_db()
    videos = db.execute(
            'SELECT v.id, v.title, v.body, v.created'
            ' FROM video v ORDER BY created DESC'
    ).fetchall()
    return render_template('video/index.html', videos)
