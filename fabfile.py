from fabric.api import task, local


@task
def publish():
    local('rm dist/*')
    local('python setup.py sdist')
    local('twine upload dist/*')


@task
def cover():
    local('coverage run --omit="venv/*,tests/*,/usr/local/lib/python*" -m unittest discover tests')
    local('coverage report')
    local('coverage html')
    local('open htmlcov/index.html')


@task
def test(path='discover'):
    local('python -m unittest ' + path)
