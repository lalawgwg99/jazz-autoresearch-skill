import os
import json
import csv
import anthropic

class HypothesisGenerator:
    def __init__(self, history_file="results.tsv"):
        self.history_file = history_file
        self._prompt_template = None

    def _load_prompt_template(self):
        if self._prompt_template is None:
            template_path = os.path.join(os.path.dirname(__file__), "prompt_template.md")
            with open(template_path, "r") as f:
                self._prompt_template = f.read()
        return self._prompt_template

    def read_history(self, limit=10):
        if not os.path.exists(self.history_file):
            return []
        history = []
        with open(self.history_file, "r") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                history.append(row)
        return history[-limit:]

    def _build_history_table(self, history):
        if not history:
            return "(no experiments yet)"
        lines = ["timestamp | hypothesis | val_bpb | improved | config"]
        lines.append("-" * 80)
        for row in history:
            lines.append(f"{row['timestamp']} | {row['hypothesis'][:40]} | {row['val_bpb']} | {row['improved']} | {row['config']}")
        return "\n".join(lines)

    def generate_next_hypothesis(self):
        history = self.read_history()

        if not history:
            return {
                "hypothesis_description": "Initial experiment: default config",
                "proposed_config_changes": {"n_layer": 8}
            }

        best_score = min(float(r["val_bpb"]) for r in history if r["val_bpb"] != "N/A")
        history_table = self._build_history_table(history)

        prompt = self._load_prompt_template()
        prompt = prompt.replace("{{best_score}}", str(best_score))
        prompt = prompt.replace("{{history_table}}", history_table)

        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": prompt}]
        )

        text = next((b.text for b in response.content if b.type == "text"), None)
        if text:
            # 擷取 JSON 區塊（可能被 markdown code fence 包住）
            if "```" in text:
                text = text.split("```")[1].lstrip("json").strip()
            return json.loads(text)

        # fallback
        return {
            "hypothesis_description": "LLM returned no parseable output, trying n_layer+1",
            "proposed_config_changes": {"n_layer": 9}
        }
