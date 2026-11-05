from langchain_core.prompts import ChatPromptTemplate
import logging
import argparse
from pathlib import Path

template = ChatPromptTemplate.from_messages([
    ("system", "依据参考资料回答，不编造。参考资料：{context}"),
    ("human", "{input}"),
])

def build_prompt(question, reference):
    if not question.strip():
        raise ValueError("问题不能为空")

    prompt = template.invoke({
        "context": reference,
        "input": question,
    })
    return prompt.to_string()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )
    logger = logging.getLogger("prompt_demo")

    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--reference")
    source.add_argument("--reference-file")
    args = parser.parse_args()

    try:
        if args.reference_file is not None:
            reference = Path(args.reference_file).read_text(encoding="utf-8")
        else:
            reference = args.reference
        text = build_prompt(args.question, reference)
    except FileNotFoundError as error:
        parser.error(f"无法读取参考资料：{error}")
    except ValueError as error:
        parser.error(str(error))

    logger.info(f"提示词组装成功，字符数={len(text)}")
    print(text)