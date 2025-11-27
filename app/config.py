from app.engine.chat_engine import run_toy_llm
MODEL_REGISTRY = {
    "toy-llm-v1": run_toy_llm,
    # later: "llama-3-8b": LlamaRunner(...)
}