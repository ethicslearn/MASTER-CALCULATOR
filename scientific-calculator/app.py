from flask import Flask, render_template, request, jsonify
import ast
import math

app = Flask(__name__)


# --- Safe expression evaluation ------------------------------------------------


_ALLOWED_NAMES = {
    # constants
    "pi": math.pi,
    "e": math.e,
    # functions
    "sin": math.sin,   # radians
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,  # log base 10
    "ln": math.log,     # natural log
    "sqrt": math.sqrt,
    "abs": abs,
}


_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.Num,  # for older Python versions
)


_ALLOWED_BIN_OPS = (
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.Mod,
)


_ALLOWED_UNARY_OPS = (
    ast.UAdd,
    ast.USub,
)


def _validate_node(node: ast.AST) -> None:
    """Recursively validate that the AST node only contains safe constructs."""
    if not isinstance(node, _ALLOWED_NODES):
        raise ValueError("Unsupported expression")

    if isinstance(node, ast.BinOp):
        if not isinstance(node.op, _ALLOWED_BIN_OPS):
            raise ValueError("Unsupported operator")
        _validate_node(node.left)
        _validate_node(node.right)

    elif isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, _ALLOWED_UNARY_OPS):
            raise ValueError("Unsupported unary operator")
        _validate_node(node.operand)

    elif isinstance(node, ast.Call):
        # Only allow simple name calls, e.g. sin(x), log(10)
        if not isinstance(node.func, ast.Name):
            raise ValueError("Unsupported function call")
        if node.func.id not in _ALLOWED_NAMES:
            raise ValueError(f"Unsupported function: {node.func.id}")
        for arg in node.args:
            _validate_node(arg)
        # No kwargs
        if node.keywords:
            raise ValueError("Keyword arguments are not allowed")

    elif isinstance(node, ast.Name):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Unknown identifier: {node.id}")

    elif isinstance(node, (ast.Constant, ast.Num)):
        # Only allow int / float
        value = getattr(node, "n", getattr(node, "value", None))
        if not isinstance(value, (int, float)):
            raise ValueError("Only numeric literals are allowed")


def safe_eval(expr: str) -> float:
    """
    Safely evaluate a mathematical expression string using a restricted AST.

    Supported:
    - Numbers, +, -, *, /, %, **, parentheses
    - Functions: sin, cos, tan, log (base 10), ln, sqrt, abs
    - Constants: pi, e
    """
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse into AST
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid syntax") from exc

    # Validate AST recursively
    _validate_node(tree.body)

    # Evaluate with restricted globals / locals
    compiled = compile(tree, "<expression>", "eval")
    return eval(compiled, {"__builtins__": {}}, _ALLOWED_NAMES)


# --- Routes --------------------------------------------------------------------


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True) or {}
    expr = data.get("expression", "")

    try:
        result = safe_eval(expr)
    except Exception as exc:
        # Hide internal details, return generic error
        return jsonify({"error": "Invalid expression"}), 400

    # Use repr-like formatting but trim trailing .0
    if isinstance(result, float):
        if result.is_integer():
            result_str = str(int(result))
        else:
            # limit precision a bit
            result_str = f"{result:.10g}"
    else:
        result_str = str(result)

    return jsonify({"result": result_str})


if __name__ == "__main__":
    # For local development only
    app.run(debug=True)