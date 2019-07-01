# Venue Project 2019

## Virtual Environment Instructions:

### Requirements:  
Python3 (`apt-get install python3`)  
pip3 (`apt-get install python3-pip`)  
venv module for python3 (`apt-get install python3-venv`)  

### Installation and activation
1. Create virtual env (`python3 -m venv env`) *Only do this the first time*
2. Avtivate environment (`source env/bin/activate`)
3. Install requirements (`pip install -r requirements.txt`)

When done, use (`deactivate`) to exit virtual env

## Add/update requirements

1. Activate environment (`Source env/bin/activate`)
2. install package using pip 
3. run (`pip freexe --local > requirements.txt`)

## Run Project Instructions:

### In development
#### If needed:
1. Migrations (`python3 manage.py makemigrations`)
2. Migrate (`python3 manage.py migrate`)
#### Run server:
3. Run Server (`python3 manage.py runserver`)