@echo off
PUSHD ..

docker build . -t lexxai/web_hw_09
docker images

POPD