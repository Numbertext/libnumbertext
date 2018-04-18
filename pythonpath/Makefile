# convert all ../data/*.sor files to name_*.py Python modules
BIN=../bin

all: org/Numbertext/Soros.py org/Numbertext/places.py org/Numbertext/locales.py \
  $(addprefix numbertext_, $(addsuffix .py, $(basename $(notdir $(wildcard ../data/*.sor)))))

org/Numbertext/Soros.py: ../src/Soros.py
	cp ../src/Soros.py org/Numbertext/

org/Numbertext/places.py: ../src/places.py
	cp ../src/places.py org/Numbertext/

#org/Numbertext/%.py: ../data/%.sor $(BIN)/Convert.py
numbertext_%.py: ../data/%.sor $(BIN)/Convert.py
	python $(BIN)/Convert.py $< >$@

org/Numbertext/locales.py: $(addprefix numbertext_, $(addsuffix .py, $(basename $(notdir $(wildcard ../data/*.sor)))))
	python $(BIN)/locales.py $(basename $(notdir $(wildcard ../data/*.sor))) $(shell cat ../data/*.sor | grep -Eo '\[:.....:]' | tr '-' '_' | tr -d '[]:' | sort | uniq) >org/Numbertext/locales.py

clean:
	rm -f $(addprefix numbertext_, $(addsuffix .py, $(basename $(notdir $(wildcard ../data/*.sor)))))
	rm -f org/Numbertext/places.py* org/Numbertext/locales.py* org/Numbertext/Soros.py*
