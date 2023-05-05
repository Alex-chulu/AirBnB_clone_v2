#!/usr/bin/env bash

# Install Nginx if it's not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install nginx -y
fi

# Create the necessary directories if they don't already exist
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create a fake HTML file in /data/web_static/releases/test/
sudo echo "<html><head></head><body>Hello World!</body></html>" > /data/web_static/releases/test/index.html

# Create or update the symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration file
sudo sed -i '/listen 80 default_server;/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Restart Nginx to apply changes
sudo service nginx restart
