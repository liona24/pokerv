pokerv
======

A simple multiplayer poker game built with [Flask](http://flask.pocoo.org/), [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) and [VueJS](https://vuejs.org/).


## Installation

Node and python 3 are required.

Running this will build the vue application:

```
$ git clone git@github.com:liona24/pokerv.git
$ cd pokerv/frontend
$ npm install
$ npm run build
```

For testing purposes the Flask dev server will suffice:

```
$ cd ..
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ cd backend
$ python server.py
```

## Usage

The interface should be straight-forward. Suggestions welcome.

## Notes

This software is somewhere in alpha land and thus may (and does) contain many bugs.

Also take a note that the requirements contain a link to another repo since it is not available on the python package index (because of its development status)

Suits are taken from [here](http://www.chaos-dwarfs.com/images/xander/malifaux-bioshock/malifaux-suits_01.png).
