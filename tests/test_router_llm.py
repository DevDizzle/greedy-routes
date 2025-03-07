# tests/test_router_llm.py
import pytest
from app.router_llm import classify_routing_scenario

@pytest.mark.parametrize("message,expected_scenario", [
    ("I have 3 trucks delivering around NYC", "Multi-Vehicle Delivery Optimization"),
    ("I have 5 places to visit, shortest route", "Single-Person Route (TSP)"),
    ("Pickup some items, deliver them to X", "Pickup & Delivery with Constraints"),
    ("We do rideshare, picking up passengers", "Rideshare / Passenger Routing"),
    ("Unrelated question about finance", "No match"),
])
def test_classify_routing_scenario(message, expected_scenario):
    result = classify_routing_scenario(message)
    # Example: result might be {"scenario":"Multi-Vehicle Delivery Optimization","missing_parameters":[]}
    assert "scenario" in result, "Result must have scenario field"
    # The test might be flexible; just check if scenario is correct or 'No match'
    # If you are mocking the LLM or have a naive classifier, adapt accordingly.
    scenario = result["scenario"]
    # Because the LLM can be fuzzy, you might do partial matching or changes
    if expected_scenario == "No match":
        assert scenario in ["No match", "Error"]
    else:
        assert scenario == expected_scenario
