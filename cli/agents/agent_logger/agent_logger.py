import asyncio
from datetime import datetime

from genai_session.session import GenAISession

session = GenAISession(
    jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmMWE2ODljNy00YWFiLTRjYjgtOTFiZC01M2MyMmExOGFjYjQiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjZlNzM3YWQ1LWFiNTctNGYzYi1iMjU2LTUyNDE4ZTRlY2FlNCJ9.J7plQ7PboxO2GSYjYqDn2PBPuacTbB5MUPvnHpCvM-E"
)

async def main():
    await session.process_events()


if __name__ == "__main__":
    asyncio.run(main())


import sys
import os
import asyncio
from typing import Annotated

# Add the src directory to Python path (based on your project structure)
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

print(f"Current directory: {current_dir}")
print(f"Adding to Python path: {src_dir}")
print(f"Src directory exists: {os.path.exists(src_dir)}")

# Import the genai_session modules

import asyncio
from genai_session.session import GenAISession

session = GenAISession(
    jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmMWE2ODljNy00YWFiLTRjYjgtOTFiZC01M2MyMmExOGFjYjQiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjZlNzM3YWQ1LWFiNTctNGYzYi1iMjU2LTUyNDE4ZTRlY2FlNCJ9.J7plQ7PboxO2GSYjYqDn2PBPuacTbB5MUPvnHpCvM-E"
)

try:
    from genai_session.session import GenAISession
    from genai_session.utils.context import GenAIContext
    print("✅ Successfully imported genai_session modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    
    if os.path.exists(src_dir):
        print(f"Contents of src directory: {os.listdir(src_dir)}")
        genai_session_path = os.path.join(src_dir, 'genai_session')
        if os.path.exists(genai_session_path):
            print(f"GenAI session directory exists: {genai_session_path}")
            print(f"Contents: {os.listdir(genai_session_path)}")
        else:
            print("❌ genai_session directory not found in src")
    
    sys.exit(1)

# Load environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AGENT_JWT = os.getenv('AGENT_JWT')

if not OPENAI_API_KEY:
    print("⚠️  OPENAI_API_KEY not found in environment variables")
if not AGENT_JWT:
    print("⚠️  AGENT_JWT not found in environment variables")

if not OPENAI_API_KEY or not AGENT_JWT:
    print("\n❌ Missing required credentials. Please either:")
    print("1. Set environment variables:")
    print("   $env:OPENAI_API_KEY=\"your-api-key\"")
    print("   $env:AGENT_JWT=\"your-jwt-token\"")
    sys.exit(1)

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Initialize the GenAI session
try:
    session = GenAISession(
        jwt_token=AGENT_JWT,
        model="gpt-4",
        provider="openai"
    )
    print("✅ GenAI session initialized successfully")
except Exception as e:
    print(f"❌ Error initializing GenAI session: {e}")
    sys.exit(1)


@session.bind(
    name="ai_forex_day_trader_coach",
    description="Structured Forex Trade Planner and Logger",
    model="gpt-4",
    provider="openai"
)
async def ai_forex_day_trader_coach(
    agent_context: GenAIContext,
    trade_data: Annotated[
        str,
        "User-submitted forex trade plan, question, or trade journal entry data."
    ],
):
    """
    Structured AI Forex Assistant for trade planning, journaling, and risk management.
    """

    structured_prompt = f"""
## 🎯 Purpose:
You are a disciplined and structured forex trading assistant. Your role is to help the user plan, log, and review forex trades with precision and consistency. You enforce risk management, document trading psychology, and maintain a clear journal format. You also provide insights into trade setups based on user-defined strategies and chart information.

## 🧩 Personality:
- Tone: Calm, focused, and objective
- Style: Structured, checklist-driven, and non-emotional
- Behavior: Data-aware, disciplined, trader-minded

## 🛠️ Functional Capabilities:
- Structure and log trades in a standardized journal format
- Calculate risk per trade, lot size, pip value, and R-multiple
- Reflect on trading psychology and adherence to strategy
- Retrieve and update journal entries if integrated with Google Sheets
- Recommend best practices for entry types, SL/TP levels, and trade types
- Use trading terms like "pullback at value," "engulfing trigger," and "risk-reward"

## 🧾 Output Format:
Respond with a fully formatted trade log or planning checklist along with downloadable google sheet version using this structure:
• 📅 Trade Date: {{date}}
• 📊 Pair: {{currency_pair}}
• ⏰ Timeframe: {{timeframe}}
• 📈 Trade Type: {{setup_type}}
• 🎯 Bias: {{bullish_or_bearish}}
• 🔁 Entry Type: {{market|limit|stop}}
• 📍 Entry Price: {{entry_price}}
• ❌ Stop Loss: {{stop_loss}}
• ✅ Take Profit: {{take_profit}}
• 🧮 Pip Risk: {{pip_risk}}
• 💵 Account Size: ${{account_size}}
• ⚖️ Risk Per Trade: {{risk_percent}}% (${{dollar_risk}})
• 🔢 Lot Size: {{lot_size}}
• 🧠 Checklist:

✅ Trade from value

✅ Trend confirmation

✅ Clear entry trigger (e.g., Engulfing)
• 🧠 Pre-trade Emotion: {{emotion}}
• 🗒️ Notes: {{notes}}

## 📌 Assistant Instructions:
- Always confirm missing fields if a user provides partial data
- Suggest risk adjustments if account size or SL is too aggressive
- If integrated with Sheets, ask if they’d like to log the trade now
- Keep all trade logs reproducible and journal-friendly

## 🔒 Boundaries:
- Do not give financial advice or predict market direction
- Do not place or execute trades
- Always encourage safe and disciplined trading practices

## 🔎 User Input:
{trade_data}
    """

    try:
        response = await session.generate_response(structured_prompt)
        return response
    except Exception as e:
        error_message = f"Error generating structured trade log: {str(e)}"
        print(error_message)
        return error_message


async def main():
    """Main function to start the structured trade coach agent"""
    try:
        print("🚀 Starting Structured Forex Trading Assistant Agent...")
        print("📘 Trade planner and logger is active.")
        print("=" * 50)
        
        await session.process_events()
        
    except KeyboardInterrupt:
        print("\n👋 Agent stopped by user")
    except Exception as e:
        print(f"❌ Error starting agent: {e}")
    finally:
        print("🔚 Agent session ended")


if __name__ == "__main__":
    asyncio.run(main())
