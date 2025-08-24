#!/usr/bin/env python3
"""
Test script for LightRAG API
Tests all endpoints with various scenarios
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_basic_info():
    """Test root endpoint"""
    print("\n🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_query(question, mode="mix", top_k=5):
    """Test query endpoint"""
    print(f"\n🔍 Testing query: '{question}'...")
    try:
        data = {
            "question": question,
            "mode": mode,
            "top_k": top_k
        }
        response = requests.post(
            f"{BASE_URL}/query",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Question: {result.get('question', 'N/A')}")
            print(f"Answer: {result.get('answer', 'N/A')[:200]}...")
            print(f"Mode: {result.get('mode', 'N/A')}")
            print(f"Status: {result.get('status', 'N/A')}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Query failed: {e}")
        return False

def test_reindex():
    """Test reindex endpoint"""
    print(f"\n🔍 Testing reindex endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/reindex")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Reindex failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting LightRAG API Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Health check
    total_tests += 1
    if test_health():
        tests_passed += 1
        print("✅ Health check passed")
    else:
        print("❌ Health check failed")
    
    # Test 2: Basic info
    total_tests += 1
    if test_basic_info():
        tests_passed += 1
        print("✅ Root endpoint passed")
    else:
        print("❌ Root endpoint failed")
    
    # Test 3: Simple query
    total_tests += 1
    if test_query("Napoleon là ai?"):
        tests_passed += 1
        print("✅ Simple query passed")
    else:
        print("❌ Simple query failed")
    
    # Test 4: Different modes
    for mode in ["naive", "local", "global", "mix"]:
        total_tests += 1
        if test_query(f"Ai là Napoleon? (mode: {mode})", mode=mode):
            tests_passed += 1
            print(f"✅ Query with mode '{mode}' passed")
        else:
            print(f"❌ Query with mode '{mode}' failed")
    
    # Test 5: Different top_k values
    for k in [3, 5, 10]:
        total_tests += 1
        if test_query(f"Napoleon sinh năm nào? (top_k: {k})", top_k=k):
            tests_passed += 1
            print(f"✅ Query with top_k={k} passed")
        else:
            print(f"❌ Query with top_k={k} failed")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print(f"⚠️  {total_tests - tests_passed} tests failed. Check the output above.")

if __name__ == "__main__":
    main()
