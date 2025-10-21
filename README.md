##  hng1


A simple FastAPI application that analyzes strings, stores their properties, and supports filtering (including natural-language based filters).
Built with FastAPI.

## Setup

```bash
git clone https://github.com/Obi-ah/hng0.git
cd hng0
python -m venv venv
source venv/bin/activate    
pip install requirements.txt
```

]
## Run Locally
```
uvicorn app.main:app --reload
```

## Endpoints
| Method | Endpoint | Description |
|:--|:--|:--|
| **POST** | `/strings` | Analyze and store a string |
| **GET** | `/strings/{value}` | Retrieve analyzed string |
| **GET** | `/strings` | Filter strings via query parameters |
| **GET** | `/strings/filter-by-natural-language` | Filter using natural text (e.g. “all single word palindromic strings”) |
| **DELETE** | `/strings/{value}` | Delete a stored string |