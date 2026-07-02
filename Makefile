.PHONY: nice

nice:
	uv run isort .
	uv run black .
