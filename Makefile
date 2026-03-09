TOOLBOX = fedora

setup:
	toolbox run --container $(TOOLBOX) uv sync

build:
	toolbox run --container $(TOOLBOX) uv run python build.py build

clean:
	toolbox run --container $(TOOLBOX) uv run python build.py clean

.PHONY: setup build clean
