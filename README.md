# flash_card_serv

## virtualenv set up
	virtualenv venv_name
	source venv_name/bin/activate
	pip install -r requirements.txt

## database set up
> #### info
>	flask db
>command added by **flask-migrate**
>generate everything related to database migrations

create the migration repository:
	
	flask db init


generate automatic migration script:

	flask db migrate -m "<comment>"

apply migration script:

	flask db upgrate

## run the server
Use `flask run` to run the server locally.
Use `flask run --host=0.0.0.0` for it to be publicky available

## flask shell
Use `flask shell` command to run a python shell with database classes imported.
Add the classes you want to be able to access to in the	`make_shell_context` function definition in **flask_card_serv.py** file.









