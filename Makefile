SRCDIR = src
BUILDDIR = build

all: dir rustgo

dir:
	mkdir -p $(BUILDDIR)

rustgo: rustgo.a libhello.a
	go tool link -o $(BUILDDIR)/rustgo -extld clang -buildmode exe -buildid b01dca11ab1e -linkmode external -v -extldflags='-lhello -L./$(BUILDDIR) -ldl'  $(BUILDDIR)/rustgo.a

rustgo.a: $(SRCDIR)/hello.go hello.o
	go tool compile -o $(BUILDDIR)/rustgo.a -p main -buildid b01dca11ab1e -pack $(SRCDIR)/hello.go
	go tool pack r $(BUILDDIR)/rustgo.a $(BUILDDIR)/hello.o

hello.o: $(SRCDIR)/hello.s
	go tool asm -I "$(shell go env GOROOT)/pkg/include" -D GOOS_darwin -D GOARCH_amd64 -o $(BUILDDIR)/hello.o $(SRCDIR)/hello.s

libhello.a: $(SRCDIR)/hello.rs
	rustc -g -O --crate-type=staticlib --out-dir $(BUILDDIR) $(SRCDIR)/hello.rs

clean:
	rm -rf $(BUILDDIR)

