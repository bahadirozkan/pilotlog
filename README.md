## Import/Export Django App
After pulling the repo, build the project with <br>
``` docker-compose build ``` <br>
Then to run <br>
``` docker-compose up -d ``` <br>
Migrate the Django project with <br>
``` docker-compose exec web python manage.py makemigrations ``` and <br>
``` docker-compose exec web python manage.py migrate ``` <br>
## Import
From the browser, go to http://127.0.0.1:8000/import/ to import the json file. Use the [file](https://github.com/bahadirozkan/pilotlog/blob/main/files/import%20-%20pilotlog_mcc.json) that is provided in the repo. It will redirect once the import is finished. Data analysis is avaible in [Exploratory Data Analysis.](https://github.com/bahadirozkan/pilotlog/blob/main/files/Exploratory%20Data%20Analysis%20.ipynb) ImportDataSerializer in data_handler -> serializers handle the manupulation of data.
## Export
After the import is finished, you can export the file from http://127.0.0.1:8000/api/export This will download the file as .csv
## Test
run ``` docker-compose exec web python manage.py test data_handler.tests ```
