# flask-api-template
Backend Flask API template using Postgres

This README describes how to setup the environment and run the flask server

Based on the template found here https://github.com/spchuang/DoubleDibz-tutorial/tree/master/FINAL

## Installing Dependencies
This has been developed using python 3.6. You are recommended to use Anaconda or virtualenv to hold the dependencies to not pollute the system installs.

To install all packages and clean up the directory afterwards do
```
python setup.py install
python setup.py clean
```

## Postgres

Install Postgres

This can be accomplished on mac using homebrew with the command
```
brew install postgres
```
#### Running Postgres in the Foreground
Run postgres before doing the following commands either in the foreground or background
To run in the foreground use the command on mac
```
postgres -D /usr/local/var/postgres
```

#### Open postgres user:
```
sudo su - postgres
```

#### Open PSQL using:
```
psql
```
if the above command does not work then do 
```
sudo -u username psql postgres
```
where username is your username

#### Create a database user
```
create role XXX with createdb login password 'XXX';
```

### Create development database
To create the development database and test database run the following
```
CREATE DATABASE XXX OWNER XXX;
CREATE DATABASE XXX OWNER XXX;
```

### Running Postgres in the Background and Restarting
If you would like to keep postgres running in the background and restart it use the command
```
sudo service postgresql restart
```

### Creating the Database Tables
To create the database tables you must run the following command in the root directory
```
python manage.py initdb
```

## Running the Application
To run the application you must run the following command in the root directory
```
python manage.py run
```
