from pathlib import Path
from typing import List, Tuple, Union

import pandas as pd


def read_jsonl(path: Union[str, Path]) -> Tuple[List[str], List[str]]:
    df = pd.read_json(str(path), orient='records', lines=True)
    return list(df.text), list(df.label_id)
