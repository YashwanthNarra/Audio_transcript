audio-to-text/
│
├── app/
│   ├── main.py
│   │
│   ├── services/
│   │   ├── sarvam.py
│   │   └── gemini.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   └── utils/
│       └── file_handler.py
│
├── frontend/
│
├── .env
├── requirements.txt
└── README.md


| Package            | Purpose                      |
| ------------------ | ---------------------------- |
| `fastapi`          | Backend API                  |
| `uvicorn`          | Run the FastAPI server       |
| `python-multipart` | Receive uploaded audio files |
| `python-dotenv`    | Read API keys from `.env`    |
| `sarvamai`         | Sarvam AI Python SDK         |
| `google-genai`     | Gemini API Python SDK        |



### important things to consider
1. We have to ensure the gemini doesnt change the meaning


# Bad file       → 400
# Sarvam fails   → 502
# Gemini fails   → 502
# Success        → 200



# telugu test-1
Sarvam time :  2.261461019515991 sec
Gemini time :  7.69333291053772