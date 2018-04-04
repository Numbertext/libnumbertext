# convert all ../data/*.sor files to name_*.py Python modules

all: numbertext_titles.py numbertext_locales.py \
  $(addprefix numbertext_, $(addsuffix .py, $(basename $(notdir $(wildcard ../data/*.sor)))))

numbertext_%.py: ../data/%.sor Convert.py
	python Convert.py $< >$@

numbertext_titles.py: ../data/titles.txt ConvertTitles.py
	python ConvertTitles.py $< >$@

numbertext_locales.py: $(addprefix numbertext_, $(addsuffix .py, $(basename $(notdir $(wildcard ../data/*.sor)))))
	./locales.sh $(basename $(notdir $(wildcard ../data/*.sor))) >numbertext_locales.py

clean:
	rm -f numbertext_*.py
