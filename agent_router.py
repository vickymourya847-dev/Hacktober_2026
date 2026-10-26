
import re


APP_ALIASES = {
    "chrome": "chrome",
    "google chrome": "chrome",
    "vs code": "vscode",
    "vscode": "vscode",
    "visual studio code": "vscode",
    "notepad": "notepad",
    "calculator": "calculator",
}


def route_message(message: str):
    text = message.strip()
    lower = text.lower()

    # Only explicit, standalone launch commands.
    match = re.fullmatch(
        r"(?:please\s+)?(?:open|launch|start)\s+"
        r"([a-z0-9 ]+?)[.!]?",
        lower
    )

    if match:
        target = match.group(1).strip()

        if target in APP_ALIASES:
            return {
                "intent": "open_app",
                "application": APP_ALIASES[target],
                "requires_confirmation": True
            }

    # Explicit web search requests.
    search_match = re.match(
        r"^(?:please\s+)?(?:search(?:\s+the\s+web)?"
        r"(?:\s+for)?|look\s+up|find\s+online)\s+(.+)$",
        text,
        flags=re.IGNORECASE
    )

    if search_match:
        return {
            "intent": "research",
            "query": search_match.group(1).strip()
        }

    # Explicit reasoning mode.
    if lower.startswith("reason:"):
        return {
            "intent": "reasoning",
            "message": text[7:].strip()
        }

    # Coding requests.
    coding_patterns = (
        "code:",
        "write python",
        "write code",
        "debug",
        "fix this code",
        "help me fix",
        "review my code",
    )

    if lower.startswith(coding_patterns):
        return {
            "intent": "coding",
            "message": text
        }

    return {
        "intent": "chat",
        "message": text
    }
