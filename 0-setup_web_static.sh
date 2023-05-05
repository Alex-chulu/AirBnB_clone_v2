#!/usr/bin/env bash

ME=$(whoami)
WEB_STATIC_ROOT=/data/web_static

# Check if running with sudo or root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null
then
  echo "Installing Nginx..."
  apt-get -y update
  apt-get -y install nginx
fi

# Create required directories
echo "Creating folders..."
mkdir -p $WEB_STATIC_ROOT/releases
mkdir -p $WEB_STATIC_ROOT/shared
mkdir -p $WEB_STATIC_ROOT/releases/test

# Create fake HTML file for testing
echo "<html><head></head><body><p>Nginx web server is running!</p></body></html>" > $WEB_STATIC_ROOT/releases/test/index.html

# Create symbolic link and give ownership to ubuntu
echo "Creating symbolic link..."
ln -fs $WEB_STATIC_ROOT/releases/test $WEB_STATIC_ROOT/current
chown -R $ME:$ME $WEB_STATIC_ROOT
chown -R www-data:www-data $WEB_STATIC_ROOT/current

# Update Nginx configuration file
echo "Updating Nginx configuration..."
SITENAME=mydomainname.tech
CONFIG_FILE=/etc/nginx/sites-available/$SITENAME
echo "server {
    listen 80;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name $SITENAME www.$SITENAME;

    location /hbnb_static {
        alias $WEB_STATIC_ROOT/current;
        autoindex off;
    }

    error_page 404 /404.html;
    location = /404.html {
        internal;
        root /var/www/html;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        internal;
        root /var/www/html;
    }
}" > $CONFIG_FILE

# Create symlink
