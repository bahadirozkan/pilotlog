## Import/Export Django App 
After pulling the repo, build the project with 
``` docker-compose build ``` 
Then to run ``` docker-compose up -d ``` 
Migrate the Django project with
``` docker-compose exec web python manage.py makemigrations ``` and 
``` docker-compose exec web python manage.py migrate ``` 
## Import 
From the browser, go to http://127.0.0.1:8000/import/ to import the json file. It will redirect once the import is finished. Use the [modified file](https://github.com/bahadirozkan/pilotlog/blob/main/files/modified_pilotlog.json) that is provided in the repo Explanation of the modification is avaible in [Exploratory Data Analysis](https://github.com/bahadirozkan/pilotlog/blob/main/Exploratory%20Data%20Analysis%20.ipynb) 
## Export 
After the import is finished, you can export the file from http://127.0.0.1:8000/api/export This will download the file as .csv 
