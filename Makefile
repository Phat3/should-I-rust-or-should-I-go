rustgo: rustgo.a libhello.a
	go tool link -o rustgo -extld clang -buildmode exe -buildid b01dca11ab1e -linkmode external -v -extldflags='-lhello -L/home/phate/seba/shouldl_i_rust_or_should_i_go -ldl'  rustgo.a

rustgo.a: hello.go hello.o
	go tool compile -o rustgo.a -p main -buildid b01dca11ab1e -pack hello.go
	go tool pack r rustgo.a hello.o

hello.o: hello.s
	go tool asm -I "$(shell go env GOROOT)/pkg/include" -D GOOS_darwin -D GOARCH_amd64 -o hello.o hello.s

libhello.a: hello.rs
	rustc -g -O --crate-type staticlib hello.rs

