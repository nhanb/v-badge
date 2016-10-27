import uuid
from flask import redirect, request, render_template, url_for
from vbadge import app, celery_app
from .imgutil import create_badge, get_profile


@app.route('/')
def index():
    return render_template('index.html')


@celery_app.task
def submit_fid(fid, token):
    img_path = create_badge(get_profile(fid))
    return (img_path, token)


@app.route('/submit', methods=['POST'])
def submit():
    fid = request.form['fid'].strip()
    if not fid:
        return redirect('/')
    token = uuid.uuid4()
    submit_fid.delay(fid, token)
    return redirect(url_for('manage', token=token))


@app.route('/manage')
def manage():
    return render_template('manage.html', token=request.args['token'])
