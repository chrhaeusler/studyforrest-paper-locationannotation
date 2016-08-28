all: paper.pdf

paper/results_def.tex: data/structure.csv
	python3 code/descriptive_stats.py | tee paper/results_def.tex

paper.pdf: paper/p.tex paper/results_def.tex
	$(MAKE) -C paper
	cp paper/p.pdf paper.pdf

clean:
	$(MAKE) -C paper clean
	rm -f paper.pdf
