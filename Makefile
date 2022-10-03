test:
	poetry run python manage.py test tests/

console:
	poetry run python manage.py shell

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate