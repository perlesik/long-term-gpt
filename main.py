import openai
from config import API_KEY
import extract_code
import json

openai.api_key = API_KEY
messages = [{"role": "system", "content": "You are an intelligent assistant."}]
json_format = [
    ["class_name", "methods"],
    ["name", "description", "parameters"],
    ["name", "type"]
]


def configure_intro(app_name: str, include_gui: bool, additional_description: str) -> str:
    message = f"Create {app_name} application in Python. "
    if include_gui:
        message += "GUI has to be included. "
    message += f"Additionally, this should be included: {additional_description}. "
    message += f"I want you to make JSON-like representation of a class skeleton. "
    message += f"Format should look like this: {json_format[0]}, "
    message += f"then '{json_format[0][-1]}' should contain {json_format[1]}, "
    message += f"then '{json_format[1][-1]}' should contain {json_format[2]}. "
    message += "It must be of JSON type. Only the JSON representation."
    return message


def intro_query(message: str):
    print(f"Intro: {message}")
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    else:
        return
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})
    with open("reply.txt", "w") as intro_reply:
        intro_reply.write(reply)


def methods_query(app_name: str) -> list:
    methods_query_queue = []
    if type(json_data) == list:
        for class_num in json_data:
            for method in class_num["methods"]:
                class_name = class_num['class_name']
                method_name = method["name"]
                parameters = method["parameters"]
                message = f"I have a class skeleton of an app named {app_name}. I need code in Python for method " \
                          f"named '{method_name}' from class named '{class_name}'. "
                if parameters:
                    message += f"It consists of following parameters: "
                else:
                    message += "It doesn't have any parameters; "
                for d in parameters:
                    message += f"{d['name']} of type {d['type']}; "
                message += "|"
                message = message.replace("; |", ".")
                message += f"Please, give me only the code of method {method_name}."
                # print(message)
                methods_query_queue.append(message)
    else:
        for method in json_data["methods"]:
            class_name = json_data['class_name']
            method_name = method["name"]
            parameters = method["parameters"]
            message = f"I have a class skeleton of an app named {app_name}. I need code in Python for method named " \
                      f"'{method_name}' from class named '{class_name}'. "
            if parameters:
                message += f"It consists of following parameters: "
            else:
                message += "It doesn't have any parameters; "
            for d in parameters:
                message += f"{d['name']} of type {d['type']}; "
            message += "|"
            message = message.replace("; |", ".")
            message += f"Please, give me only the code of method {method_name}."
            # print(message)
            methods_query_queue.append(message)
    return methods_query_queue


def query(message: str, save_content: bool) -> str:
    print(f"User: {message}")
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        messages.pop(-1)
    else:
        return "Message is empty."
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    if save_content:
        messages.append({"role": "assistant", "content": reply})
    return reply


# def dialog():
#     print("<< You are now beginning conversation with ChatGPT. >>")
#     while True:
#         message = input("User: ")
#         if message:
#             messages.append(
#                 {"role": "user", "content": message},
#             )
#             chat = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo", messages=messages
#             )
#         else:
#             return
#         reply = chat.choices[0].message.content
#         print(f"ChatGPT: {reply}")
#         messages.append({"role": "assistant", "content": reply})


def get_methods() -> list | dict:
    with open("class_skeleton.json", "r") as file:
        data = json.loads(file.read())
    return data


if __name__ == '__main__':
    with open("code.txt", "w") as f:
        f.write("")
    with open("reply.txt", "w") as f:
        f.write("")
    with open("class_skeleton.json", "w") as f:
        f.write("")
    # app = input("What application do you want?: ")
    # gui_answer = input("Do you want it to include GUI? (y/n): ")
    # if gui_answer == "y":
    #     gui = True
    # else:
    #     gui = False
    # description = input("Provide additional description if you will: ")
    app, gui, description = "Task Management Tool", True, "deadlines"
    intro = configure_intro(app, gui, description)
    # print("\n" + intro + "\n")
    intro_query(intro)
    json_content = extract_code.get_json_from_file()
    extract_code.save_to_json_file(json_content)
    json_data = get_methods()
    query_queue = methods_query(app)
    for q in query_queue:
        method_reply = query(q, save_content=False)
        with open("code.txt", "a") as c:
            c.write("// ------------------------------------------------------ //")
            c.write(extract_code.get_code_from_reply(method_reply))
            c.write("// ------------------------------------------------------ //")
