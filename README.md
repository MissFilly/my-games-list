### Set up your development environment:

    $ sudo apt-get install python-pip virtualenv
    $ virtualenv env && source env/bin/activate
    $ pip install -r requirements.txt

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
