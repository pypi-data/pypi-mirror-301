from xbrain.utils.openai_utils import chat
from xbrain.xbrain_tool import run_tool, tools


def run(messages, chat_model=True, user_prompt=None):
    openai_tools = []
    for tool in tools:
        # 如果是 chat 模式，不把内置工具加入到 openai_tools 中
        if chat_model and tool["name"].startswith("XBrain"):
            continue
        else:
            openai_tools.append(tool)
    
    print("##find actions## \n" + 
          "\n".join([f"{num}: {tool['name']} {tool['path']}" for num, tool in enumerate(openai_tools)]) +
          "\n"
          )
    chat_response = chat(messages, tools=[i["model"] for i in openai_tools], user_prompt=user_prompt)
    if chat_response.content is None:
        res = run_tool(chat_response)
    else:
        res = chat_response.content
    return "\n".join(map(str, res)) if isinstance(res, list) else res
