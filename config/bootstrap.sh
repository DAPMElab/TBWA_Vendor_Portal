#!/usr/bin/env bash

# update everything
apt-get -y update

# git
apt-get -y install git-core git

# nginx
apt-get -y install nginx 

# zsh
apt-get -y install zsh git-core git
git clone git://github.com/robbyrussell/oh-my-zsh.git /home/vagrant/.oh-my-zsh
git clone git://github.com/zsh-users/zsh-syntax-highlighting.git /home/vagrant/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
sudo -u vagrant -H cp /home/vagrant/.oh-my-zsh/templates/zshrc.zsh-template /home/vagrant/.zshrc
chsh -s $(which zsh) vagrant

# python
apt-get -y install python
apt-get -y install python-pip
apt-get -y install python-software-properties
# install all declared requirements
sudo pip install flask
sudo pip install gunicorn
sudo pip install rethinkdb
sudo pip install passlib
sudo pip install -r /vagrant/config/requirements.txt

# rethinkdb
sudo add-apt-repository -y ppa:rethinkdb/ppa
sudo apt-get -y update
sudo apt-get -y install rethinkdb
# configure rethinkdb
sudo cp /etc/rethinkdb/default.conf.sample /etc/rethinkdb/instances.d/instance1.conf
sudo echo "bind=all" >> /etc/rethinkdb/instances.d/instance1.conf
sudo echo "http-port=8080" >> /etc/rethinkdb/instances.d/instance1.conf

