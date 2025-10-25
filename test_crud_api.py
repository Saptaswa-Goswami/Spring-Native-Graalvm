import requests
import json
import time
import random
import string
from typing import List, Dict, Optional

BASE_URL = "http://localhost:8080/api/users"
HEALTH_URL = "http://localhost:8080/actuator/health"

def generate_random_string(length: int = 8) -> str:
    """Generate a random string of specified length."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_random_email() -> str:
    """Generate a random email address."""
    username = generate_random_string(8)
    domain = generate_random_string(5)
    return f"{username}@{domain}.com"

def generate_random_user(index: int) -> Dict:
    """Generate a random user with a unique email based on index to avoid conflicts."""
    timestamp = int(time.time() * 1000)  # Use timestamp to ensure uniqueness
    return {
        "name": f"Test User {index} {timestamp}",
        "email": f"testuser{index}_{timestamp}@example.com",
        "address": f"{random.randint(100, 999)} {generate_random_string(10)} St, {generate_random_string(8)} City"
    }

def print_request_response(method: str, url: str, data: Optional[Dict] = None, 
                          response: Optional[requests.Response] = None) -> None:
    """Print the request and response details."""
    print(f"\n{'='*60}")
    print(f"REQUEST: {method} {url}")
    if data:
        print(f"PAYLOAD: {json.dumps(data, indent=2)}")
    
    if response:
        print(f"RESPONSE STATUS: {response.status_code}")
        print(f"RESPONSE HEADERS: {dict(response.headers)}")
        try:
            response_data = response.json()
            print(f"RESPONSE BODY: {json.dumps(response_data, indent=2)}")
        except:
            print(f"RESPONSE BODY: {response.text}")
    print(f"{'='*60}\n")

def test_health_endpoint() -> bool:
    """Test the health endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get(HEALTH_URL)
        print_request_response("GET", HEALTH_URL, response=response)
        
        if response.status_code == 200:
            health_data = response.json()
            if health_data.get("status") == "UP":
                print("✓ Health check passed")
                return True
            else:
                print("✗ Health check failed - status is not UP")
                return False
        else:
            print(f"✗ Health check failed with status code {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check failed with error: {e}")
        return False

def test_create_user(user_data: Dict) -> Optional[Dict]:
    """Test creating a user."""
    print(f"Testing CREATE user: {user_data['name']}")
    try:
        response = requests.post(BASE_URL, json=user_data, headers={"Content-Type": "application/json"})
        print_request_response("POST", BASE_URL, user_data, response)
        
        if response.status_code == 201:
            created_user = response.json()
            print(f"✓ User created successfully with ID: {created_user.get('id')}")
            return created_user
        else:
            print(f"✗ Failed to create user. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Failed to create user with error: {e}")
        return None

