# router_llm.py

import os
import re
import json
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Retrieve your Gemini (PaLM) API key from an environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.warning("No GEMINI_API_KEY found in environment variables.")

# Configure the google-generativeai library with your key
genai.configure(api_key=GEMINI_API_KEY)

# Create a GenerativeModel for Gemini 1.5 Pro
model = genai.GenerativeModel("gemini-1.5-pro")

def classify_routing_scenario(user_message: str) -> dict:
    """
    Classifies a user message to determine the routing scenario using Gemini 1.5 Pro.

    Returns a dict in the format:
       {
         "scenario": "<scenario_name or 'No match'>",
         "missing_parameters": ["param1", ...]
       }
    or an error fallback if something goes wrong.
    """
    try:
        logger.info("Starting classification of user message.")

        # Build the scenario-classification prompt
        prompt = f"""
You are a routing scenario classifier for a route optimization system.

Below is a mapping of routing scenarios and their relevant parameters:

- Multi-Vehicle Delivery Optimization: vehicles, shipments, timeWindows, vehicleCapacity, avoidTolls, multiTrip
- Single-Person Route (TSP): locations, timeWindows (optional), avoidTolls (optional)
- Pickup & Delivery with Constraints: pickups, deliveries, loadDemands, timeWindows, vehicleCapacity
- Rideshare / Passenger Routing: pickups, deliveries, timeWindows, maxPassengers, vehicleType

User Query: "{user_message}"

Based on the user query, determine the routing scenario that best fits the request.
Return your answer in the following JSON format:

{{
  "scenario": "<scenario_name>",
  "missing_parameters": ["param1", "param2", ...]
}}

If the query does not match any known scenario, return:

{{
  "scenario": "No match",
  "missing_parameters": []
}}
"""

        logger.info("Sending prompt to Gemini model.")

        # Call Gemini with generate_content
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,
            }
        )

        # Check if we got a valid response
        if not response or not response.text:
            logger.error("No valid response from Gemini classification.")
            raise ValueError("No response from Gemini classification.")

        raw_text = response.text.strip()
        logger.info(f"Router LLM raw response: {raw_text}")

        # Extract JSON from the LLM's output using a regex
        json_match = re.search(r"{[\s\S]*}", raw_text)
        if not json_match:
            logger.warning("Could not find JSON object in LLM output; returning 'No match'.")
            return {
                "scenario": "No match",
                "missing_parameters": []
            }

        json_string = json_match.group(0)
        parsed_output = json.loads(json_string)
        return parsed_output

    except Exception as e:
        logger.exception("Error in classify_routing_scenario:")
        # Return a fallback
        return {
            "scenario": "Error",
            "missing_parameters": [str(e)]
        }
