# cindicator_test
Test task for Cindicator company. Junior data engineer position
## How to use?
`sudo docker run --rm -it    --user=$(id -u)    --env="DISPLAY"    --workdir=/app    --volume="$PWD":/app    --volume="/etc/group:/etc/group:ro"    --volume="/etc/passwd:/etc/passwd:ro"    --volume="/etc/shadow:/etc/shadow:ro"    --volume="/etc/sudoers.d:/etc/sudoers.d:ro"    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v "$PWD/config.ini:/usr/project/config/config.ini" philippov_test`
