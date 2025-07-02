from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("SecretNumber")

class CiscoInput(BaseModel):
    series: str

@mcp.tool()
def CiscoRouterCatalog(input: CiscoInput) -> str:
  
    if input.series == "cisco8100":
        return "Good for small size businesses"

    elif input.series == "cisco8200":
        return "Good for medium size businesses"

    else:
        return "nothing available right now"

if __name__ == "__main__":
    mcp.run(transport='stdio')
