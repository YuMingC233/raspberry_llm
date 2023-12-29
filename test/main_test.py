import requests

proxies = {
  'http': 'http://10.0.69.15:1234',
  'https': 'http://10.0.69.15:1234',
}

response = requests.get('https://google.com', proxies=proxies)
print(response.status_code)

"""
from openai import OpenAI

client = OpenAI()

msg = [
    {"role": "system",
     "content": "你将扮演一位16岁的高中生。你没有义务帮助我，因此无需询问我需要什么帮助；你只需说出符合你目前身份的话，像个正常女高中生即可。"},
    {"role": "user", "content": "你好。今天的天气针不戳！😎😎😎"}
]

stream = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=msg,
    stream=True,
)

print("她说：", end="")
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
print()

while True:
    you_say = input("你说：")

    msg.append({"role": "user", "content": you_say})
    stream = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=msg,
        stream=True
    )

    print("她说：",end="")
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print()
"""