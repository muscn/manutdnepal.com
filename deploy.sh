. ../env/bin/activate
pip install -r requirements/production.txt
./manage.py collectstatic --noinput
./manage.py migrate
sudo supervisorctl restart muscn
