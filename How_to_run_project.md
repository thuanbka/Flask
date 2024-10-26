##HOW to run project in local

# Create a virtual enviroment

python -m venv my_virtual

# Active virtual enviroment

- Windows: .\my_virtual\Scripts\activate
- Linux/MacOS: source venv/bin/activate

# Install requirement:

pip install -r requirement.txt

# Init database postgres:

$ sudo su - postgres
$ psql
$ CREATE USER thuannv WITH PASSWORD 'thuan06121998' CREATEDB;
$ CREATE DATABASE flask_app OWNER thuannv;
$ quit

# Start project

- Init DB run: flask initdb
- Run project: flask run
