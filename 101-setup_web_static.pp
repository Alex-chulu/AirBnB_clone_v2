#!/usr/bin/env bash

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null
then
    echo "Installing Nginx..."
    wget https://apt.puppetlabs.com/puppet-release-bionic.deb
    dpkg -i puppet-release-bionic.deb
    apt-get update
    apt-get -y install puppet-agent
fi

# Create required directories
echo "Creating directories..."
mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file for testing
echo "<html><head></head><body><p>Nginx web server is running!</p></body></html>" > /data/web_static/releases/test/index.html

# Create a symbolic link to the test release, and give ownership to ubuntu
echo "Creating symbolic link..."
if [ -L /data/web_static/current ]
then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve

