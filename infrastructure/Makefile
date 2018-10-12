SOURCES := $(shell echo src/*.py)
TARGETS := $(patsubst src/%.py,templates/%.json,$(SOURCES))

all: clean venv/bin/activate $(TARGETS)

clean:
	rm -rf $(TARGETS)

cleanvenv:
	rm -rf venv

templates/%.json: src/%.py
	venv/bin/python $< > $@

venv/bin/activate:
	virtualenv --version || echo "Please install python virtualenv on your system."
	test -d venv || virtualenv venv --system-site-packages
	venv/bin/pip install -r requirements.txt
