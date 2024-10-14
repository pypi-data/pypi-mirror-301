from typing import Any, List


def get_truncation_warning_message(instance, limit) -> str:
    return (
        f"Attention: {instance} exceeding the {limit} character limit will be "
        "automatically truncated upon ingestion into the Arize platform. Should you require "
        "a higher limit, please reach out to our support team at support@arize.com"
    )


def log_a_list(list_of_str: List[Any], join_word: str) -> str:
    if list_of_str is None or len(list_of_str) == 0:
        return ""
    if len(list_of_str) == 1:
        return list_of_str[0]
    return f"{', '.join(map(str, list_of_str[:-1]))} {join_word} {list_of_str[-1]}"
