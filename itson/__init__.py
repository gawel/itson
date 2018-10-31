# -*- coding: utf-8 -*-
import os
from datetime import datetime
from tinydb import (TinyDB, Query)
from bottle import (
    route, default_app, template, request,
    run, debug,
    redirect,
    auth_basic, static_file,
)

db = TinyDB(os.path.expanduser('~/.itson.json'))

Session = Query()
FMT = '%Y-%m-%dT%H:%M'
SIZES = {k: '%sm' % k for k in [i / 10 for i in list(range(5, 45, 5))]}


def check_auth(user, pw):
    auth = ('admimin', os.environ.get('ADMIN_PASSWORD', 'passwd'))
    if (user, pw) == auth:
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


@route("/statics/<filepath:re:.*\.(jpg|css)>")
def statics(filepath):
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


def _session(**kwargs):
    now = datetime.now()
    itson = False
    latest = None
    for latest in latests():
        if not latest['ended']:
            itson = True
            break
        else:
            latest = None
    data = {
        'itson': itson,
        'latest': latest,
    }
    if latest:
        started = datetime.strptime(latest['started'], FMT)
        duration = now - started
        duration = int(duration.seconds / 60)
        records = db.search(
            (Session.started == latest['started']) & (Session.ended == 0))
        record = {}
        for record in records:
            record = record
        record.update({
                'ended': now.strftime(FMT),
                'duration': duration,
                'size': kwargs['size'],
                'comment': kwargs.get('comment') or '',
        })
        data.update(record)
        db.update(
            record,
            (Session.started == latest['started']) & (Session.ended == 0))
    else:
        spot = kwargs.get('new_spot') or None
        if spot is None:
            spot = kwargs.get('spot') or 'Secret'
        record = dict(
            date=now.strftime('%Y-%m-%d'),
            started=now.strftime(FMT),
            ended=0,
            duration=0,
            spot=spot,
        )
        data.update(record)
        db.insert(record)
    return data


@route('/session')
@route('/session', method='POST')
@auth_basic(check_auth)
def session():
    data = {
        'itson': False,
        'latest': None,
        'title': 'Ready to go?',
    }
    if request.forms:
        data.update(_session(**request.forms))
        redirect('/')

    else:
        for latest in latests():
            if not latest['ended']:
                data.update(title='Back ?', itson=True)
                break
            else:
                latest = data['latest'] = None

    spots = []
    for r in db.all():
        spot = r.get('spot')
        if spot not in (None, 'Secret') and spot not in spots:
            spots.insert(0, spot)
    spots.insert(1, 'Secret')

    data.update(
        sizes=sorted(SIZES.items()),
        spots=spots,
    )
    return template('session', **data)


@route('/api/sessions', method='POST')
@auth_basic(check_auth)
def api_session():
    data = _session(**request.json)
    latest = data.pop('latest', None)
    if latest:
        print(latest)
    return {k: v for k, v in data.items() if v}


@route('/<path:path>')
def error_404(path):
    return redirect('/')


def main():
    if 'ADMIN_PASSWORD' not in os.environ:
        debug(mode=True)
    run(host='0.0.0.0', port=4444, reloader=True)


application = default_app()
