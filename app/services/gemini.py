import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def clean_transcription(text: str) -> str:

    prompt = f"""
    You are a billing extraction system.

    Below is a conversation between a shopkeeper and customers.

    Your job is to extract the FINAL PURCHASED ITEMS and create a bill.

    STRICT RULES:

    1. Include ONLY items that were finally purchased.
    2. Ignore items that were:
    - only discussed
    - rejected
    - unavailable
    - returned
    - exchanged
    3. If an item was returned, DO NOT include it in the final bill.
    4. If the same item appears multiple times, combine it into ONE item.
    5. Preserve the EXACT quantity mentioned in the conversation.
    6. NEVER assume quantity = 1 when a quantity, weight, volume, or number is explicitly mentioned.
    7. Preserve units such as:
    - kg
    - grams
    - liters
    - ml
    - pieces
    - sets
    8. If an item has no explicit quantity, use "1".
    9. Use the most specific product name available.
    Example: "cold-pressed oil" instead of just "oil".
    10. Do NOT include prices.
    11. Do NOT include speaker names.
    12. Do NOT explain your reasoning.
    13. Do NOT add any item that was not purchased.
    14. Return ONLY the final bill.

    ================================
                FINAL BILL
    ================================

    Item                  Quantity    
    -----------------------------------------
    <item>                <qty> 
    <item>                <qty> 
    <item>                <qty> 
    -----------------------------------------
                                
    ================================

    Conversation:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text