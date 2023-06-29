.DEFAULT_GOAL := run
PIP = .venv\Scripts\pip
PYTHON = .venv\Scripts\python.exe

# Install packages
install:
	@$(MAKE) create-venv
	$(PIP) install -r requirements.txt

# create the .venv if there isn't
create-venv:
	@if not exist ".venv" ( \
		echo Creating virtual environment... && \
		py -m venv .venv  )
# Run the server
run:
	$(PYTHON) manage.py runserver
# Make database migrations
makemigrations:
	$(PYTHON) manage.py makemigrations
migrate:
	$(PYTHON) manage.py migrate
# collect static files
collectstatic:
	$(PYTHON) manage.py collectstatic --noinput
# Delete database content
flush:
	$(PYTHON) manage.py flush --noinput
clean:
	rmdir /s /q .venv
	rmdir /s /q static