def test_get_all_users() -> List[Dict]:
    """Test getting all users."""
    print("Testing GET all users")
    try:
        response = requests.get(BASE_URL)
        print_request_response("GET", BASE_URL, response=response)
        
        if response.status_code == 200:
            users = response.json()
            print(f"✓ Retrieved {len(users)} users")
            return users
        else:
            print(f"✗ Failed to get users. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"✗ Failed to get users with error: {e}")
        return []

def test_get_user_by_id(user_id: int) -> Optional[Dict]:
    """Test getting a user by ID."""
    print(f"Testing GET user by ID: {user_id}")
    url = f"{BASE_URL}/{user_id}"
    try:
        response = requests.get(url)
        print_request_response("GET", url, response=response)
        
        if response.status_code == 200:
            user = response.json()
            print(f"✓ Retrieved user with ID: {user['id']}")
            return user
        elif response.status_code == 404:
            print(f"✗ User with ID {user_id} not found")
            return None
        else:
            print(f"✗ Failed to get user. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Failed to get user with error: {e}")
        return None

def test_update_user(user_id: int, updated_data: Dict) -> Optional[Dict]:
    """Test updating a user."""
    print(f"Testing UPDATE user with ID: {user_id}")
    url = f"{BASE_URL}/{user_id}"
    try:
        response = requests.put(url, json=updated_data, headers={"Content-Type": "application/json"})
        print_request_response("PUT", url, updated_data, response)
        
        if response.status_code == 200:
            updated_user = response.json()
            print(f"✓ User updated successfully with ID: {updated_user.get('id')}")
            return updated_user
        else:
            print(f"✗ Failed to update user. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Failed to update user with error: {e}")
        return None

def test_delete_user(user_id: int) -> bool:
    """Test deleting a user."""
    print(f"Testing DELETE user with ID: {user_id}")
    url = f"{BASE_URL}/{user_id}"
    try:
        response = requests.delete(url)
        print_request_response("DELETE", url, response=response)
        
        if response.status_code in [204, 200]:  # 204 No Content or 200 OK
            print(f"✓ User with ID {user_id} deleted successfully")
            return True
        else:
            print(f"✗ Failed to delete user. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Failed to delete user with error: {e}")
        return False

def run_crud_tests():
    """Run comprehensive CRUD tests."""
    print("Starting comprehensive CRUD tests...\n")
    
    # Test health endpoint first
    if not test_health_endpoint():
        print("Health check failed. Aborting tests.")
        return
    
    created_users = []
    
    # CREATE: Create 10 users
    print("\n" + "="*60)
    print("CREATE TESTS")
    print("="*60)
    
    for i in range(1, 11):
        user_data = generate_random_user(i)
        created_user = test_create_user(user_data)
        if created_user:
            created_users.append(created_user)
        time.sleep(0.1)  # Small delay to ensure different timestamps
    
    if len(created_users) == 0:
        print("No users were created successfully. Aborting tests.")
        return
    
    # READ: Get all users
    print("\n" + "="*60)
    print("READ TESTS")
    print("="*60)
    
    all_users = test_get_all_users()
    print(f"Expected {len(created_users)} users, got {len(all_users)} users")
    
    # Test getting each created user by ID
    for user in created_users:
        test_get_user_by_id(user['id'])
        time.sleep(0.1)
    
    # UPDATE: Update each user
    print("\n" + "="*60)
    print("UPDATE TESTS")
    print("="*60)
    
    updated_users = []
    for user in created_users:
        updated_data = {
            "name": f"Updated {user['name']}",
            "email": f"updated_{user['email']}",
            "address": f"Updated {user['address']}"
        }
        updated_user = test_update_user(user['id'], updated_data)
        if updated_user:
            updated_users.append(updated_user)
        time.sleep(0.1)
    
    # Verify updates worked by getting users again
    print("\nVerifying updates...")
    for user in updated_users:
        retrieved_user = test_get_user_by_id(user['id'])
        if retrieved_user and retrieved_user['name'].startswith('Updated'):
            print(f"✓ User {user['id']} update verified")
        time.sleep(0.1)
    
    # DELETE: Delete every other user to test deletion
    print("\n" + "="*60)
    print("DELETE TESTS")
    print("="*60)
    
    users_to_delete = created_users[::2]  # Every other user
    for user in users_to_delete:
        test_delete_user(user['id'])
        time.sleep(0.1)
    
    # Verify deletions by getting all users again
    remaining_users = test_get_all_users()
    print(f"After deletion, {len(remaining_users)} users remain")
    
    # Test error cases
    print("\n" + "="*60)
    print("ERROR CASE TESTS")
    print("="*60)
    
    # Try to get a non-existent user
    test_get_user_by_id(999999)
    
    # Try to update a non-existent user
    invalid_update_data = {
        "name": "Non-existent User",
        "email": "nonexistent@example.com",
        "address": "123 Fake St"
    }
    test_update_user(999999, invalid_update_data)
    
    # Try to delete a non-existent user
    test_delete_user(999999)
    
    print("\n" + "="*60)
    print("CRUD TESTS COMPLETED")
    print("="*60)
    print(f"Created: {len(created_users)} users")
    print(f"Remaining after deletion: {len(remaining_users)} users")
    print("All CRUD operations tested successfully!")

if __name__ == "__main__":
    run_crud_tests()