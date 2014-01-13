
#TBWA

###Server API

[Documented here](https://github.com/DAPMElab/TBWA/blob/master/src/server/README.md)

###Starting the server

```bash
# this will spawn a supervisor process that will restart the server automatically.
vagrant up
```

The server will then be running on `http://localhost:5000/`.
You can view the database admin conosle at `http://localhost:8080`.

###Running Tests

#####Simple

```bash
vagrant ssh
cd /vagrant
sh test.sh
```

#####Exact

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
- You should now be able to simply run `vagrant up` in a directory with a Vagrantfile and a new virtual machine will be created.
  - All the software dependencies declared in `config/bootstrap.sh` will be installed.
- If dependencies are added, run `vagrant provision` to update.

###Code Conventions

Python: [PEP 8](http://www.python.org/dev/peps/pep-0008/)

Javascript: [Airbnb Guide](https://github.com/airbnb/javascript)

