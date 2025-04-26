from typing import List
from agents import Agent, Runner, WebSearchTool
from pydantic import BaseModel

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set the OpenAI API key for the Agent
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Define your data structure
class PortfolioCompany(BaseModel):
    company_name: str
    company_website: str
    holding_status: str  # e.g., "Current", "Exited", etc.
    transaction_date: str

class Investor(BaseModel):
    investor_name: str
    investor_website: str
    portfolio_companies: List[PortfolioCompany]

# Setup your agent
investor_crawler_agent = Agent(
    name="Investor Crawler Agent",
    instructions=(
        "Review the given investor website and extract the list of portfolio companies, "
        "including their names, websites, holding status (current, exited, etc.), and transaction date."
    ),
    tools=[WebSearchTool()],
    output_type=Investor,
)

# List of investor websites you want to crawl
investor_websites = [
    "https://www.emeram.com/en/portfolio",
    # Add more investor portfolio URLs here
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