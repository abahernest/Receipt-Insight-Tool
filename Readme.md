
#

STEPS TO RUN THE APP LOCALLY

APPROACH 1

1. Clone the repo and `cd` into the repo folder
2. Ensure Python and Pipenv are installed on your machine
3. Install dependencies by running 
```
>> pipenv shell
>> pipenv install
```
4. Setup postgres locally and create a database for the application
5. create a `.env` file that contains the necessary information found in `env.example`
6. Make database migrations. 
```
>> python manage.py migrate
```
7. Start Application
```
>> python manage.py runserver
```

APPROACH 2 (With Docker Compose)
1. Clone the appplication and `cd` into the repo folder
2. Run the command below to startup the postgres db as well as the api server
```
>> docker compose up
```

TEST
```
>> python
```

POSTMAN DOCUMENTATION
[Postman Doc](https://documenter.getpostman.com/view/11044390/2s7YYu4hju)