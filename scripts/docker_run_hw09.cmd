@echo off
PUSHD ..\tests

docker run -it --rm  --name web_hw_09  --env-file ../.env lexxai/web_hw_09

rem docker volume ls
                    

POPD