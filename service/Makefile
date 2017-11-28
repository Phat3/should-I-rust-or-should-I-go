.PHONY: all service bundle spawn clean
SERVICE=should_i_rust_or_should_i_go.py

all: bundle

service:
	cp src/$(SERVICE) service/ro/

bundle: service
	rm -f ../$(SERVICE).tgz
	tar -czvf ../$(SERVICE).tgz *
	@echo "#### Double check ../$(SERVICE).tgz and submit it :) ####"

spawn: service
	( cd service/rw && socat tcp-l:6666,reuseaddr,fork exec:"../ro/$(SERVICE)" )

clean:
	rm -f service/rw/*
	touch service/rw/you_can_prepopulate_your_rw_dir
