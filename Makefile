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

stubs:
	@poetry run mypy --install-types --non-interactive plotly_calplot
	@poetry run python3 -m pip install types-pytz

pypi_deploy:
	@poetry config pypi-token.pypi $(PLOTLY_PRD_TOKEN)
	@poetry build
	@poetry publish

testpypi_deploy:
	@poetry config repositories.test-pypi https://test.pypi.org/legacy/
	@poetry config pypi-token.test-pypi $(PLOTLY_DEV_TOKEN)
	@poetry build
	@poetry publish -r test-pypi