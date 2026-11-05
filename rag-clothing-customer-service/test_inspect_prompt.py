from inspect_prompt import build_prompt
import pytest
import subprocess
import sys
from pathlib import Path


def test_build_prompt():
    text = build_prompt(
        "M码上衣的胸围是多少？",
        "M码上衣：胸围96-100cm。",
    )
    assert "参考资料：M码上衣：胸围96-100cm。" in text
    assert "Human: M码上衣的胸围是多少？" in text
    assert "不编造" in text

@pytest.mark.parametrize("question", ["", "   ", "\t\n"])
def test_build_prompt_rejects_blank_question(question):
    with pytest.raises(ValueError, match="问题不能为空"):
        build_prompt(question, "M码上衣：胸围96-100cm。")

def test_cli_uses_question_and_reference():
    script = Path(__file__).resolve().with_name("inspect_prompt.py")
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(script),
         "--question", "M码上衣的胸围是多少？",
         "--reference", "M码上衣：胸围96-100cm。"],
        capture_output=True,
        encoding="utf-8",
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert "Human: M码上衣的胸围是多少？" in result.stdout
    assert "参考资料：M码上衣：胸围96-100cm。" in result.stdout

def test_cli_rejects_blank_question():
    script = Path(__file__).resolve().with_name("inspect_prompt.py")
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(script),
         "--question", "   ",
         "--reference", "M码上衣：胸围96-100cm。"],
        capture_output=True,
        encoding="utf-8",
        timeout=10,
    )
    assert result.returncode == 2, result.stderr
    assert "问题不能为空" in result.stderr
    assert result.stdout == ""
    assert "Traceback" not in result.stderr

def test_cli_reads_reference_file(tmp_path):
    reference_file = tmp_path / "reference.txt"
    reference_file.write_text("L码上衣：胸围100-104cm。", encoding="utf-8")
    script = Path(__file__).resolve().with_name("inspect_prompt.py")
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(script),
         "--question", "L码上衣的胸围是多少？",
         "--reference-file", str(reference_file)],
        capture_output=True,
        encoding="utf-8",
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert "参考资料：L码上衣：胸围100-104cm。" in result.stdout
    assert "Human: L码上衣的胸围是多少？" in result.stdout

def test_cli_reports_missing_reference_file(tmp_path):
    missing_file = tmp_path / "missing.txt"
    script = Path(__file__).resolve().with_name("inspect_prompt.py")
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(script),
         "--question", "L码上衣的胸围是多少？",
         "--reference-file", str(missing_file)],
        capture_output=True,
        encoding="utf-8",
        timeout=10,
    )
    assert result.returncode == 2, result.stderr
    assert "无法读取参考资料" in result.stderr
    assert result.stdout == ""
    assert "Traceback" not in result.stderr

def test_reports_invalid_json(tmp_path):
    config_file = tmp_path / "bad.json"
    config_file.write_text('{"question": ', encoding="utf-8")
    script = Path(__file__).resolve().with_name("inspect_config.py")
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(script), "--config", str(config_file)],
        cwd=tmp_path,
        capture_output=True,
        encoding="utf-8",
        timeout=10,
    )
    assert result.returncode == 2, result.stderr
    assert "配置文件不是有效的JSON" in result.stderr
    assert result.stdout == ""
    assert "Traceback" not in result.stderr