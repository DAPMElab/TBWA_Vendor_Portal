#!/usr/bin/env bash

# update everything
apt-get -y update

# git
apt-get -y install git-core git

# zsh
apt-get -y install zsh git-core git
git clone git://github.com/robbyrussell/oh-my-zsh.git /home/vagrant/.oh-my-zsh
git clone git://github.com/zsh-users/zsh-syntax-highlighting.git /home/vagrant/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
sudo -u vagrant -H cp /home/vagrant/.oh-my-zsh/templates/zshrc.zsh-template /home/vagrant/.zshrc
chsh -s $(which zsh) vagrant

# rethinkdb
sudo add-apt-repository -y ppa:rethinkdb/ppa
sudo apt-get -y update
sudo apt-get -y install rethinkdb
# configure rethinkdb
sudo cp /etc/rethinkdb/default.conf.sample /etc/rethinkdb/instances.d/instance1.conf
sudo echo "bind=all" >> /etc/rethinkdb/instances.d/instance1.conf
sudo echo "http-port=8080" >> /etc/rethinkdb/instances.d/instance1.conf

# python
apt-get -y install python
apt-get -y install python-pip
apt-get -y install pylint
# install all declared requirements
sudo pip install -r /vagrant/config/requirements.txt


