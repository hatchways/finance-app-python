# Finance App Work Simulation

Welcome to the Python Finance App work simulation by [Hatchways](http://hatchways.io/). In this project, you will be 
writing a couple of back-end API routes on a Python FastAPI back-end API. 

We will use [this rubric](https://drive.google.com/file/d/17p8-OdTxKF8bhCn_YwpQ4UPBIh13bDOo/view?usp=sharing) to evaluate your submission. Please note that if your submission does not attempt to complete all of the requirements, or does not pass our plagiarism screening, we will be unable to provide feedback on it. Please contact hello@hatchways.io if you have any questions or concerns.

Below is some high level detail about the project. Good luck!

## Language & Tools

- [Python 3.6+](https://www.python.org/downloads/)
- [FastAPI](https://fastapi.tiangolo.com/) - web framework
- [Pydantic](https://pydantic-docs.helpmanual.io/) for type parsing and validation
- [SQLAlchemy](https://www.sqlalchemy.org/) and [SQLite](https://www.sqlite.org/) for the database (you will not be 
  required to write any database queries in order to complete this project) 

## Tips

### Provided functions

The project contains helper functions you can use to complete your tasks without writing any SQL or ORM logic:
* `AccountCrud.get_accounts` in the [crud folder](api/crud) can be used to fetch all account details
* `TransactionCrud.get_transactions_for_range` in the [crud folder](api/crud) can be used to fetch transaction data 
  by date

### Seed data

We've included sample data that the application has been configured to use. For more information on how the database 
is set up, please reference [Database](#Database).

## Quickstart

This section contains all the information required for getting the server up and running.

Python 3 should be used for this project. Depending on your environment and Python setup, you may need to use `pip3` and
`python3` instead of `pip` and `python` for the commands outlined below.

### Installing Dependencies

We highly recommend using a virtual environment for this project. Ensure you're using Python 3.6+, activate your virtual
environment, then install all dependencies with `pip install -r requirements.txt`. Creating a virtual environment is an
optional step, but makes it easier to manage your python packages on your machine.

Note: you may be prompted to install rust, since the `cryptography` package 
[depends on rust](https://cryptography.io/en/latest/faq/#why-does-cryptography-require-rust). After installing rust, you
will likely need to reload your terminal before reattempting installation. If you continue to have issues installing 
`cryptography`, you can try upgrading `pip`.

Other common issues with this step are outlined [below](#common-setup-errors).

#### Note for VS Code users

If VS Code doesn't detect your virtual environment automatically, make sure to set your python environment manually to, 
for example `venv/bin/python`.

### Run the server

Create a .env file in the root directory, and copy the contents from [.env.sample](.env.sample).

`python main.py` - launches the FastAPI server in debug mode (with hot-reloading).

### Testing Routes
Once the server is running, you can go to `localhost:8080/docs` or `localhost:8080/redoc` to see the auto-generated API 
documentation. You can use cURL, Postman, or another tool of your choice to make requests to the API.

#### Example cURL Commands
You can log in as the seeded account with the following command:
```bash
curl --request POST 'localhost:8080/api/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "test@test.com",
    "password": "sample"
}'
```
You can then use the token returned from the `/api/login` request to make an authenticated request to get the user:
```bash
curl 'localhost:8080/api/user' \
--header 'Authorization: Bearer YOUR-TOKEN-HERE'
```

### Unit tests

`python -m pytest tests/ -s -v` - runs all the tests with [pytest](https://docs.pytest.org/en/6.2.x/contents.html). 
We've provided you with a few example tests and some fixtures to get you started.

#### Adding your own tests

If a ticket requires it, you can add a new test file to the `tests` folder. Ensure any new test files start with `test_`.

**Note:** Please do NOT modify the test files that are already present.

### Formatting

Black, a Python formatter, is included in the environment and can be used to format your code. 
To run it, simply execute `black .` from the root directory.

## Database

**Note: No database setup should be required to get started with running the project.** 

This project uses SQLite, which stores your tables inside a file. The `.env` file configures the project to use 
`database.db` for development and `database_test.db` for unit tests:
* `database.db` is committed into the repository and already has seed data
* `database_test.db` gets reset every time the tests are run and is therefore not committed into Git.

#### Resetting the Database

If you would like to reset your development database, two scripts are provided:

`python db_init.py` - this will initialize the database schema and should give the following output:

![image](https://user-images.githubusercontent.com/5796488/153083276-a92b4aa5-c404-46ed-a9e7-c61ff60d72b7.png) 

`python seed.py` - this will seed the starting data and should give the following output:

![image](https://user-images.githubusercontent.com/5796488/153083273-6ccc5165-72f0-4109-a409-2307d913754c.png)

`seed.py` uses sample data located in the `/seed_data` directory to populate the database. You may need to run 
`python db_init.py` prior to running `python seed.py` 

## Common Setup Errors
**Error**
```
error: invalid command 'bdist_wheel'
  ----------------------------------------
  ERROR: Failed building wheel for python-multipart
```
**Suggestions**
* Try running `pip install wheel` then try again. 
