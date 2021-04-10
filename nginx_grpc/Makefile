SERVER_IMG_REPO_BASE ?= b4fun/nginx_grpc_example_
SERVER_IMG_TAG ?= latest

all: greeter_server_image greeter_client

.PHONY: greeter_server
greeter_server:
	GOOS=linux go build -o ./bin/greeter_server_linux_amd64 ./server

.PHONY: greeter_server_image
greeter_server_image: greeter_server
	docker build . \
		-f ./server.Dockerfile \
		-t "${SERVER_IMG_REPO_BASE}greeter_server:${SERVER_IMG_TAG}"

.PHONY: greeter_client
greeter_client:
	go build -o ./bin/greeter_client google.golang.org/grpc/examples/helloworld/greeter_client/