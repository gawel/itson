itson
================================================

Small app to track time spent in the water, surfing.

Clone the repo::

$ git clone git@github.com:gawel/itson.git
$ cd itson

Create a venv and install the soft::

$ make

Start the app for testing::

$ make serve

Go to http://localhost:4444/

Default login/password is: admimin / passwd

Use whatever wsgi server for production. `itson.application` is a wsgi app::

$ ADMIN_PASSWORD=yourpassword ./venv/bin/chaussette itson.application --port 8080

