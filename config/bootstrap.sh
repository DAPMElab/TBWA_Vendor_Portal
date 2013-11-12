#!/usr/bin/env bash

# update everything
apt-get -y update

# git
apt-get -y install git-core git

# node
apt-get -y install python-software-properties python g++ make
add-apt-repository ppa:chris-lea/node.js
apt-get -y update
apt-get -y install nodejs

# vim
apt-get -y install vim

# curl
apt-get -y install curl

# zsh
apt-get -y install zsh git-core git
git clone git://github.com/robbyrussell/oh-my-zsh.git /home/vagrant/.oh-my-zsh
git clone git://github.com/zsh-users/zsh-syntax-highlighting.git /home/vagrant/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
sudo -u vagrant -H cp /home/vagrant/.oh-my-zsh/templates/zshrc.zsh-template /home/vagrant/.zshrc
chsh -s $(which zsh) vagrant

# grunt 
npm install -g grunt grunt-cli

# sass
/opt/vagrant_ruby/bin/gem install sass
echo PATH=$PATH:/opt/vagrant_ruby/bin/sass >> /home/vagrant/.zshrc

# rethinkdb
sudo add-apt-repository -y ppa:rethinkdb/ppa
sudo apt-get -y update
sudo apt-get -y install rethinkdb

# python
apt-get -y install python
apt-get -y install python-pip
apt-get -y install pylint
# install all declared requirements
sudo pip install -r /vagrant/config/requirements.txt


