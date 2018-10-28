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
        d = '%sh%smn' % (int(d / 60), d % 60)
    else:
        d = '%smn' % d
    return d


def latests():
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    return db.search(Session.date == date)


def get_sessions(records):
    sess = []
    now = datetime.now()
    for r in records:
        started = datetime.strptime(r['started'], FMT)
        ended = 0
        if r['ended'] != 0:
            ended = datetime.strptime(r['ended'], FMT).strftime('%H:%M')
        duration = r['duration']
        if not duration:
            duration = now - started
            duration = int(duration.seconds / 60)
        duration = dformat(duration)
        size = r.get('size') or ''
        if size:
            size = SIZES[float(size)]
        sess.insert(0, dict(
            date=started.strftime('%Y-%m-%d'),
            started=started.strftime('%H:%M'),
            ended=ended,
            duration=duration,
            spot=r.get('spot') or 'Secret',
            size=size,
            comment=r.get('comment', ''),
        ))
    return sess


@route("/statics/<filepath:re:.*\.jpg>")
@route("/statics/<filepath:re:.*\.css>")
def images(filepath):
    return static_file(filepath, root="statics")


@route('/')
def index():
    context = dict(
        itson=False,
        title="It's OFF...",
    )
    sessions = get_sessions(latests())
    if sessions:
        context.update(
            title="It's ON!",
            itson=True,
            sessions=sessions,
        )
    print(context)
    return template('index', **context)


@route('/history')
def history():
    itson = False
    title = "It's OFF..."
    for latest in latests():
        title = "It's ON!"
        itson = True
    return template('history', itson=itson, title=title,
                    sessions=get_sessions(db.all()))


@route('/session')
@route('/session', method='POST')
@auth_basic(check_auth)
def session():
    now = datetime.now()
    title = 'Ready to go?'
    itson = False
    latest = None
    for latest in latests():
        if not latest['ended']:
            title = 'Back ?'
            itson = True
            break
        else:
            latest = None

    if request.forms:
        if latest:
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
                (Session.started == latest['started']) & (Session.ended == 0))
            return redirect('/')
        else:
            spot = request.forms.get('new_spot') or None
            if spot is None:
                spot = request.forms.get('spot') or 'Secret'
            db.insert(dict(
                date=now.strftime('%Y-%m-%d'),
                started=now.strftime(FMT),
                ended=0,
                duration=0,
                spot=spot,
            ))
            return redirect('/session')

    spots = []
    for r in db.all():
        spot = r.get('spot')
        if spot not in (None, 'Secret') and spot not in spots:
            spots.insert(0, spot)
    spots.insert(1, 'Secret')

    context = dict(
        title=title, itson=itson,
        sizes=sorted(SIZES.items()),
        spots=spots,
    )
    return template('session', **context)


def main():
    run(host='0.0.0.0', port=4444, reloader=True)


application = default_app()
