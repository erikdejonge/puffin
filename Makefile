publish:
	rm dist/*
	python setup.py sdist
	twine upload dist/*

cover:
	coverage run --omit="venv/*,tests/*,/usr/local/lib/python*" -m unittest discover tests
	coverage report
	coverage html
	open htmlcov/index.html

test:
	python -m unittest discover