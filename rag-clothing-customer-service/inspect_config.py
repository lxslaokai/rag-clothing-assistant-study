import json
from pathlib import Path
from inspect_prompt import build_prompt
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).with_name("prompt_config.json"),
    )
    args = parser.parse_args()
    config_path = args.config.resolve()

    config_text = config_path.read_text(encoding="utf-8")
    try:
        config = json.loads(config_text)
    except json.JSONDecodeError as error:
        parser.error(f"配置文件不是有效的JSON：{error}")

    if "question" not in config:
        parser.error("配置缺少必填字段：question")

    reference_path = config_path.parent / config["reference_file"]
    reference = reference_path.read_text(encoding="utf-8")
    text = build_prompt(config["question"], reference)
    print(text)
