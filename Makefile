.DEFAULT_GOAL := run
PIP = .venv\Scripts\pip
PYTHON = .venv\Scripts\python.exe

# Install packages from requirements.txt file
.PHONY : install
install:
	@$(MAKE) create-venv
	$(PIP) install -r requirements.txt

.PHONY : create-venv
# create the .venv if there isn't
create-venv:
	@if not exist ".venv" ( \
		echo Creating virtual environment... && \
		py -m venv .venv  )
.PHONY : run
# Run the server
run:
	$(PYTHON) manage.py runserver
.PHONY : migrations
# Make database migrations
migrations:
	$(PYTHON) manage.py makemigrations
.PHONY : migrate
# update the database if any changes
migrate:
	$(PYTHON) manage.py migrate
.PHONY : collectstatic
# collect static files
collectstatic:
	$(PYTHON) manage.py collectstatic --noinput
.PHONY : flush
# Delete database content
flush:
	$(PYTHON) manage.py flush --noinput
.PHONY : clean
# Delete the .venv and the static file so you can run make install again
clean:
	rmdir /s /q .venv
	rmdir /s /q static

.PHONY: package
# install a package so I don't have to activate the .venv to install a package
package:
	$(PIP) install $(filter-out $@,$(MAKECMDGOALS))
	$(PIP) freeze > requirements.txt
	@echo Installed successfully
