NAME = $(shell python setup.py --name)
VERSION = $(shell python setup.py --version)
DIST = dist/$(NAME)-$(VERSION).tar.gz
TEST_DIST = data/$(NAME).tar.gz

test: sdist
	cp $(DIST) $(TEST_DIST)
	kitchen test

sdist:
	python setup.py sdist

list:
	kitchen list

destroy:
	kitchen destroy

distclean: clean
	rm -f $(DIST)

clean:
	rm -f $(TEST_DIST)
