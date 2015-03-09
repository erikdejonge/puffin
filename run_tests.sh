#!/usr/bin/env bash
python3 tests.py

git commit -am "test `date`"
git push
docker build puftestp27 .