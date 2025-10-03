# rag/generator.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class LLMGenerator:
    """Generate natural language answers from context."""

    def __init__(self, model_name='google/flan-t5-base'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def generate(self, context: str, query: str, max_length: int = 256) -> str:
        input_text = f"Context: {context}\nQuestion: {query}\nAnswer:"
        inputs = self.tokenizer(input_text, return_tensors='pt', truncation=True)
        outputs = self.model.generate(**inputs, max_length=max_length)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
