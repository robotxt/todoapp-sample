TEST_ENVIRONMENT := -e SECRET_KEY=abc \
										-e ENVIRONMENT=test
CONTAINER := web


.PHONY: pipfreezerequirements
pipfreezerequirements:
	docker-compose run --rm --no-deps $(CONTAINER) \
		pip3 freeze > requirements.txt


.PHONY: shell
shell:
	docker-compose run --rm --no-deps $(CONTAINER) \
		python todo/manage.py shell_plus


