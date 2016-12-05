all: training_analysis test_analysis

training_test:
	@python C_training_analysis.py
	@python C_test_analysis.py

heatmap: 
	@python C_heatmap.py

statistics:
	@python C_statistics.py

training_analysis:
	@python3 C_training_analysis.py
	@python3 R_training_check_results.py
	@python3 F_training_results.py
	R --no-save < F_training_results.r


test_analysis:
	@python3 C_test_analysis.py
	@python3 C_test_plots.py
	@python3 F_test_results.py
	R --no-save < F_test_results.r

clean: 
	rm *.bin.tsv
	rm *.tex
	rm *.pdf

plot_training_analysis:
	@python3 F_training_results.py
	R --no-save < F_training_results.r

plot_test_analysis:
	@python3 F_test_results.py
	R --no-save < F_test_results.r
