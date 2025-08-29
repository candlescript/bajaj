from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

# ---------- CONFIG ----------
FULL_NAME = "john_doe"
DOB = "17091999"
EMAIL = "john@xyz.com"
ROLL_NUMBER = "ABCD123"

USER_ID = f"{FULL_NAME.lower()}_{DOB}"


# ---------- Request Schema ----------
class DataInput(BaseModel):
    data: List[str]


# ---------- Helper Function ----------
def process_data(data_list):
    odd_numbers = []
    even_numbers = []
    alphabets = []
    special_characters = []
    total_sum = 0

    for item in data_list:
        if re.fullmatch(r"\d+", item):  # numbers only
            num = int(item)
            if num % 2 == 0:
                even_numbers.append(item)
            else:
                odd_numbers.append(item)
            total_sum += num
        elif re.fullmatch(r"[A-Za-z]+", item):  # alphabets only
            alphabets.append(item.upper())
        else:
            special_characters.append(item)

    # Build concat string in reverse order with alternating caps
    all_letters = "".join("".join(re.findall("[A-Za-z]", i)) for i in data_list)
    rev = all_letters[::-1]
    concat_string = "".join(
        c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(rev)
    )

    return {
        "is_success": True,
        "user_id": USER_ID,
        "email": EMAIL,
        "roll_number": ROLL_NUMBER,
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets,
        "special_characters": special_characters,
        "sum": str(total_sum),
        "concat_string": concat_string,
    }


# ---------- POST Endpoint ----------
@app.post("/bfhl")
async def bfhl(input_data: DataInput):
    try:
        result = process_data(input_data.data)
        return result
    except Exception as e:
        return {"is_success": False, "error": str(e)}
