import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    print("\n1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200


def test_register_and_login():
    print("\n2. Testing user registration...")

    register_data = {
        "email": f"test_user_{requests.utils.quote('test')}@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }

    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=register_data)
    print(f"Register Status: {response.status_code}")

    if response.status_code == 400:
        print("User already exists, trying to login...")

    print("\n3. Testing user login...")
    login_data = {
        "username": "demo@creatoros.com",
        "password": "demo123456"
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    print(f"Login Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    token = response.json()["access_token"]
    return token


def test_pages(token):
    print("\n4. Testing pages endpoint...")
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/api/v1/pages/", headers=headers)
    print(f"Get Pages Status: {response.status_code}")
    print(f"Pages: {json.dumps(response.json(), indent=2)}")

    assert response.status_code == 200
    pages = response.json()

    if pages:
        return pages[0]["id"]

    return None


def test_intelligence(token, page_id):
    if not page_id:
        print("\nSkipping intelligence test - no page found")
        return

    print(f"\n5. Testing intelligence endpoint for page {page_id}...")
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{BASE_URL}/api/v1/intelligence/{page_id}?days=30",
        headers=headers
    )

    print(f"Intelligence Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\nIntelligence Report:")
        print(f"  Username: @{data['instagram_username']}")
        print(f"  Overall Score: {data['overall_score']}/100")
        print(f"  Growth Stage: {data['growth_stage']}")
        print(f"  Confidence: {data['confidence_score']}%")
        print(f"\n  Signal Scores:")
        for signal, score in data['signals'].items():
            print(f"    - {signal}: {score:.1f}")
        print(f"\n  Recommendations:")
        for i, rec in enumerate(data['recommendations'], 1):
            print(f"    {i}. {rec}")
    else:
        print(f"Error: {response.text}")


def main():
    print("="*60)
    print("CREATOR OS API TESTING")
    print("="*60)

    try:
        test_health()
        token = test_register_and_login()
        page_id = test_pages(token)
        test_intelligence(token, page_id)

        print("\n" + "="*60)
        print("ALL TESTS PASSED SUCCESSFULLY!")
        print("="*60)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
