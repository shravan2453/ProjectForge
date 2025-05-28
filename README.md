# IdeaGenerationChatBot

**Contributors:** Shravan Selvavel, Natnael Worku

This is a chatbot utilizing Google Gemini API to help students and businesses with idea generation, with the primary intention being full website integration


# Project Setup

## Installation
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`

## .gitignore
In Bash run:
echo -e "venv/\n__pycache__/\n.env\n*.pyc" >> .gitignore

In PowerShell run:
"venv/", "__pycache__/", ".env", "*.pyc" | Out-File -FilePath .gitignore -Append -Encoding UTF8
