python scripts/download_data.py \
    --url="https://archive.ics.uci.edu/static/public/2/adult.zip" \
    --target_dir="data/raw"

python scripts/read_and_validate.py \
    --raw_dir="data/raw/adult.data" \
    --processor_dir="data/processed"

python scripts/eda.py \
    --processed_dir="data/processed/cleaned_data.csv" \
    --results_dir="results/figures"

python scripts/split_and_fit.py \
    --processed_dir="data/processed/cleaned_data.csv" \
    --results_dir="results/figures" \
    --preprocessed_dir="data/processed"

python scripts/evaluate_model.py \
    --x_dir="data/processed/X_test.csv" \
    --y_dir="data/processed/y_test.csv" \
    --results_dir="results/figures" \
    --pickle_loc="results/figures/model.pickle"