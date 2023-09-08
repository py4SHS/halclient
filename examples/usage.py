from __future__ import annotations

from pathlib import Path

from halpy import HALClient

client = HALClient()


response = client.search(
    query="python",
    include_fields=["docid", "label_s", "abstract_s"],
    before=2019,
    after=2012,
    rows=100,
    offset=0,
)

Path("result.json").write_text(response.text)
