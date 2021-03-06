server:
	python manage.py server

install:
	virtualenv venv
	. venv/bin/activate
	pip install -r requirements.txt

activate:
# Using `.` since source is a bash builtin not supported by make
	. venv/bin/activate
venv: activate
work: activate

clean:
	find pulpopaul . -name "*~" -delete -o -name "*pyc" -delete

deploy:
	git push openshift master

lint:
	@-pylint pulpopaul/

.PHONY: server install activate venv work clean lint
