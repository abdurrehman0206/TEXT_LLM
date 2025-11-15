"""
Simple script to test the Paraphrase API
Run this after starting the Docker container
"""
import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("=" * 60)
    print("Testing Health Endpoint")
    print("=" * 60)
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        data = response.json()
        print(f"✓ Health check passed!")
        print(f"  Status: {data['status']}")
        print(f"  Model loaded: {data['model_loaded']}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_root():
    """Test the root endpoint"""
    print("\n" + "=" * 60)
    print("Testing Root Endpoint")
    print("=" * 60)
    try:
        response = requests.get(f"{API_BASE_URL}/")
        response.raise_for_status()
        data = response.json()
        print(f"✓ Root endpoint working!")
        print(f"  Message: {data['message']}")
        print(f"  Status: {data['status']}")
        return True
    except Exception as e:
        print(f"✗ Root endpoint failed: {e}")
        return False

def test_paraphrase():
    """Test the paraphrase endpoint"""
    print("\n" + "=" * 60)
    print("Testing Paraphrase Endpoint")
    print("=" * 60)
    
    test_article = """The Minister of Livestock and Rural Development of Somaliland, Omar Shucayb Mohamed, who participated in the Consultative Meeting on Addressing Trade Barriers and Enhancing Livestock Exports, stated that the country's economy heavily relies on livestocks, emphasizing that this sector generates the majority of the nation's hard currency earnings.

He said: "When looking at the national economy, 70% of our revenue comes from livestock."

The consultative meeting on livestock trade barriers and export development, held yesterday in Hargeisa, focused on the challenges facing livestock trade and export promotion in Somaliland."""
    
    payload = {
        "article": test_article,
        "max_tokens": 1000
    }
    
    print(f"Original article length: {len(test_article)} characters")
    print("Sending request... (this may take 30-60 seconds)")
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{API_BASE_URL}/paraphrase",
            json=payload,
            timeout=120  # 2 minute timeout
        )
        response.raise_for_status()
        data = response.json()
        elapsed_time = time.time() - start_time
        
        print(f"✓ Paraphrase request successful!")
        print(f"\nResponse time: {elapsed_time:.2f} seconds")
        print(f"\nStatistics:")
        stats = data['statistics']
        print(f"  Original words: {stats['original_word_count']}")
        print(f"  Paraphrased words: {stats['paraphrased_word_count']}")
        print(f"  Length match: {stats['length_match_percentage']:.1f}%")
        print(f"  Inference time: {stats['inference_time_seconds']:.2f} seconds")
        print(f"  Tokens per second: {stats['tokens_per_second']:.2f}")
        
        print(f"\nOriginal Article (first 100 chars):")
        print(f"  {data['original_article'][:100]}...")
        
        print(f"\nParaphrased Article (first 100 chars):")
        print(f"  {data['paraphrased_article'][:100]}...")
        
        return True
    except requests.exceptions.Timeout:
        print("✗ Request timed out (this is normal for large articles)")
        return False
    except Exception as e:
        print(f"✗ Paraphrase request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"  Error details: {error_data}")
            except:
                print(f"  Response: {e.response.text}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PARAPHRASE API TEST SUITE")
    print("=" * 60)
    print(f"Testing API at: {API_BASE_URL}")
    print("\nMake sure the Docker container is running!")
    print("Press Ctrl+C to cancel\n")
    
    time.sleep(2)
    
    results = []
    
    # Test health endpoint
    results.append(("Health Check", test_health()))
    
    # Test root endpoint
    results.append(("Root Endpoint", test_root()))
    
    # Test paraphrase endpoint
    results.append(("Paraphrase Endpoint", test_paraphrase()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")

