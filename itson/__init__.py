# -*- coding: utf-8 -*-
import os
from datetime import datetime
from tinydb import (TinyDB, Query)
from operator import itemgetter
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


class Record(dict):

    def __getattr__(self, attr):
        return self[attr]


def url(path=None):
    root_url = '/'.join(request.url.split('/')[:3])
    if path:
        root_url += path
    return root_url


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
        size = r.get('size') or 0
        sess.insert(0, Record(
            id=r.doc_id,
            sort_key=started,
            date=started.strftime('%Y-%m-%d'),
            started=started.strftime('%H:%M'),
            ended=ended,
            duration=duration,
            spot=r.get('spot') or 'Secret',
            size=size,
            comment=r.get('comment', ''),
            report_url=r.get('report_url', ''),
            record=r,
        ))
    sess = sorted(sess, key=itemgetter('sort_key'), reverse=True)
    return sess


@route(r"/statics/<filepath:re:.*\.(jpg|css|ico)>")
def statics(filepath):
    return static_file(filepath, root="statics")


@route('/')
def index():
    date = datetime.now().strftime(FMT)
    return redirect('/sessions/' + date.split('T')[0].replace('-', '/'))


@route('/sessions/<year:int>/<month:int>/<day:int>')
@route('/sessions/<year:int>/<month:int>/<day:int>/')
@route('/sessions/<year:int>/<month:int>/<day:int>/<share_id:int>')
@route('/sessions/<year:int>/<month:int>/<day:int>/<share_id:int>/')
def session(year=None, month=None, day=None, share_id=None):
    now = datetime.now().strftime(FMT).split('T')[0]
    today = True
    date = '%04d-%02d-%02d' % (year, month, day)
    if date != now:
        today = False
    context = dict(
        itson=False,
        title="It's OFF..." if today else "It was OFF...",
    )
    records = db.search(Session.date == date)
    sessions = get_sessions(records)
    if sessions:
        context.update(
            title="It's ON!" if today else "It was ON!",
            itson=True,
            sessions=sessions,
        )
    return template('index', url=url(), request=request, **context)


@route('/sessions')
@route('/sessions/')
@route('/admin/sessions')
@route('/admin/sessions/')
def history():
    itson = False
    title = "It's OFF..."
    for latest in latests():
        title = "It's ON!"
        itson = True
    sessions = get_sessions(db.all())
    amount = len(sessions)
    total = Record(
        date=amount,
        spot=len(set(s['spot'] for s in sessions)),
        duration=dformat(sum(s['record']['duration'] for s in sessions)),
        size='%.2f' % (sum(
            float(s['record'].get('size') or 0) for s in sessions
        ) / amount))
    return template('history', itson=itson, title=title,
                    url=url(), request=request,
                    admin='/admin/' in request.url,
                    sessions=sessions, total=total)


@route('/admin/sessions/<doc_id:int>')
@route('/admin/sessions/<doc_id:int>/')
@route('/admin/sessions/<doc_id:int>', method='POST')
@auth_basic(check_auth)
def edit_session(doc_id=None):
    record = db.get(doc_id=doc_id)
    record = Record(record, id=record.doc_id)
    if request.forms:
        data = {k: v for k, v in request.forms.items() if v}
        ended = data.get('ended') or 0
        data['ended'] = ended
        try:
            ended = datetime.strptime(data['ended'], FMT)
        except (ValueError, TypeError):
            pass
        else:
            started = datetime.strptime(data['started'], FMT)
            duration = ended - started
            duration = int(duration.seconds / 60)
            data['duration'] = duration
        db.update(data, doc_ids=[doc_id])
        return redirect(request.url)
    return template('edit', itson=True, title='Edit',
                    url=url(), request=request,
                    admin='/admin/' in request.url,
                    record=record,
                    )


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
    record = {}
    if latest:
        started = datetime.strptime(latest['started'], FMT)
        duration = now - started
        duration = int(duration.seconds / 60)
        records = db.search(
            (Session.started == latest['started']) & (Session.ended == 0))
        for record in records:
            record = record
        record.update({
                'ended': now.strftime(FMT),
                'duration': duration,
                'size': kwargs['size'],
                'comment': kwargs.get('comment') or '',
        })
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
        db.insert(record)
    data.update(record)
    return data


@route('/admin/sessions/new')
@route('/admin/sessions/new', method='POST')
@auth_basic(check_auth)
def new_session():
    data = {
        'itson': False,
        'latest': None,
        'title': 'Ready to go?',
    }
    if request.forms:
        data.update(_session(**request.forms))
        return redirect(
            '/sessions/' + data['date'].split('T')[0].replace('-', '/'))
    else:
        for latest in latests():
            if not latest['ended']:
                data.update(title='Back ?', itson=True)
                break
            else:
                latest = data['latest'] = None

    spots = []
    for r in reversed(db.all()):
        spot = r.get('spot')
        if spot not in (None, 'Secret') and spot not in spots:
            spots.append(spot)
    spots.insert(1, 'Secret')

    data.update(
        sizes=sorted(SIZES.items()),
        spots=spots,
        url=url(),
        request=request,
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
