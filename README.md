# Cindicator test task

[![Build Status](https://travis-ci.com/marky24/cindicator_test.svg?branch=main)](https://travis-ci.com/github/marky24/cindicator_test)  
Test task for Cindicator company. Junior data engineer position  
![Gifochka](https://media.giphy.com/media/zk58NdoX6xZfLdR8kI/giphy.gif)
## Installing
To install script, execute following commands
```
$ git clone https://github.com/marky24/cindicator_test.git  
$ cd cindicator_test
```
## Running the tests
To run tests execute:
```
$ sudo docker exec philippov_test_container python3 test/tests.py

```
**Only after execution all commands from "Run script" section**
## Run script

You can pass args with `config.ini` or pass them from console
```
$ sudo docker build -t philippov_test .  
$ sudo docker run --rm -it    --user=$(id -u)    --env="DISPLAY"    --workdir=/app    --volume="$PWD":/app    --volume="/etc/group:/etc/group:ro"    --volume="/etc/passwd:/etc/passwd:ro"    --volume="/etc/shadow:/etc/shadow:ro"    --volume="/etc/sudoers.d:/etc/sudoers.d:ro"    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v "$PWD/config.ini:/usr/project/config/config.ini" --name philippov_test_container philippov_test  
```
if you have problems with launch, you need to type  
```
$ xhost +
```  
to give docker access to X server. If you get error after it, install X server with  
```
$ sudo apt-get install x11-xserver-utils
```
