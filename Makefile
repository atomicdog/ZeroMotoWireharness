setup:
	uv sync

build:
	uv run python build.py build

clean:
	uv run python build.py clean

.PHONY: setup build clean
