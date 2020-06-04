
#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
# cd /home/o2store/www/o2store_be
# git pull

source ~/.profile
echo "$DOCKER_PASSWORD" | docker login --username $DOCKER_USERNAME --password-stdin
docker stop o2store_be
docker rm o2store_be
docker rmi mush60/testing-docker:latest
docker run -d --name o2store_be -p 5000:5000 mush60/testing-docker:latest