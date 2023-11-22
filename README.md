# ChicoGuessr - GeoGuessr Clone

GeoGuessr clone based in Chico, California.


## Setup

The first thing to do is to clone the repository:

```sh
$ git clone git@github.com:ChicoState/ChicoGuessr.git
$ cd ChicoGuessr
```
Get your [Google Maps JS API Key](https://console.cloud.google.com/).
Then create a .env in the current directory & add your API key inside it like this:
```sh
$ API_KEY="<KEY>"
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ pip install virtualenv (if not installed already)
$ virtualenv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

To leave virtual env:
```sh
(env)$ deactive
```
