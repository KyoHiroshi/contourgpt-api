# Natural Language Car Explorer API

**ContourGPT** is a backend API designed to interpret natural language queries and translate them into structured logic for dataset exploration. Initially built for segmentation tasks, this project is now being refactored and repurposed to help users find cars through simple, conversational input — no filters, dropdowns, or complex searches needed.

---

## Core Idea

Turn this:

> “Show me hybrid cars under £15,000 with less than 50,000 miles”

Into a structured query that the backend uses to fetch relevant results from a car database.

---

## Planned Features

- 🔍 **Natural Language Understanding**: Use GPT models to convert user queries into structured filters.
- 🚘 **Car Dataset Integration**: Replace original segmentation logic with car-related rule parameters (e.g., `make`, `model`, `price`, `mileage`, `fuelType`, etc.).
- ⚛️ **React UI** (planned): Simple interface to let users type what they’re looking for and see cars immediately.
- 🐘 **SQL Database**: Store and query a structured car dataset using PostgreSQL or SQLite.
- 🐳 **Docker**: Containerised for ease of development, testing, and deployment.
- ☁️ **Cloud Deployment** (eventual): Host via AWS using EC2, RDS, and S3.

---

## Tech Stack

| Layer         | Stack                        |
| ------------- | ---------------------------- |
| **Frontend**  | React (TypeScript - planned) |
| **Backend**   | Flask + OpenAI GPT           |
| **Database**  | PostgreSQL / SQLite          |
| **Container** | Docker                       |
| **Hosting**   | AWS (planned)                |

---

## 📁 Project Structure

```
ContourGPT/
├── app.py                  # Main Flask app
├── contourgpt_v2.py        # GPT-based NLP logic
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker config for backend
└── README.md               # You’re reading this
```

---

## 🧪 Running Locally

### 1. Clone & install dependencies

```bash
git clone https://github.com/yourusername/ContourGPT.git
cd ContourGPT
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set your OpenAI API key

You can either set the key in your environment:

```bash
export OPENAI_API_KEY=your-key-here
```

Or modify `contourgpt_v2.py` to securely read from a `.env` file (recommended).

### 3. Start the Flask server

```bash
python app.py
```

Server runs at: `http://localhost:8050`

---

## API Overview

### `POST /generateSegment`

> Repurposed soon as `POST /generateQuery` or similar for the car dataset.

**Description:** Extracts structured parameters from a user query.

**Request Body:**

```json
{
  "user_prompt": "I want a hybrid car with under 50000 miles and costs less than 15000"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Query parsed successfully.",
  "segmentID": "abc123" // to be renamed or restructured in car context
}
```

---

## 🛠️ To-Do (Refactor Plan)

### ✅ Existing

- &#x20;Flask + CORS
- &#x20;OpenAI GPT integration
- &#x20;JSON schema validation
- &#x20;Oracle DB interactions (legacy)

### 🔄 In Progress

- &#x20;Replace segmentation logic with car attributes
- &#x20;Replace Oracle with PostgreSQL/SQLite
- &#x20;Update endpoint naming to suit cars (e.g., /generateQuery)
- &#x20;Add a /searchCars route that uses structured queries to fetch results

### 🚀 Planned

- &#x20;Docker Compose (API + DB + frontend)
- &#x20;React frontend interface
- &#x20;AWS hosting (EC2 + RDS + S3)

---

## 🧹 Notes for Refactor

- **`enforce_json_structure()`** in `contourgpt_v2.py` is key to  NLP pipeline.
- Original function interprets queries into:
  ```json
  {
    "segmentName": "...",
    "ruleParam": "Age",
    "ruleOperator": ">=",
    "ruleValue": 50
  }
  ```
  Replace `segmentName`, `ruleParam`, etc., with car-related terms like:
  - `carType`
  - `price`
  - `mileage`
  - `fuelType`
  - `transmission`
  - etc.

---

## 🙌 Credits

Built originally as part of a university final-year project focused on marketing segmentation. Renewed and reimagined to serve a broader and more engaging use case.