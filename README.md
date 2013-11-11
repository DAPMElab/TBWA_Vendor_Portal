
#TBWA

###Running Tests

You'll need an instance of rethinkdb running on port 28015.  
Add the settings to your environment variables:

    source config/settings.dev

Then simply run `nosetests` from anywhere within the repo.

###RethinkDB

Run with the `--bind all` flag to view the admin console.

You can then view the console through `http://localhost:8080`

###Set Up

http://www.vagrantup.com/

After configuring Vagrant, simply run `vagrant up` and a new virtual machine will be created.
All the software dependencies will be installed.
If dependencies are added, run `vagrant provision` to update.

###Code Conventions

Python: [PEP 8](http://www.python.org/dev/peps/pep-0008/)

Javascript: [Airbnb Guide](https://github.com/airbnb/javascript)

