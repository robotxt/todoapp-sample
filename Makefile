TEST_ENVIRONMENT := -e SECRET_KEY=abc \
										-e ENVIRONMENT=test
CONTAINER := web

TEST_SCRIPT = scripts/test.sh

.PHONY: pipfreezerequirements
pipfreezerequirements:
	docker-compose run --rm --no-deps $(CONTAINER) \
		pip3 freeze > requirements.txt


.PHONY: shell
shell:
	docker-compose run --rm --no-deps $(CONTAINER) \
		python todo/manage.py shell_plus


.PHONY: lint
lint:
	docker-compose run --rm --no-deps $(CONTAINER) flake8 .


.PHONY: test
test:
	docker-compose run --rm --no-deps $(TEST_ENVIRONMENT) $(CONTAINER) \
		$(TEST_SCRIPT) $(TEST_ARGS)
