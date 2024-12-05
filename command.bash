python scripts/download_data.py \
    --url="https://archive.ics.uci.edu/static/public/2/adult.zip" \
    --target_dir="data/raw"

python scripts/read_and_validate.py \
    --raw_dir="data/raw/adult.data" \
    --processor_dir="data/processed"