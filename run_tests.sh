#!/usr/bin/env bash
python3 tests.py

git commit -am "test `date`"
git push

docker build --no-cache=true -t puftestp27 .
docker run -it --rm puftestp27 python /puffin/tests.py