from datetime import datetime

from langchain.tools import tool


@tool
def get_current_datetime() -> str:
    """Retorna a hora atual."""
    return datetime.now().strftime("%H:%M")


@tool
def get_current_date() -> str:
    """Retorna a data atual."""
    return datetime.now().strftime("%d/%m/%Y")