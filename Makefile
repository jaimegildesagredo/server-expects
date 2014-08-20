test:
	docker build --rm -t server_expects_tests .
	docker run --env-file .test-env server_expects_tests
