from tinydb import TinyDB
import webtest
import pytest
import itson


@pytest.fixture
def db(tmp_path):
    db = TinyDB(str(tmp_path / '.itson.json'))
    itson.db = db
    yield db


@pytest.fixture
def app(db):
    itson.debug(mode=True)
    return webtest.TestApp(itson.application)


def test_app(app):
    resp = app.get('/')
    resp.mustcontain("No surf today...")

    resp = app.get('/session', status='*')
    assert resp.status_code == 401

    app.authorization = ('Basic', ('admimin', 'passwd'))
    resp = app.get('/session')

    form = resp.form
    form['new_spot'] = 'My Spot'
    resp = form.submit().follow()
    resp.mustcontain("I'm surfing")

    resp = app.get('/session')
    form = resp.form
    form['size'] = '2.0'
    resp = form.submit().follow()
    resp.mustcontain("I surfed")

    resp = app.get('/history')
    resp.mustcontain('My Spot')


def test_api(app):
    data = dict(spot='Other spot')
    resp = app.post_json('/api/sessions', status='*')
    assert resp.status_code == 401

    app.authorization = ('Basic', ('admimin', 'passwd'))

    resp = app.post_json('/api/sessions', data)
    data = resp.json
    print('start', data)
    assert 'spot' in data
    assert 'date' in data
    assert 'ended' not in data

    data = dict(size=2.0)
    resp = app.post_json('/api/sessions', data)
    data = resp.json
    print('end', data)
    assert 'spot' in data
    assert 'date' in data
    assert 'ended' in data
