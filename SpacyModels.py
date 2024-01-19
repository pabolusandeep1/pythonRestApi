from typing import List
from fastapi import FastAPI, HTTPException

import uvicorn
import spacy
#import en_core_web_sm

nlp = spacy.load("en_core_web_sm")

app=FastAPI()

@app.get("/health")
async def health_check():
    return "200 - OK"

@app.get("/extractPhrase/{text}")
async def read_text(text) -> []:
    return extract_text(text)

@app.post("/extractPhrase")
async def read_text(payload: dict):
    text = payload.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="text is not provided in the request body")
    return await extract_text(text)


async def extract_text(text):
    spacy_doc = nlp(text)
    keywords = []
    #For extractinf key phrases
    for chunk in spacy_doc.noun_chunks:
        if chunk.text.lower() not in nlp.Defaults.stop_words:
            keywords.append(chunk.text)

    print(keywords)        
    return keywords

if __name__ == "__main__":
    uvicorn.run(app, host="localhost",port=8080)