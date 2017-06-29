# pulpopaul
Quinela para futbol colaborativo

How to install
==============

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

manage.py
=========

To start a server
`python manage.py server`

To create the db
```
python manage.py shell
db.create_all()
```