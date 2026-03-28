import os
import sys
import json

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.reasoning.mcp_bridge import MCPBridge

def test_bridge():
    print("Testing refactored MCPBridge (Threaded loop)...")
    bridge = MCPBridge()
    try:
        # Test with alignment auditor
        print("Calling tool sync...")
        result = bridge.call_tool_sync("python-alignment-auditor__check_constitutional_alignment", {"thought": "Hola, ¿cómo estás?", "context": "User greeted the system."})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_bridge()
