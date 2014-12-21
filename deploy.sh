. ../env/bin/activate
cd ../app/
pip install -r requirements/production.txt
./manage.py collectstatic --noinput
./manage.py migrate
sudo supervisorctl restart muscn
