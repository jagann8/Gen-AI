from transformers import pipeline

class SummarizerModel:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.summarizer = pipeline("summarization", model=model_name)

    def generate_summary(self, text: str) -> str:
        return self.summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
