# Cindicator test task 
Test task for Cindicator company. Junior data engineer position

##Installing
To install script, execute following commands
```
$ https://github.com/marky24/cindicator_test.git  
$ cd cindicator_test
```
##Running the tests
To run tests execute:
```
$ python3 test/tests.py
```
## How to use?
```
$ sudo docker build -t philippov_test .  
$ sudo docker run --rm -it    --user=$(id -u)    --env="DISPLAY"    --workdir=/app    --volume="$PWD":/app    --volume="/etc/group:/etc/group:ro"    --volume="/etc/passwd:/etc/passwd:ro"    --volume="/etc/shadow:/etc/shadow:ro"    --volume="/etc/sudoers.d:/etc/sudoers.d:ro"    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v "$PWD/config.ini:/usr/project/config/config.ini" philippov_test  
```
