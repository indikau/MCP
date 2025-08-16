from dispatcher_agent import run_dispatcher
from shared_schema import validate_schema
import os


import asyncio

async def test_dispatcher_workflow():
    print("🚀 Starting Dispatcher Agent Test...")

    # Step 1: Run dispatcher agent to get trending stock data
    results = await run_dispatcher()
    print(f"✅ Retrieved {len(results)} entries.")

    # Step 2: Validate schema of first entry (if any)
    if results:
        first_entry = results[0]
        is_valid = validate_schema(first_entry)
        print("🔎 Sample Entry:", first_entry)
        print("✅ Schema Validation:", "Passed" if is_valid else "Failed")
    else:
        print("⚠️ No data returned.")

    # Step 3: Check output mode from .env
    output_mode = os.getenv("OUTPUT_MODE", "csv")
    print(f"🛠️ Output Mode: {output_mode}")
    if output_mode not in ["csv", "sqlite"]:
        print(f"❌ Unsupported OUTPUT_MODE: {output_mode}")
    else:
        print("✅ Dispatcher will save data properly.")

if __name__ == "__main__":
    asyncio.run(test_dispatcher_workflow())