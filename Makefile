setup:
	uv sync

build:
	uv run python build.py build

serve: build
	uv run zensical serve

clean:
	uv run python build.py clean

.PHONY: setup build serve clean
