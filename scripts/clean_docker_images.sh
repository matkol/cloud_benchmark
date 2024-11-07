# remove old conntainers
docker ps -qa --no-trunc --filter "status=exited" 2>/dev/null | xargs --no-run-if-empty docker rm
# now remove "dangling" images
docker images --filter "dangling=true" -q --no-trunc 2>/dev/null | xargs --no-run-if-empty docker rmi
# remove cstr docker containers
# docker ps -a | tr -s " " | cut -d " " -f -2 | grep cstr | cut -d " " -f 1 | xargs --no-run-if-empty docker rm -f
