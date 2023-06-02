def get_json_from_file() -> str:
    with open("reply.txt", "r") as reply:
        content = reply.read()
        content = content.replace("json", "", 1)
        return content.split("```")[1]


def save_to_json_file(code_content: str):
    with open("class_skeleton.json", "w") as class_skeleton:
        class_skeleton.write(code_content)


def get_code_from_reply(text_content: str) -> str:
    code = text_content.split("```")[1]
    code = code.replace("python", "", 1)
    return code
