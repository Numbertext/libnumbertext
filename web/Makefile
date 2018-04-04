all:
	cat index.html.in | ../bin/shellhtml >webroot/index.html
	cat Soros.html.in | ../bin/shellhtml >webroot/Soros.html
	cat AUTHORS.html.in | ../bin/shellhtml >webroot/AUTHORS.html

clean:
	rm webroot/index.html webroot/Soros.html webroot/*.pdf
	rm webroot/Soros.py webroot/Soros.js
