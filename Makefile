check:
	python -m pytest -v . && \
		flake8 -v . && \
		mypy -v .
