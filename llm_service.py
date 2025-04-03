from llama_cpp import Llama
import config

llm = Llama(model_path=config.LLM_MODEL_PATH, n_ctx=1024, n_threads=4, n_batch=128)

def generate_response(prompt, max_tokens=256):
    result = llm(prompt, max_tokens=max_tokens, stop=["Запит:", "Відповідь:"])
    return result['choices'][0]['text'].strip()
