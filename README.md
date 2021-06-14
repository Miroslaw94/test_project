# Test project
This is a test project for python developer. 


## Installation
This project require Python version 3.6 or newer with packages listed in `requirements.txt` file. To install all of 
these packages go to main directory of this project (where you will find `requirements.txt` file) and use command

    pip install -r requirements.txt

After successful installation of packages go to `/project/test_project` directory and use command
`python manage.py runserver` to run django server. Swagger documentation will be available at 
`http://localhost:8000/swagger`



#### Reminder
This project should not be considered as production ready, since it contains unsafe django secret key and is in 
debug mode. 
