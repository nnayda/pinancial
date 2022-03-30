
linter-build:
	@docker build -t pinancial-python-linter python-linter/.
	chmod +x python-linter/entrypoint.sh

lint:
	@docker run \
			--name pinancial-python-linter-python-linter \
			--rm \
			-it \
			-v $(PWD):/src \
			pinancial-python-linter
