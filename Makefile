
MODEL_FILE = $(shell ls -1 model/model_*.json 2>/dev/null | sort | tail -n 1)

ifneq ($(wildcard .env), )
	include .env
	IMAGE_NAME := ${DOCKER_USER}/mlz
	CAN_PUBLISH := 1
else
	IMAGE_NAME := mlz
endif


build:
ifeq ($(MODEL_FILE),)
	docker build -t ${IMAGE_NAME} .
else
	docker build --build-arg MODEL_FILE=$(MODEL_FILE) -t ${IMAGE_NAME} .
endif

publish:
ifneq ($(CAN_PUBLISH),)
	docker push $(IMAGE_NAME):latest
else
	@echo "action not available"
endif

run:
	docker run -it -p 8081:8081 ${IMAGE_NAME}
