setup:
	python3 -m pip install -r requirements.txt

build:
	python3 build.py build

clean:
	python3 build.py clean

restore:
	python3 build.py restore

default: clean build
