from fastapi import FastAPI
from app.schemas.request_response import TextRequest, SummaryResponse
from app.services.summarization import SummarizerService

app = FastAPI()
summarizer = SummarizerService()

@app.post("/summarize", response_model=SummaryResponse)
def summarize_text(request: TextRequest):
    summary = summarizer.summarize(request.text)
    return SummaryResponse(summary=summary)


### END of the program execution
