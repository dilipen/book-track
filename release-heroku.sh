#echo `pwd`/restapi/.env.heroku
#echo `pwd`/restapi/.env 
#cp ./restapi/.env.heroku ./restapi/.env
python manage.py makemigrations myapp
python manage.py migrate
