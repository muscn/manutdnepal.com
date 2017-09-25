. ../env/bin/activate
cd ../app/
pip install -r requirements/production.txt  | grep -v 'Requirement already satisfied' | grep -v 'Cleaning up...'
./manage.py migrate -v 0
circusctl restart muscn
