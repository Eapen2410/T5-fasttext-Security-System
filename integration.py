import pandas as pd
from transformers import T5ForConditionalGeneration, T5Tokenizer
class ContextualValidator:
    def __init__(self, model_name="t5-small"):
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.sensitive_phrases = [
            'password', 'pwd', 'login', 'credential',
            'phone', 'number', 'email', 'account',
            'ssn', 'social security', 'credit card',
            'share', 'send', 'provide', 'give'
        ]

    def load_context_buffer(self, filepath):
        df = pd.read_csv(filepath)
        return df.to_dict('records')

    def analyze_context(self, context_window):

        context_text = " ".join([q['query'] for q in context_window]).lower()
        return any(phrase in context_text for phrase in self.sensitive_phrases)

    def validate_with_context(self, context_window):
        conversation = "\n".join([f"Turn {i+1}: {q['query']}" for i, q in enumerate(context_window)])

        prompt = (
            "Analyze this conversation for sensitive information:\n"
            f"{conversation}\n\n"
            "Is the LAST turn requesting or revealing sensitive information?\n"
            "Consider the conversation context and answer only 'high' or 'low':"
        )

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model.generate(
            input_ids=inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=10,
            num_beams=2,
            early_stopping=True
        )

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True).lower().strip()
        return 'high' if 'high' in decoded else 'low'

    def process_file(self, input_file, output_file):
        buffer = self.load_context_buffer(input_file)
        window_size = 3
        for i in range(len(buffer)):
            current = buffer[i]


            if float(current['confidence']) > 0.9:
                current['validated_label'] = current['label'].replace("__label__", "")
                current['validation_method'] = "fasttext_high_confidence"
                continue

            context_window = buffer[max(0, i-window_size+1):i+1]


            if self.analyze_context(context_window):
                current['validated_label'] = 'high'
                current['validation_method'] = "t5"
                continue

            validated_label = self.validate_with_context(context_window)
            current['validated_label'] = validated_label
            current['validation_method'] = "t5_validation"

            fasttext_label = current['label'].replace("__label__", "")
            if validated_label != fasttext_label:
                current['discrepancy'] = f"FastText:{fasttext_label} vs T5:{validated_label}"

        pd.DataFrame(buffer).to_csv(output_file, index=False)
        return buffer
validator = ContextualValidator()
results = validator.process_file(
    input_file="context_buffer_log.csv",
    output_file="validated_context_buffer.csv"
)
for i, item in enumerate(results[:5]):
    print(f"\nMessage {i+1}: {item['query']}")
    print(f"FastText: {item['label']} (confidence: {item['confidence']})")
    print(f"Validated: {item['validated_label']} via {item['validation_method']}")
    if 'discrepancy' in item:
        print(f"Discrepancy: {item['discrepancy']}")