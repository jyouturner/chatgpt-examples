import os
import openai
import json


def post_chatgpt_process(diy_schema):
    """Get the parts URL"""
    print("seatching internal API to get the part URL")
    return json.dumps(diy_schema)


# the JSON schema for ChatGPT to conver the text response to. In this case, ChatGPT will decide the part name, and instructions
# in the response it will return the JSON data instead of text. Then we can use the JSON data to call our own function to
# populdate the URL of the part based on the name
schema = {
    "type": "object",
    "properties": {
        "parts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    # "url": {"type": "string"},
                    "amount": {"type": "number"},
                },
                "required": ["name", "amount"],
            },
        },
        "instructions": {
            "type": "array",
            "description": "Steps to finish the task (no numbering)",
            "items": {"type": "string"},
        },
    },
    "required": ["parts", "instructions"],
}

openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=[
        {
            "role": "system",
            "content": "You are a DIY assistant from the Home Depot. You output structured data for function home_depot_service_params",
        },
        {
            "role": "user",
            "content": "Provide purchase list and step by step guide to fix leaking toilet",
        },
    ],
    functions=[{"name": "post_chatgpt_process", "parameters": schema}],
    function_call={"name": "post_chatgpt_process"},
    temperature=0,
)
message = response["choices"][0]["message"]
if message.get("function_call"):
    function_name = message["function_call"]["name"]
    function_args = json.loads(message["function_call"]["arguments"])
    print(function_args)
    revised_response = post_chatgpt_process(function_args)
    print(revised_response)
else:
    print(message)
# print(resonse.choices[0].message.function_call.arguments)
