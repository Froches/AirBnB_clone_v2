#!/usr/bin/env bash
#Sets up your web servers for the deployment of web_static.
sudo apt get update
sudo apt install nginx
mkdir /data/
mkdir /data/web_static
mkdir /data/web_static/releases
mkdir /data/web_static/shared
mkdir /data/web_static/releases/test
touch /data/web_static/releases/test/index.html
echo "This is some content to test my nginx configuration"> /data/web_static/releases/test/index.html
rm -f /data/web_static/current && ln -s /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
echo "
server {
    # Other configurations...

    location /hbnb_static {
        alias /data/web_static/current/;
    }

    # Other configurations...
}
" > /etc/nginx/sites-available/
sudo service restart nginx
