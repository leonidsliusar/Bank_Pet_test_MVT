test:  # run all test with coverage report
	coverage run -m pytest
	coverage report

run_app:  # make migration and run server
	python manage.py migrate
	python manage.py runserver

docker_start:  # run server and db in containers
	docker compose up -d

docker_stop:  # stop server and db and delete containers
	docker compose down

docker_del_v:  # stop servers, delete volumes
	docker compose down -v

docker_del_all:  # stop servers, delete images and volumes
	docker compose down --rmi "all" -v

get_env:  # create env file
	touch .env
	echo "DB_NAME =\n\
	DB_USER =\n\
	DB_PASSWORD =\n\
	DB_HOST = localhost\n\
	DB_PORT = 5432\n\
	SECRET_KEY =\n\
	DJANGO_ALLOWED_HOSTS=(localhost 127.0.0.1, )" > .env