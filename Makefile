package := "plotly-calplot"

lint:
	black .
	isort .

install:
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
	@poetry install

checks:
	@poetry run flake8 .
	# poetry run black --check plotly-calplot tests
	# poetry run mypy plotly-calplot
	# poetry run mypy ./tests/**.py
	# poetry run pytest
	@poetry run vulture .
	@poetry run poetry check