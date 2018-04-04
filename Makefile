all:
	cd pythonpath; make

dist:
	make
	zip -r numbertext-`head -1 VERSION`.oxt .

clean:
	cd pythonpath; make clean
