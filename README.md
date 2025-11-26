# Master Calculator

A modern web-based scientific calculator built with **Flask**, **HTML**, **CSS**, and **vanilla JavaScript**. 

It supports two modes:

- **Ordinary** – basic calculator layout (c, %, backspace, +, −, ×, ÷, digits, 00, decimal, =)
- **Science** – extended layout with trigonometric, logarithmic, root, power and constant functions

The UI mimics a mobile/desktop-style calculator with a dark display, circular buttons, and an orange accent theme.

---

## Features

### Ordinary Mode
- Clear (`c`)
- Percentage (`%`)
- Backspace (◀)
- Basic operators: addition (+), subtraction (−), multiplication (×), division (÷)
- Number keys: `0–9` plus `00`
- Decimal point (`.`)
- Equals (`=`) to evaluate the current expression

### Science Mode
- All basic arithmetic operators
- **Trigonometric functions**: `sin`, `cos`, `tan`
- **Logarithmic functions**: `log` (base 10), `ln` (natural log)
- **Root / power**:
  - `√` (square root)
  - `x²` (implemented by appending `**2` to the current expression)
- **Constants**:
  - `π` (pi)
  - `e` (Euler's number)
- Parentheses: `(` and `)`
- Digits arranged with operators on the right side, similar to a typical scientific calculator layout

### General Behavior
- Top display shows the **current expression** and **result**.
- Clicking buttons builds an expression string in JavaScript.
- When you press `=`, the app sends the expression to the backend (`/calculate` endpoint) via **POST JSON**.
- The Flask backend safely evaluates the expression (using Python math functions) and returns a JSON result.
- Errors (invalid expressions, math errors) are shown in the result display.

> Note: The exact backend implementation lives in your main Flask file (e.g. `app.py`) and exposes at least two routes: `/` for the UI and `/calculate` for evaluation.

---

## Project Structure

Typical layout of this project:

```text path=null start=null
scientific-calculator/
├─ app.py                 # Flask application (entry point, name may vary)
├─ requirements.txt       # Python dependencies
├─ README.md              # This file
├─ templates/
│  └─ index.html          # Calculator UI (HTML + JS logic)
└─ static/
   └─ styles.css          # Calculator styling
```

- `templates/index.html` contains:
  - Display markup
  - The **Ordinary** and **Science** button grids
  - JavaScript handling button clicks and calling `/calculate`
- `static/styles.css` defines the dark theme, circular buttons, orange accents, and ordinary/science mode styling.

---

## Requirements

- Python 3.9+ (recommended)
- pip (Python package manager)

Python dependencies are listed in `requirements.txt`:
command:- ` pip install -r requirements.txt  `

```text path=null start=null
Flask>=3.0.0
gunicorn>=21.2.0
```

(`gunicorn` is mainly for deployment on Linux-based hosts; on Windows you typically run with `flask` or `python app.py` during development.)

---

## Installation & Local Setup

1. **Clone or download the project**

   ```bash path=null start=null
   git clone https://github.com/<your-username>/scientific-calculator.git
   cd scientific-calculator
   ```

2. **Create and activate a virtual environment (recommended)**

   On Windows (PowerShell):

   ```powershell path=null start=null
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   On macOS/Linux:

   ```bash path=null start=null
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash path=null start=null
   pip install -r requirements.txt
   ```

4. **Run the Flask app (development)**

   If your entry file is `app.py` and defines `app = Flask(__name__)`:

   ```bash path=null start=null
   # Option A: use Flask CLI
   set FLASK_APP=app.py        # Windows (cmd)
   # or in PowerShell: $env:FLASK_APP = "app.py"
   flask run

   # Option B: run directly with Python
   python app.py
   ```

5. **Open in the browser**

   By default, the app runs at:

   - http://127.0.0.1:5000/ or
   - http://localhost:5000/

   You should see the calculator UI with **Ordinary** and **Science** mode toggle at the top.

---

## How It Works (Step by Step)

1. **User interface**
   - The browser loads `index.html` via the root route (`/`).
   - Buttons have data attributes like `data-value` (for numbers/operators) and `data-action` (for `clear`, `delete`, `equals`, `square`).

2. **Building expressions on the client**
   - JavaScript listens for `.btn` clicks.
   - For normal keys, it appends the `data-value` to `currentExpression` and updates the expression display.
   - `AC` clears everything, `DEL` deletes the last character.
   - `x²` appends `**2` so the backend can interpret it as a power operation.

3. **Evaluating expressions on the backend**
   - When `=` is pressed, JS sends a `POST` request to `/calculate` with JSON:
     ```json path=null start=null
     { "expression": "<user_expression_here>" }
     ```
   - The Flask route parses the expression string, maps functions (`sin`, `cos`, `tan`, `log`, `ln`, `sqrt`, `pi`, `e`, etc.) to Python's `math` module, evaluates the expression, and returns:
     ```json path=null start=null
     { "result": <number> }
     ```
     or, on error:
     ```json path=null start=null
     { "error": "message" }
     ```
   - The frontend shows the result or error in the display.

4. **Mode switching (Ordinary / Science)**
   - Two pill buttons at the top toggle between modes.
   - JavaScript toggles CSS classes `mode-ordinary` and `mode-science` on the `<body>` element.
   - CSS shows only the relevant keypad grid:
     - `buttons-grid-ordinary` for ordinary mode
     - `buttons-grid-science` for science mode
   - Only the layout changes; the calculation logic stays the same.

---

## Customization

- **Styling**: adjust colors, spacing, and button sizes in `static/styles.css`.
- **Functions**: add new scientific functions by:
  1. Adding a button with appropriate `data-value` in `templates/index.html`.
  2. Extending the backend evaluation logic to understand that function.
- **Layouts**: modify the ordinary/science grids to match different calculator layouts.

---

## License

Apache 2.0

## Program Devloper:- 
--> Developer name:- Shreyansh Jaiswal
--> Developement company:-  CODE DRAGON 
  <!-- Powered by ETHICS LEARN --> 
