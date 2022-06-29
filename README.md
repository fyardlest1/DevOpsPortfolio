# DevOpsPortfolio

## About the project
This project is my portfolio for the DevOps Bootcamp.
The project is a store django app for a potential e-commerce website. 
I use Django and Docker compose to make it work using the knowlage I got from the entire Bootcamp and my own research to make everything works perfectly

## Step 1: How to use?
Before running the project you have to create an environment variable

1. Clone the project folder form GitHub using VS Code or your favorite code editor

2. Open VS Code integrated terminal 

3. Cd into the app/ folder, create a file with the name .env : 

```
    touch .env
```

4. In the .env file, enter the following database settings as key=value pairs that include the credentials to the database:

```
    # Database Settings
    DB_NAME=nc_tutorials_db
    DB_USER=postgres
    DB_PASSWORD=admin123
    DB_HOST=127.0.0.1
    DB_PORT=5432
```

5. Return back to the DevOpsPortfolio project where live the docker-compose.yml file

6. Enter the following command:

```
    docker compose up -d
```

7. Verify that everything is working properly:

```
    docker compose ps
```

8. In a bash terminal from the workshop1/ or workshop1/app/ folder, run:

```
    docker compose exec web python manage.py makemigrations –noinput
```

9. To generate these tables, make sure that your Docker Compose containers are all running, then open a bash terminal and run the following command:

```
    docker compose exec web python manage.py migrate --noinput
```

## Step : Create and access the database
1. Open the pgAdmin web portal and refresh the page to confirm the Django tables were created in the database: 
*http://localhost:5433/browser/*

2. Create a New Server by clicking on: New Server
 
3. Name it fyard (or any name you like)
 
4. In the Connection tab, give it a Hostname/address of pg

5. Set the Password to admin123

6. Leave all other values at their defaults, and Save this server configuration.

7. Connect to this database in the left tree view.

8. Confirm that the fyardlest2_db's public schema contains the application tables/
