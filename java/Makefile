all:
	mkdir -p org/numbertext/data
	cp ../data/*.sor org/numbertext/data
	cp -r src/main/java/org .
	CLASSPATH=. javac -encoding utf8 org/numbertext/Numbertext.java
	jar cfm numbertext.jar Manifest.txt org
	java -jar numbertext.jar

check:
	java -jar numbertext.jar -l en 99-101
	java -jar numbertext.jar -l en-GB 99-101
	java -jar numbertext.jar -p ordinal -l en 1-10
