#!/bin/bash -xe

docker-compose up -d
MAX_TRIES=60
HTTP_CODE=$(curl -sL -w "%{http_code}\\n" localhost:8121/keys -o /dev/null || true)
while [[ $HTTP_CODE != 200 && $MAX_TRIES > 0 ]] ; do
  sleep 1
  HTTP_CODE=$(curl -sL -w "%{http_code}\\n" localhost:8121/keys -o /dev/null || true)
  MAX_TRIES=$(( MAX_TRIES - 1 ))
done
docker run -it --rm --net=pacificapolicy_default -e METADATA_URL=http://metadataserver:8121 -e PYTHONPATH=/usr/src/app pacifica/metadata python test_files/loadit.py
docker run -it --rm --net=pacificapolicy_default -e METADATA_URL=http://metadataserver:8121 -v $PWD/test_files:/usr/src/app/test_files -e PYTHONPATH=/usr/src/app pacifica/metadata python test_files/loadit.py
docker-compose stop policyserver

export PYTHONPATH=$PWD
coverage run --include='policy/*' -m pytest -v
coverage report -m --fail-under=100
codeclimate-test-reporter