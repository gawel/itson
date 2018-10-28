# -*- coding: utf-8 -*-
import os
from datetime import datetime
from tinydb import TinyDB, Query
from bottle import (
    route, run, template, request, default_app, redirect,
    auth_basic, static_file,
)

db = TinyDB(os.path.expanduser('~/.itson.json'))

Session = Query()
FMT = '%Y-%m-%dT%H:%M'
SIZES = {k: '%sm' % k for k in [i / 10 for i in list(range(5, 45, 5))]}


def check_auth(user, pw):
    if pw == 'itson':
        return True
    return False


def dformat(d):
    if d == 0:
        d = 0
    elif d > 60:
        d = '%sh%sm' % (int(d / 60), d % 60)
    else:
        d = '%sm' % d
    return d


@route("/static/images/<filepath:re:.*\.jpg>")
def images(filepath):
    return static_file(filepath, root="images")


@route('/')
def index():
    itson = False
    title = "It's OFF..."
    latests = db.search(Session.ended == 0)
    if latests:
        title = "It's ON!"
        itson = True
    records = []
    t = 0
    for r in db.all():
        started = datetime.strptime(r['started'], FMT)
        ended = 0
        if r['ended'] != 0:
            ended = datetime.strptime(r['ended'], FMT).strftime('%H:%M')
        duration = r['duration']
        t += duration
        duration = dformat(duration)
        records.insert(0, dict(
            date=started.strftime('%Y-%m-%d'),
            started=started.strftime('%H:%M'),
            ended=ended,
            duration=duration,
            size=SIZES[float(r.get('size', '0.5'))],
            comment=r.get('comment', ''),
        ))
    return template('index', total=dformat(t), itson=itson, title=title,
                    records=records, request=request)


@route('/session')
@route('/session', method='POST')
@auth_basic(check_auth)
def session():
    now = datetime.now()
    title = 'Ready to go?'
    itson = False
    latests = db.search(Session.ended == 0)
    if latests:
        title = 'Back ?'
        itson = True
    if request.forms:
        if itson:
            latest = latests[0]
            started = datetime.strptime(latest['started'], FMT)
            duration = now - started
            duration = int(duration.seconds / 60)
            db.update(
                {
                    'ended': now.strftime(FMT),
                    'duration': duration,
                    'size': request.forms['size'],
                    'comment': request.forms['comment'] or '',
                },
                Session.ended == 0)
        else:
            db.insert(dict(
                started=now.strftime(FMT),
                ended=0,
                duration=0,
            ))
        return redirect('/')
    context = dict(
        title=title, itson=itson,
        sizes=sorted(SIZES.items()),
        request=request,
    )
    return template('session', **context)


def main():
    run(host='0.0.0.0', port=4444)


application = default_app()
