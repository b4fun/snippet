FROM gcr.io/distroless/base-debian10

COPY ./bin/greeter_server_linux_amd64 /
CMD ["/greeter_server_linux_amd64"]