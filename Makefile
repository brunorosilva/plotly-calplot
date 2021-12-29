package := "plotly_calplot"

st_example:
	@poetry run streamlit run examples/streamlit_fig.py
pt_example:
	@poetry run streamlit run examples/plotly_fig_show.py

lint:
	black .
	isort .

install:
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
	@poetry install

checks:
	@poetry run flake8 .
	@poetry run vulture .
	@poetry run poetry check