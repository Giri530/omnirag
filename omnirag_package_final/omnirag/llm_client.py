from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
class LLMClient:
    def __init__(self, model_name="Qwen/Qwen2.5-0.5B-Instruct", use_4bit=False):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.is_qwen = "qwen" in model_name.lower()
        self.is_t5 = "t5" in model_name.lower()
        print(f"   Loading {model_name}...")
        print(f"   Device: {self.device}")
        print(f"   Model Type: {'Qwen' if self.is_qwen else 'T5'}")
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        if use_4bit and self.device == "cuda":
            from transformers import BitsAndBytesConfig
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=quantization_config,
                device_map="auto",
                trust_remote_code=True
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True
            )
            if self.device == "cpu":
                self.model = self.model.to(self.device)
    def generate(self, prompt, max_tokens=512, temperature=0.75, system_prompt=None):
        try:
            if self.is_qwen:
                return self._generate_qwen(prompt, max_tokens, temperature, system_prompt)
            else:
                return self._generate_t5(prompt, max_tokens, temperature)
        except Exception as e:
            print(f" Generation error: {e}")
            return ""
    def _generate_qwen(self, prompt, max_tokens, temperature, system_prompt):
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        messages.append({
            "role": "user",
            "content": prompt
        })
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        with torch.no_grad():
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                top_p=0.95,
                pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id
            )
        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response.strip()
    def _generate_t5(self, prompt, max_tokens, temperature):
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True
        ).to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_tokens,
                temperature=temperature if temperature > 0 else 1.0,
                do_sample=temperature > 0,
                top_p=0.95,
                pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id
            )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.strip()
    def clear_cache(self):
        if self.device == "cuda":
            torch.cuda.empty_cache()
