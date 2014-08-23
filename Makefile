test:
	vagrant ssh -c '/vagrant/dev/vagrant-tests.sh'

provision:
	vagrant provision
