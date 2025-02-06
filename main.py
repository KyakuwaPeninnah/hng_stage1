from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def is_perfect(n):
    return sum(i for i in range(1, n) if n % i == 0) == n

def get_fun_fact(n):
    url = f"http://numbersapi.com/{n}/math?json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json().get("text", "No fun fact available.")
    except requests.exceptions.RequestException:
        return "No fun fact available."

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="An integer number")):
    properties = ["odd" if number % 2 else "even"]
    if is_armstrong(number):
        properties.insert(0, "armstrong")

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(number)),
        "fun_fact": get_fun_fact(number)
    }
