@echo off
PUSHD ..

docker-compose up -d code 
timeout 1
docker attach hw09-code-1

docker-compose down 

POPD