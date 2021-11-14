dev:
	bash scripts/run.sh

build:
	python -m scripts.freeze
	python -m scripts.serve

serve:
	python -m scripts.serve

images: export REPROC_IMAGES=True
images:
	python -m scripts.process_images

deploy: export APP_CONFIG=Deploy
deploy:
	python -m scripts.freeze
	python -m scripts.deploy

upgrade:
	pip-compile requirements.in
	pip-compile dev-requirements.in
	pip-sync requirements.txt dev-requirements.txt

install:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt
	npm install
	python -m scripts.install

viewdb:
	mongo --port 5009
