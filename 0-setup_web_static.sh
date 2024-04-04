#!/usr/bin/env bash
# This is a bash script sets up web servers for the deployment of web_static.
if ! command -v nginx &> /dev/null
then
	sudo apt-get -y update
	sudo apt-get -y install nginx
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

html_content="<html>
  <head></head>
  <body> Maha Kamal website </body>
  </html>"
echo "$html_content" > /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data

config="server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
    }
}"
echo "$config" > /etc/nginx/sites-available/default
service nginx restart
