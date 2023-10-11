@echo off
PUSHD ..

docker-compose up -d code --build
timeout 1
docker attach hw09-code-1

docker-compose down 

POPD