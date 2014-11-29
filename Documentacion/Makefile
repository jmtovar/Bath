ALL=proyecto.pdf rubrica.pdf

ARTIFACTS=$(addsuffix .aux,$(basename $(ALL))) \
          $(addsuffix .bbl,$(basename $(ALL))) \
          $(addsuffix .blg,$(basename $(ALL))) \
          $(addsuffix .log,$(basename $(ALL))) \
          $(addsuffix .out,$(basename $(ALL))) \
          $(addsuffix .pdf,$(basename $(ALL)))

ALL:$(ALL)

%.pdf:%.tex
	pdflatex $?
	\rm -f $*.aux $*.log

proyecto.pdf:proyecto.tex
	pdflatex $?
	bibtex $(basename $?)
	pdflatex $?
	pdflatex $?
	\rm -f proyecto.aux proyecto.bbl proyecto.blg proyecto.log proyecto.out

clean:
	\rm -f $(ARTIFACTS)
