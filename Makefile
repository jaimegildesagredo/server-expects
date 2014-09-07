NAME = $(shell python setup.py --name)
VERSION = $(shell python setup.py --version)
DIST = dist/$(NAME)-$(VERSION).tar.gz
TEST_DIST = data/$(NAME).tar.gz

test: sdist
	cp $(DIST) $(TEST_DIST)
	kitchen test $(KITCHEN_INSTANCE)

sdist:
	python setup.py sdist

list:
	kitchen list $(KITCHEN_INSTANCE)

destroy:
	kitchen destroy $(KITCHEN_INSTANCE)

distclean: clean
	rm -f $(DIST)

clean:
	rm -f $(TEST_DIST)

ec2_test: sdist
	ssh-keygen -q -b 2048 -t rsa -f $(AWS_SSH_KEY_PATH) -N ''
	aws ec2 import-key-pair --key-name $(AWS_SSH_KEY_ID) --public-key-material "`cat $(AWS_SSH_KEY_PATH).pub`"
	cp $(DIST) $(TEST_DIST)
	KITCHEN_YAML=.kitchen.cloud.yml kitchen test $(KITCHEN_INSTANCE)

ec2_list:
	KITCHEN_YAML=.kitchen.cloud.yml kitchen list $(KITCHEN_INSTANCE)

ec2_destroy:
	KITCHEN_YAML=.kitchen.cloud.yml kitchen destroy $(KITCHEN_INSTANCE)
	aws ec2 delete-key-pair --key-name $(AWS_SSH_KEY_ID)
