package := "plotly_calplot"

st_example:
	@poetry run streamlit run examples/streamlit_fig.py
pt_example:
	@poetry run python3 examples/plotly_fig_show.py

lint:
	@poetry run black .
	@poetry run isort .

install:
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
	@poetry install

checks:
	@poetry run flake8 .
	@poetry run black .
	@poetry run mypy plotly_calplot
	@poetry run mypy ./tests/**.py
	@poetry run pytest tests/
	@poetry run poetry check

pypi_deploy:
	@poetry build
	@poetry publish