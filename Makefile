run:
	bash scripts/run.sh

build:
	python -m scripts.freeze
	python -m scripts.serve

deploy: export APP_CONFIG=Deploy
deploy:
	python -m scripts.freeze
	# python -m scripts.deploy

install:
	pipenv install
	python -m scripts.install

viewdb:
	mongo --port 5009
