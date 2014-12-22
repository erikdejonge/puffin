publish:
	rm dist/*
	python setup.py sdist
	twine upload dist/*

cover:
	coverage run --omit="venv/*" -m unittest discover tests
	coverage report
	coverage html
	open htmlcov/index.html