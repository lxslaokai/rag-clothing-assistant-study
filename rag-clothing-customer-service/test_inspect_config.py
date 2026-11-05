import json
import subprocess
import sys
from pathlib import Path


def test_uses_selected_config(tmp_path):
    reference_file = tmp_path / "reference.txt"
    reference_file.write_text("L码上衣：胸围100-104cm。", encoding="utf-8")
    settings = {
        "question": "L码上衣的胸围是多少？",
        "reference_file": "reference.txt",
    }
    config_file = tmp_path / "settings.json"
    config_file.write_text(json.dumps(settings, ensure_ascii=False), encoding="utf-8")
    script = Path(__file__).resolve().with_name("inspect_config.py")
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(script), "--config", str(config_file)],
        cwd=tmp_path,
        capture_output=True,
        encoding="utf-8",
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert "参考资料：L码上衣：胸围100-104cm。" in result.stdout
    assert "Human: L码上衣的胸围是多少？" in result.stdout