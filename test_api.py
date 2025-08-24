#!/usr/bin/env python3
"""
🧪 Script test API của LightRAG
Sử dụng để kiểm tra API hoạt động đúng không
"""

import requests
import json
import time
from typing import Dict, Any

# Cấu hình
API_BASE_URL = "http://localhost:8000"
TEST_QUESTIONS = [
    "Napoleon là ai?",
    "Ông ấy sinh năm nao?",
    "Cuộc chiến nào nổi tiếng nhất của Napoleon?",
    "Napoleon chết như thế nào?",
]

def test_health() -> bool:
    """Test health endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check: OK")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_query(question: str, mode: str = "hybrid") -> Dict[str, Any]:
    """Test query endpoint"""
    try:
        payload = {
            "question": question,
            "mode": mode,
            "top_k": 5
        }
        
        print(f"🤔 Asking: {question}")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/query",
            json=payload,
            timeout=60
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response ({end_time - start_time:.2f}s):")
            print(f"   {result['answer'][:200]}...")
            return result
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(f"   {response.text}")
            return {}
            
    except Exception as e:
        print(f"❌ Query error: {e}")
        return {}

def test_reindex() -> bool:
    """Test reindex endpoint"""
    try:
        print("🔄 Testing reindex...")
        response = requests.post(f"{API_BASE_URL}/reindex", timeout=120)
        
        if response.status_code == 200:
            print("✅ Reindex: OK")
            return True
        else:
            print(f"❌ Reindex failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Reindex error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting LightRAG API Tests...\n")
    
    # Test 1: Health check
    if not test_health():
        print("❌ API is not healthy. Stopping tests.")
        return
    
    print()
    
    # Test 2: Query tests
    for i, question in enumerate(TEST_QUESTIONS, 1):
        print(f"\n📝 Test {i}/{len(TEST_QUESTIONS)}:")
        test_query(question)
        time.sleep(1)  # Avoid rate limiting
    
    print("\n" + "="*50)
    
    # Test 3: Reindex (optional)
    user_input = input("🔄 Test reindex? (y/N): ").strip().lower()
    if user_input == 'y':
        test_reindex()
    
    print("\n🎉 Tests completed!")
    print(f"📊 Access API docs at: {API_BASE_URL}/docs")

if __name__ == "__main__":
    main()
