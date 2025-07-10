from pyhub.llm import OpenAILLM

llm = OpenAILLM(
    model="gpt-4o",
    max_tokens=2000,
    system_prompt="유저 메시지에 어울리는 블로그 도입부를 써줘.",
)

prompt = "우리는 무엇으로 사는가?"
for reply in llm.ask(prompt, stream=True):
    print(reply.text, end="", flush=True)
print()
