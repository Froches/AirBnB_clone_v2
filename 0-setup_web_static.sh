#!/usr/bin/env bash
# Install Nginx if not installed

if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary folders if they don't exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
sudo touch /data/web_static/releases/test/index.html

# Create a simple HTML content for the test index.html file
echo "<html><head><title>Test Page</title></head><body>Test Page</body></html>" | sudo tee /data/web_static/releases/test/index.html

# Remove existing symbolic link and create a new one
sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content to hbnb_static
config_text="location /hbnb_static/ {\n\talias /data/web_static/current/;\n}\n"
sudo sed -i "/server_name _;/a $config_text" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0
