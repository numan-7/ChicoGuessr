# ChicoGuessr - GeoGuessr Clone

GeoGuessr clone made in collaboration with <a href="https://github.com/lukehaz" target="_blank">lukehaz </a>based in Chico, California:
<br/>
<a href="https://www.chicoguessr.xyz" target="_blank">Play Here</a>
<br/>
<a href="https://www.youtube.com/watch?v=5f4Sn2td6gI" target="_blank">Preview Here</a>
## Setup

The first thing to do is to clone the repository:

```sh
$ git clone git@github.com:ChicoState/ChicoGuessr.git
$ cd ChicoGuessr
```
Get your [Google Maps JS API Key](https://console.cloud.google.com/). <br/>
Then create a .env in the current directory & add your API key inside it like this:
```sh
1 API_KEY="<KEY>"
```
Get your [Django Secret Key](https://djecrety.ir/). <br/>
Then add it into the .env:
```sh
1 API_KEY="<KEY>"
2 SECRET_KEY = "<KEY>"
3 DEBUG = false
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
