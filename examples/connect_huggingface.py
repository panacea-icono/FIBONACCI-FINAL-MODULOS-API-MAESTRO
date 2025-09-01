import os
import sys

try:
    from huggingface_hub import InferenceApi
except ImportError:
    print("Install dependency: pip install huggingface_hub", file=sys.stderr)
    raise

MODEL_ID = os.getenv("HF_MODEL", "distilbert-base-uncased-finetuned-sst-2-english")
HF_TOKEN = os.getenv("HF_TOKEN")

api = InferenceApi(repo_id=MODEL_ID, token=HF_TOKEN)
result = api(inputs="Tu entrada aquí")
print(result)
