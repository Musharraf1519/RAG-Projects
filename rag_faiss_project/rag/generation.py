from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class RAGGenerator:
    """
    CPU-friendly generator for RAG.
    Uses Flan-T5 small model for lightweight inference.
    """

    def __init__(self, model_name="google/flan-t5-small", device="cpu"):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.model.to(device)
        print(f"[INFO] Loaded {model_name} on {device}")

    def generate_answer(self, context: str, query: str, max_length=200):
        """
        Generate an answer given context and query.
        Combines retrieved context and query into a prompt for the model.
        """
        input_text = f"Context: {context}\nQuestion: {query}\nAnswer:"
        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_length,
            do_sample=True,
            top_p=0.95,
            top_k=50
        )

        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer
