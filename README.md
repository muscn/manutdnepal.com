This is the source code for [http://manutd.org.np](http://manutd.org.np), the official site of Manchester United Supporters' Club, Nepal. Developer setup instructions follow.


### 1. Install
```
virtualenv env # create a virtual environment
source env/bin/activate # Enter the virtual environment
git clone git@github.com:muscn/manutd.org.np.git app # git clone the repo
cd app # cd to project dir
pip install -r requirements/development.txt # install Python packages required for development
cp app/local_settings.sample.py app/local_settings.py # create local settings file from sample file
vi app/local_settings.py # configure your settings here, database, static & media paths and urls
./manage.py migrate # synchronize database and run migrations
./manage.py collectstatic # collect static files
```

### 2. Run
```
./manage.py runserver
```

### 3. Add cronjobs
`crontab -e`  
```
*/5 * * * * source /home/manutd/.bashrc && source /home/manutd/env/bin/activate && python /home/manutd/app/manage.py scrape table > /home/manutd/logs/cronjob.log
@daily source /home/manutd/.bashrc && source /home/manutd/env/bin/activate && python /home/manutd/app/manage.py scrape tv > /home/manutd/logs/cronjob.log
0 7,15,23 * * * source /home/manutd/.bashrc && source /home/manutd/env/bin/activate && python /home/manutd/app/manage.py scrape injuries > /home/manutd/logs/cronjob.log
```

### 4. Auto deploy via Git
#`visudo`
  ```
manutd ALL= NOPASSWD: /usr/local/bin/supervisorctl restart muscn
```


### 5. Rejoice!
