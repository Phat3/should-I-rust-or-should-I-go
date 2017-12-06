SRCDIR = src
BUILDDIR = build
EXECNAME = commander

all: dir $(EXECNAME)

dir:
	mkdir -p $(BUILDDIR)

$(EXECNAME): frontend.a 
	go tool link -o $(BUILDDIR)/$(EXECNAME) -extld clang -buildmode exe -linkmode external -v -extldflags='-lcore -L./$(SRCDIR) -ldl'  $(BUILDDIR)/frontend.a
	rm $(BUILDDIR)/glue_custom.o $(BUILDDIR)/frontend.a

frontend.a: glue_custom.o
	cp $(SRCDIR)/frontend.a $(BUILDDIR)/frontend.a
	go tool pack r $(BUILDDIR)/frontend.a $(BUILDDIR)/glue_custom.o

glue_custom.o: $(SRCDIR)/glue_custom.s
	go tool asm -I "$(shell go env GOROOT)/pkg/include" -D GOOS_darwin -D GOARCH_amd64 -o $(BUILDDIR)/glue_custom.o $(SRCDIR)/glue_custom.s

clean:
	rm -rf $(BUILDDIR)

