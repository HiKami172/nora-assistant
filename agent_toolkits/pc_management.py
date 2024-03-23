import subprocess
from langchain.agents import tool

@tool
def get_installed_programs() -> str:
    """Retrieves a list of the installed programs."""
    data = subprocess.check_output(['wmic', 'product', 'get', 'name'])
    a = str(data)
    return a