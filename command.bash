python scripts/download_data.py \
    --url="https://archive.ics.uci.edu/static/public/2/adult.zip" \
    --target_dir="data/raw"

python scripts/read_and_validate.py \
    --raw_dir="data/raw/adult.data" \
    --processor_dir="data/processed"

python scripts/eda.py \
    --processed_dir="data/processed/cleaned_data.csv" \
    --results_dir="results/figures"