from typing import List
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP
import requests
import os

mcp = FastMCP("server", host="0.0.0.0", port=8000)

class FormResponse(BaseModel):
    email: str = Field(description="Email")
    name: str = Field(description="Name")
    jobTitle: str = Field(description="Job Title")
    company: str = Field(description="Company")
    city: str = Field(description="City")

@mcp.tool()
def get_responses() -> List[FormResponse]:
    """
    Returns a list of Typeform form responses (no inputs)
    """
    try:
        token = os.getenv("TYPEFORM_TOKEN") 
        url = "https://api.typeform.com/forms/QrN5llgU/responses"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        print("Calling Typeform API")        
        response = requests.get(url, headers=headers)

        print("Returned from Typeform API")
        data = response.json()
        formResponses: List[FormResponse] = []
        items = data["items"]
        for item in items:
            answers = item["answers"]
            formResponses.append(FormResponse(
                email=answers[0]["email"],
                name=answers[1]["text"],
                jobTitle=answers[2]["text"],
                company=answers[3]["text"],
                city=answers[4]["text"]
            ))

        print("Stored into list:")
        for r in formResponses:
            print(r)
        
        print("Sending back to MCP client")        
        return formResponses
        
    except Exception as e:
        return f"Error getting form responses: {e}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")