### Install the required system libraries:

    $ sudo apt-get install curl npm libpq-dev python3-dev build-essential g++ libmemcached-dev

Install PostgreSQL:

    $ sudo apt-get install postgresql postgresql-contrib

(Optional) Install pgAdmin III:

    $ sudo apt-get install pgadmin3

Install Heroku Toolbelt:

    $ wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh

### Set up your development environment:

    $ sudo apt-get install python-pip python-virtualenv
    $ git clone https://github.com/MissFilly/my-games-list.git
    $ cd my-games-list
    $ virtualenv -p /usr/bin/python3.4 env && source env/bin/activate
    $ pip install -r requirements.txt
    $ nodeenv --python-virtualenv
    $ npm install -g less

### Set up your database

If it's your first time running PostgreSQL in your current PC:

    $ sudo -u postgres psql
    postgres=# alter user postgres password 'mypassword';
    ALTER ROLE
    postgres=# create database mydb owner postgres;
    CREATE DATABASE

Then run:

    $ foreman run ./manage.py migrate

Start the local server either running `foreman start` or `foreman run ./manage.py runserver`.

### Local .env file:

    DJANGO_SECRET_KEY='my_secret_key'
    DATABASE_URL='my_database_url'
    COMPRESS_OFFLINE=False
    SENDGRID_PASSWORD='my_sendrid_password'
    SENDGRID_USERNAME='my_sendrid_username'
    
    AWS_ACCESS_KEY_ID='my_aws_access_key'
    AWS_SECRET_ACCESS_KEY='my_aws_secret_key'
    S3_BUCKET_NAME='my_bucket_name'
    
    STEAM_API_KEY='my_steam_api_key'

### Generate `.po` files

    $ cd mygameslist && foreman run -e ../.env ../manage.py makemessages -l es