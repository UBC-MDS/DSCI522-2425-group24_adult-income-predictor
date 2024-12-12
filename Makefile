# Makefile
# Michael Suriawan, December 2024

.PHONY: all clean

all: report/adult_income_predictor_report.html report/adult_income_predictor_report.pdf

# download and extract data
data/raw/adult.data: scripts/download_data.py
	python scripts/download_data.py \
		--url="https://archive.ics.uci.edu/static/public/2/adult.zip" \
		--target_dir="data/raw"

# read and validate data
data/processed/cleaned_data.csv: scripts/read_and_validate.py \
data/raw/adult.data
	python scripts/read_and_validate.py \
		--raw_dir="data/raw/adult.data" \
		--processor_dir="data/processed"

# EDA
results/figures/eda1.png results/figures/eda2.png results/figures/eda3.png results/figures/eda4.png results/figures/eda5.png results/figures/eda6.png: scripts/eda.py \
data/processed/cleaned_data.csv
	python scripts/eda.py \
		--processed_dir="data/processed/cleaned_data.csv" \
		--results_dir="results/figures"

# Data split and model fit
data/processed/X_test.csv data/processed/y_test.csv results/models/model.pickle: scripts/split_and_fit.py \
data/processed/cleaned_data.csv
	python scripts/split_and_fit.py \
		--processed_dir="data/processed/cleaned_data.csv" \
		--preprocessed_dir="data/processed" \
		--random_seed=522 \
		--models_dir="results/models" \

# Evaluate model
results/figures/cm.png results/table/test_score.csv: scripts/evaluate_model.py \
data/processed/X_test.csv \
data/processed/y_test.csv \
results/models/model.pickle
	python scripts/evaluate_model.py \
		--x_dir="data/processed/X_test.csv" \
		--y_dir="data/processed/y_test.csv" \
		--pickle_loc="results/models/model.pickle" \
		--results_figure_dir="results/figures" \
		--results_table_dir="results/table"

# build HTML report and copy build to docs folder
report/adult_income_predictor_report.html report/adult_income_predictor_report.pdf : report/adult_income_predictor_report.qmd \
report/references.bib \
results/table/test_score.csv \
results/figures/eda1.png \
results/figures/eda2.png \
results/figures/eda3.png \
results/figures/eda4.png \
results/figures/eda5.png \
results/figures/eda6.png \
results/figures/cm.png
	quarto render report/adult_income_predictor_report.qmd --to html
	quarto render report/adult_income_predictor_report.qmd --to pdf

# clean up analysis / nuke everything
clean :
	rm -rf data/raw/*
	rm -rf data/logs/validation_errors.log \
			data/processed/cleaned_data.csv
	rm -rf results/figures/eda1.png \
			results/figures/eda2.png \
			results/figures/eda3.png \
			results/figures/eda4.png \
			results/figures/eda5.png \
			results/figures/eda6.png
	rm -rf data/processed/X_test.csv \
			data/processed/y_test.csv \
			results/models/model.pickle
	rm -rf results/figures/cm.png \
			results/table/test_score.csv
	rm -rf report/adult_income_predictor_report.html \
			report/adult_income_predictor_report.pdf \
			report/adult_income_predictor_report_files