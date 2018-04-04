all:
	cd pythonpath; make
	cat description.xml.in | bin/shellhtml >description.xml
	cd web; make
	cp src/Soros.py web/webroot
	cp src/Soros.js web/webroot
	cp doc/*.pdf web/webroot

dist:
	make
	cd web; make clean
	cd test; make clean
	zip -r numbertext-`head -1 VERSION`.oxt .

check:
	cd test; make

clean:
	cd pythonpath; make clean
	cd web; make clean
