#!/bin/sh

cd $APP_PATH

# create tables
echo "Updating Database Tables"
./manage.py makemigrations
./manage.py migrate
echo "The Database has been updated"

# create admin user
echo "Superuser..."
cat /create_superuser.py | ./manage.py shell

# run the server
echo "Starting the server..."
python manage.py runserver &
echo "Starting the background tasks..."
python manage.py process_tasks
