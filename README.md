# testtask

create virtual environment using commanda and activate env:

```sh
$ python3 -m venv /path/to/new/virtual/environment
```
or

```sh
$ virtualenv -p python3 .venv
```

activate env:
```sh
$ source env/bin/activate
```

Then install the dependencies:

```sh
(.venv)$ pip install -r requirements.txt
```


Once `pip` has finished downloading the dependencies:

```sh
(.venv)$ cd test-task
(.venv)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

If you want to create superuser:

```sh
(.venv)$ python manage.py createsuperuser
```
Open `http://127.0.0.1:8000/admin/`

Enter superuser credentials.You can access admin site of django.
