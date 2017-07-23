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

scaleway_test:
	KITCHEN_DRIVER=scaleway kitchen test $(KITCHEN_OPTIONS) $(KITCHEN_INSTANCE)

scaleway_list:
	KITCHEN_DRIVER=scaleway kitchen list $(KITCHEN_INSTANCE)

scaleway_destroy:
	KITCHEN_DRIVER=scaleway kitchen destroy $(KITCHEN_OPTIONS) $(KITCHEN_INSTANCE)

.PHONY: test converge verify list destroy scaleway_test scaleway_list scaleway_destroy
