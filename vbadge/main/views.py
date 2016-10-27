from uuid import uuid4

from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe, require_POST

from .imgutil import create_badge, get_profile


@require_safe
def index(request):
    return render(request, 'main/index.html')


@require_POST
def submit(request):
    fid = request.POST['fid']

    create_badge(get_profile(fid), settings.VBADGE['BADGE_DIR'])

    token = uuid4()
    # TODO: save fid + token + last updated time to db
    return redirect(manage, fid=fid, token=token)


@require_safe
def manage(request, fid, token):

    # TODO: validate token

    return render(request, 'main/manage.html', {
        'fid': fid,
        'token': token,
        'badge_url': '/static/badges/%s.png' % fid,
    })
