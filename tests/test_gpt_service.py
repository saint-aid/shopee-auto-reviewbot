import os
import csv
import sys
import types
import tempfile
import unittest
from unittest.mock import patch

# Provide a minimal openai stub if openai is unavailable
try:
    import openai  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback for testing env
    openai = types.ModuleType("openai")

    class ChatCompletion:
        @staticmethod
        def create(*args, **kwargs):
            return {}

    openai.ChatCompletion = ChatCompletion
    openai.api_key = None
    sys.modules['openai'] = openai

# Provide a minimal pandas stub if pandas is unavailable
try:
    import pandas as pd  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback for testing env
    pd = types.ModuleType("pandas")

    class DataFrame(list):
        def __init__(self, rows):
            super().__init__(rows)

        def to_csv(self, path, index=False):
            if not self:
                return
            with open(path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self[0].keys())
                writer.writeheader()
                for row in self:
                    writer.writerow(row)

        def apply(self, func, axis=1):
            return [func(row) for row in self]

        def __setitem__(self, key, values):
            if isinstance(key, str):
                for row, val in zip(self, values):
                    row[key] = val
            else:
                super().__setitem__(key, values)

        def __getitem__(self, key):
            if isinstance(key, str):
                return [row.get(key) for row in self]
            return super().__getitem__(key)

    def read_csv(path):
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            return DataFrame([dict(r) for r in reader])

    pd.DataFrame = DataFrame
    pd.read_csv = read_csv
    sys.modules['pandas'] = pd

from app.gpt_service import generate_reply, bulk_generate


class TestGPTService(unittest.TestCase):
    def test_generate_reply_returns_message(self):
        expected = "mock message"
        with patch('app.gpt_service.openai.ChatCompletion.create') as mock_create:
            mock_create.return_value = {
                "choices": [{"message": {"content": expected}}]
            }
            reply = generate_reply("some review")
            self.assertEqual(reply, expected)

    def test_bulk_generate_writes_replies(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_csv = os.path.join(tmpdir, "input.csv")
            output_csv = os.path.join(tmpdir, "output.csv")

            # create simple CSV without pandas
            with open(input_csv, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["content", "seller_response"])
                writer.writeheader()
                writer.writerow({"content": "review1", "seller_response": ""})
                writer.writerow({"content": "review2", "seller_response": ""})

            responses = [
                {"choices": [{"message": {"content": "reply1"}}]},
                {"choices": [{"message": {"content": "reply2"}}]},
            ]

            with patch('app.gpt_service.openai.ChatCompletion.create') as mock_create:
                mock_create.side_effect = responses
                result_df = bulk_generate(input_csv=input_csv, output_csv=output_csv)
                self.assertEqual(mock_create.call_count, 2)

            # read the output CSV using csv module for compatibility
            with open(output_csv, newline="") as f:
                reader = list(csv.DictReader(f))
            replies = [row["reply"] for row in reader]
            self.assertEqual(replies, ["reply1", "reply2"])
            # result_df should reflect same replies
            self.assertEqual(result_df["reply"], ["reply1", "reply2"])


if __name__ == '__main__':
    unittest.main()
