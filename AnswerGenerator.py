from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

# Set your OpenAI API key here
#openai.api_key = "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"

def read_api_key():
    with open("api_key.txt", "r") as file:
        return file.read().strip()

# Set your OpenAI API key here
openai.api_key = read_api_key()

class Question(BaseModel):
    question: str

@app.get("/health")
async def health():
    return '200 OK'

@app.post("/ask")
async def ask_question(question: Question):
    # Use the OpenAI GPT API to get a response
    response = openai.Completion.create(
        engine="davinci-codex",  # You can choose a different engine based on your requirements
        prompt=question.question,
        max_tokens=50  # Adjust as needed
    )
    print("Response from the openAI : "+ response)

    # Extract the generated text from the OpenAI response
    answer = response.choices[0].text.strip()
    print("Printing the answer: "+answer)

    # Return the answer in a JSON response
    return {"question": question.question, "answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
