# convert all ../data/*.sor files to name_*.py Python modules
BIN=../bin

all: numbertext_titles.py numbertext_locales.py \
  $(addprefix numbertext_, $(addsuffix .py, $(basename $(notdir $(wildcard ../data/*.sor)))))

numbertext_%.py: ../data/%.sor $(BIN)/Convert.py
	python $(BIN)/Convert.py $< >$@

numbertext_titles.py: ../data/titles.txt $(BIN)/ConvertTitles.py
	python $(BIN)/ConvertTitles.py $< >$@

numbertext_locales.py: $(addprefix numbertext_, $(addsuffix .py, $(basename $(notdir $(wildcard ../data/*.sor)))))
	python $(BIN)/locales.py $(basename $(notdir $(wildcard ../data/*.sor))) >numbertext_locales.py

clean:
	rm -f numbertext_*.py
