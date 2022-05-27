
install:
	poetry install

package-install:
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest -vv

test-coverage:
	poetry run pytest --cov=page_loader/ tests/ --cov-report xml

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

.PHONY: install test lint selfcheck check build




