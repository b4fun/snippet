package main

import (
	"context"
	"fmt"
	"log"
	"math/rand"
	"net"
	"os"
	"time"

	"google.golang.org/grpc"
	pb "google.golang.org/grpc/examples/helloworld/helloworld"
	"google.golang.org/grpc/reflection"
)

type server struct {
	pb.UnimplementedGreeterServer
}

func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
	log.Printf("Received: %v", in.GetName())
	return &pb.HelloReply{Message: fmt.Sprintf("Hello %s, from default server", in.GetName())}, nil
}

type blockServer struct {
	pb.UnimplementedGreeterServer
}

func (s *blockServer) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
	log.Printf("Received: %v", in.GetName())

	time.Sleep(getBlockTime())

	return &pb.HelloReply{Message: fmt.Sprintf("Hello %s, from block server", in.GetName())}, nil
}

func getPort() string {
	if v := os.Getenv("PORT"); v != "" {
		return v
	}

	return ":50051"
}

func getBlockTime() time.Duration {
	d := 3 * time.Second
	if v := os.Getenv("BLOCK_DURATION"); v != "" {
		vv, err := time.ParseDuration(v)
		if err == nil {
			d = vv
		}
	}

	return time.Duration(rand.Int63n(int64(d)))
}

func getServerToUse() string {
	if v := os.Getenv("SERVER_TYPE"); v != "" {
		return v
	}

	return ""
}

func init() {
	rand.Seed(time.Now().UnixNano())
}

func main() {
	lis, err := net.Listen("tcp", getPort())
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()

	var serverImpl pb.GreeterServer
	switch getServerToUse() {
	case "block":
		serverImpl = &blockServer{}
		log.Print("using block server")
	default:
		serverImpl = &server{}
		log.Print("using default server")
	}

	pb.RegisterGreeterServer(s, serverImpl)

	reflection.Register(s)

	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
