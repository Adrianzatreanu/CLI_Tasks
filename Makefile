run_client: build_client
	docker run -it -t test_client bash

run_image: build_image
	docker run -t test_image

build_image:
	docker build -t test_image tasks_image/

build_client:
	docker build -t test_client test_client/
