import torch
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    AutoConfig
)
class LLMClient:
    def __init__(self, model_name="google/flan-t5-small", use_4bit=False):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"   Loading {model_name}...")
        print(f"   Device: {self.device}")
        config = AutoConfig.from_pretrained(model_name)
        model_type = config.model_type.lower()
        print(f"   Model Type: {model_type}")
        if model_type in ['t5', 'bart', 'pegasus', 'mbart', 'blenderbot']:
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if use_4bit else None,
                device_map="auto" if use_4bit else None
            )
            self.model_class = "seq2seq"
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if use_4bit else None,
                device_map="auto" if use_4bit else None
            )
            self.model_class = "causal"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        if not use_4bit:
            self.model.to(self.device)
        print(f"Model loaded ({self.model_class})")
    def generate(self, prompt, max_tokens=500, temperature=0.75):
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)
        with torch.no_grad():
            if self.model_class == "seq2seq":
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    top_p=0.9
                )
            else:
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.pad_token_id
                )
        generated_text = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )
        if self.model_class == "causal":
            generated_text = generated_text[len(prompt):].strip()
        
        return generated_text
