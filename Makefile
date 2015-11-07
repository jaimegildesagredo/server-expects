KITCHEN_OPTIONS=-c 2

test:
	kitchen test $(KITCHEN_OPTIONS) $(KITCHEN_INSTANCE)

converge:
	kitchen converge $(KITCHEN_OPTIONS) $(KITCHEN_INSTANCE)

verify:
	kitchen verify $(KITCHEN_OPTIONS) $(KITCHEN_INSTANCE)

list:
	kitchen list $(KITCHEN_INSTANCE)

destroy:
	kitchen destroy $(KITCHEN_OPTIONS) $(KITCHEN_INSTANCE)

ec2_test:
	ssh-keygen -q -b 2048 -t rsa -f $(AWS_SSH_KEY_PATH) -N ''
	aws ec2 import-key-pair --key-name $(AWS_SSH_KEY_ID) --public-key-material "`cat $(AWS_SSH_KEY_PATH).pub`"
	KITCHEN_DRIVER=ec2 kitchen test $(KITCHEN_OPTIONS) $(KITCHEN_INSTANCE)

ec2_list:
	KITCHEN_DRIVER=ec2 kitchen list $(KITCHEN_INSTANCE)

ec2_destroy:
	KITCHEN_DRIVER=ec2 kitchen destroy $(KITCHEN_OPTIONS) $(KITCHEN_INSTANCE)
	aws ec2 delete-key-pair --key-name $(AWS_SSH_KEY_ID)
	rm -f $(AWS_SSH_KEY_PATH) $(AWS_SSH_KEY_PATH).pub

.PHONY: test converge verify list destroy ec2_test ec2_list ec2_destroy
