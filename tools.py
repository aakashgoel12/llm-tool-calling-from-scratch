"""
tools.py - Real tools that an LLM can call

Simple but realistic tools for demonstration:
- Calculator: perform math operations
- Database: query user data
- Weather: simulate weather lookup
- Time: get current time
"""

import json
import math
from datetime import datetime


# ==================== TOOL 1: Calculator ====================
def calculator(operation: str, a: float, b: float) -> dict:
    """
    Perform basic math operations.
    
    Args:
        operation: "add", "subtract", "multiply", "divide", "power"
        a: first number
        b: second number
    
    Returns: dict with result or error
    """
    try:
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return {"error": "Division by zero"}
            result = a / b
        elif operation == "power":
            result = a ** b
        else:
            return {"error": f"Unknown operation: {operation}"}
        
        return {"operation": operation, "a": a, "b": b, "result": result}
    except Exception as e:
        return {"error": str(e)}


# ==================== TOOL 2: Database ====================
# Fake user database
USER_DATABASE = {
    "user_001": {"name": "Alice Johnson", "email": "alice@example.com", "balance": 5420.50},
    "user_002": {"name": "Bob Smith", "email": "bob@example.com", "balance": 3210.00},
    "user_003": {"name": "Charlie Brown", "email": "charlie@example.com", "balance": 8765.25},
}

def database_query(user_id: str) -> dict:
    """
    Look up user information in database.
    
    Args:
        user_id: User identifier (e.g., "user_001")
    
    Returns: User data or not found error
    """
    if user_id in USER_DATABASE:
        return {
            "found": True,
            "user_id": user_id,
            **USER_DATABASE[user_id]
        }
    else:
        return {
            "found": False,
            "error": f"User {user_id} not found. Available: {list(USER_DATABASE.keys())}"
        }


# ==================== TOOL 3: Weather ====================
WEATHER_DATA = {
    "new york": {"temp": 72, "condition": "Sunny", "humidity": 45},
    "san francisco": {"temp": 65, "condition": "Cloudy", "humidity": 70},
    "london": {"temp": 59, "condition": "Rainy", "humidity": 85},
    "tokyo": {"temp": 81, "condition": "Humid", "humidity": 75},
}

def weather_lookup(city: str) -> dict:
    """
    Get weather information for a city.
    
    Args:
        city: City name (lowercase)
    
    Returns: Weather data or not found error
    """
    city_lower = city.lower()
    if city_lower in WEATHER_DATA:
        return {
            "found": True,
            "city": city,
            **WEATHER_DATA[city_lower],
            "unit": "Fahrenheit"
        }
    else:
        return {
            "found": False,
            "error": f"Weather data not available for {city}. Available: {list(WEATHER_DATA.keys())}"
        }


# ==================== TOOL 4: Time ====================
def get_current_time() -> dict:
    """
    Get current date and time.
    
    Returns: Current datetime info
    """
    now = datetime.now()
    return {
        "timestamp": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A")
    }


# ==================== Tool Registry ====================
TOOLS = {
    "calculator": {
        "name": "calculator",
        "description": "Perform mathematical operations (add, subtract, multiply, divide, power)",
        "required_params": ["operation", "a", "b"],
        "func": calculator
    },
    "database_query": {
        "name": "database_query",
        "description": "Look up user information by user_id",
        "required_params": ["user_id"],
        "func": database_query
    },
    "weather_lookup": {
        "name": "weather_lookup",
        "description": "Get weather information for a city",
        "required_params": ["city"],
        "func": weather_lookup
    },
    "get_current_time": {
        "name": "get_current_time",
        "description": "Get current date and time",
        "required_params": [],
        "func": get_current_time
    }
}


def execute_tool(tool_name: str, **kwargs) -> dict:
    """
    Execute a tool by name with given parameters.
    
    Args:
        tool_name: Name of the tool to execute
        **kwargs: Parameters for the tool
    
    Returns: Tool result
    """
    if tool_name not in TOOLS:
        return {"error": f"Unknown tool: {tool_name}. Available: {list(TOOLS.keys())}"}
    
    tool = TOOLS[tool_name]
    try:
        return tool["func"](**kwargs)
    except TypeError as e:
        return {"error": f"Missing required parameters. Expected: {tool['required_params']}"}


if __name__ == "__main__":
    # Test the tools
    print("=== Testing Tools ===\n")
    
    print("1. Calculator: 25 + 17 =", calculator("add", 25, 17))
    print("\n2. Database: User lookup")
    print(database_query("user_001"))
    print("\n3. Weather: London forecast")
    print(weather_lookup("london"))
    print("\n4. Time: Current time")
    print(get_current_time())
