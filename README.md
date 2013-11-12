
#TBWA

###Starting the server

1. Start up Vagrant and with `vagrant up`
    - if this is the first time, run `vagrant provision` afterwards to ensure that everything is installed
2. SSH into your Vagrant VM with `vagrant ssh`
3. Navigate to the project directory with `cd /vagrant`
4. Execute `run.sh` to start the database and server

The server will then be running on `http://localhost:5000/`.
You can view the database admin conosle at `http://localhost:8080`.

###Running Tests

#####Simple

Execute `test.sh`in the root of the project.

#####Complicated

If you want to only run individual tests, you need to a rethinkdb instance running on port 28015.
Do this with `sudo service rethinkdb start`.
You'll also need the app settings to your environment variables:
Do this with `source config/settings.dev`.
Then simply run `nosetests` from anywhere within the repo, or run individual tests in `testing/`.

###Set Up

- Install vagrant
  - http://www.vagrantup.com/
- Download a virtualbox image for vagrant to use
  - https://www.virtualbox.org/wiki/Downloads
- You should now be able to simply run `vagrant up`  in a directory with a Vagrantfile and a new virtual machine will be created.
  - All the software dependencies declared in `config/bootstrap.sh` will be installed.
- If dependencies are added, run `vagrant provision` to update.

###Code Conventions

Python: [PEP 8](http://www.python.org/dev/peps/pep-0008/)

Javascript: [Airbnb Guide](https://github.com/airbnb/javascript)

