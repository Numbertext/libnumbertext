all:
	cat index.html.in | ../bin/shellhtml >webroot/index.html
	cat Soros.html.in | ../bin/shellhtml >webroot/Soros.html
	cat AUTHORS.html.in | ../bin/shellhtml >webroot/AUTHORS.html

clean:
	rm -f webroot/index.html webroot/Soros.html webroot/AUTHORS.html webroot/*.pdf
	rm -f webroot/Soros.py webroot/Soros.js
