SRCDIR = ./src
BUILDDIR = ../rw/build
EXECNAME = commander

all: dir $(EXECNAME)

dir:
	mkdir -p $(BUILDDIR)

$(EXECNAME): frontend.a 
	go tool link -o $(BUILDDIR)/$(EXECNAME) -extld clang -buildmode exe -linkmode external -v -extldflags='-lcore -L./$(SRCDIR) -ldl'  $(BUILDDIR)/frontend.a
	rm $(BUILDDIR)/glue.o $(BUILDDIR)/frontend.a

frontend.a: glue.o
	cp $(SRCDIR)/frontend.a $(BUILDDIR)/frontend.a
	go tool pack r $(BUILDDIR)/frontend.a $(BUILDDIR)/glue.o

glue.o: $(SRCDIR)/glue.s
	go tool asm -I "$(shell go env GOROOT)/pkg/include" -D GOOS_darwin -D GOARCH_amd64 -o $(BUILDDIR)/glue.o $(SRCDIR)/glue.s

clean:
	rm -rf $(BUILDDIR)

