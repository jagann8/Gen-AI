from app.models.summarizer import SummarizerModel

class SummarizerService:
    def __init__(self):
        self.model = SummarizerModel()

    def summarize(self, text: str) -> str:
        return self.model.generate_summary(text)
