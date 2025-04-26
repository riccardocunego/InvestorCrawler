from typing import List
from agents import Agent, Runner, WebSearchTool
from pydantic import BaseModel, Field

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set the OpenAI API key for the Agent
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Define your data structure
class PortfolioCompany(BaseModel):
    company_name: str = Field(..., description="Name of the portfolio company.")
    company_website: str = Field(..., description="Official website URL of the portfolio company.")
    holding_status: str = Field(..., description="Status of the investment, e.g., 'Current', 'Exited', or similar.")
    transaction_date: str = Field(..., description="Date of the investment or transaction, format: YYYY-MM-DD if available, otherwise best available format.")

class Investor(BaseModel):
    investor_name: str = Field(..., description="Full name of the investment firm or investor.")
    investor_description: str = Field(..., description="Brief description of the investor, their focus areas, or investment philosophy.")
    investor_website: str = Field(..., description="Official website URL of the investor.")
    portfolio_companies: List[PortfolioCompany] = Field(..., description="List of companies the investor has invested in.")
    target_industry: List[str] = Field(..., description="List of industries or sectors the investor targets, e.g., 'Healthcare', 'Technology', etc.")
    ticket_size: str = Field(..., description="Typical investment size range, e.g., '$5M-$50M'.")
    target_EV: str = Field(..., description="Target Enterprise Value (EV) range for investments, e.g., '$20M-$200M'.")


# Setup your agent
investor_crawler_agent = Agent(
    name="Investor Crawler Agent",
    instructions=("""
        "You are a data extraction assistant specialized in extracting structured information about investors and their portfolio companies.\n\n"
        "TASK:\n"
        "Given an investor's website (especially the portfolio page), extract the following structured information:\n\n"
        "1. Investor Name: The full name of the investor or investment firm.\n"
        "2. Investor Website: The official website URL.\n"
        "3. Investor Description: A short summary describing the investor, their investment focus, or philosophy.\n"
        "4. Portfolio Companies:\n"
        "   - Company Name: Name of each portfolio company.\n"
        "   - Company Website: URL of each portfolio company.\n"
        "   - Holding Status: Whether the investment is 'Current', 'Exited', or another status.\n"
        "   - Transaction Date: Date when the investment was made or exited (if available).\n"
        "5. Target Industry: List of industries/sectors the investor typically invests in.\n"
        "6. Ticket Size: Typical investment size range.\n"
        "7. Target EV: Typical Enterprise Value (EV) range for investments.\n\n"
        "FORMATTING:\n"
        "- Ensure the extracted output fits the 'Investor' Pydantic model exactly.\n"
        "- If certain fields are missing or unavailable, leave them empty or set them to an empty list (for lists) or empty string (for text fields).\n"
        "- Be as accurate and complete as possible, even if you need to infer from context.\n\n"
        "IMPORTANT:\n"
        "- Focus especially on the Portfolio section.\n"
        "- Use structured data only, no free text paragraphs."
        """
    ),
    tools=[WebSearchTool()],
    output_type=Investor,
)

# List of investor websites you want to crawl
investor_websites = [
    "https://www.emeram.com/",
    "https://www.xenonpe.com/",
    "https://main.nl/",
    "https://afinum.de/"
]

async def main():
    results = []
    for website_url in investor_websites:
        task_prompt = (
            f"Please review the portfolio page {website_url} and return the investor name, "
            "investor website, and portfolio companies' details."
        )
        
        # Run the agent
        result = await Runner.run(investor_crawler_agent, input=task_prompt)
        results.append(result.final_output)

    # Print all results
    for investor_data in results:
        print(investor_data)

# To actually run the async main
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())