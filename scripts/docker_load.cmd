@echo off
PUSHD ..\tests

docker pull redis:latest
docker pull lexxai/web_hw_09:latest
                  

POPD