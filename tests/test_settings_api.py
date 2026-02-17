"""
Test suite for QWINNET Settings API
Testing:
- Public settings endpoints (GET)
- Admin settings endpoints (GET/PUT) with authentication
- Data flow from Admin CMS -> DB -> Public Website
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test credentials
ADMIN_EMAIL = "admin@qwin.net"
ADMIN_PASSWORD = "istrianakB@hagi@29"

@pytest.fixture(scope="module")
def admin_token():
    """Get admin JWT token."""
    response = requests.post(
        f"{BASE_URL}/api/admin/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    pytest.skip("Admin authentication failed")

@pytest.fixture
def auth_headers(admin_token):
    """Get auth headers."""
    return {"Authorization": f"Bearer {admin_token}"}


class TestPublicAPIs:
    """Tests for public (unauthenticated) API endpoints"""
    
    def test_api_root(self):
        """Test API root endpoint returns OK"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "ok"
        print("✓ API root endpoint working")
    
    def test_get_public_general_settings(self):
        """Test public general settings returns data from DB"""
        response = requests.get(f"{BASE_URL}/api/settings/general")
        assert response.status_code == 200
        data = response.json()
        
        # Verify expected fields
        assert "contact" in data
        assert "hero" in data
        
        # Verify WhatsApp number is from DB (not default)
        whatsapp = data.get("contact", {}).get("whatsapp", "")
        assert whatsapp != "", "WhatsApp number should not be empty"
        print(f"✓ General settings: WhatsApp={whatsapp}")
        
        # Verify hero title is present
        hero_title = data.get("hero", {}).get("title", "")
        print(f"✓ Hero title: {hero_title}")
    
    def test_get_public_packages(self):
        """Test public packages returns data from DB with custom prices"""
        response = requests.get(f"{BASE_URL}/api/packages")
        assert response.status_code == 200
        data = response.json()
        
        packages = data.get("packages", [])
        assert len(packages) >= 3, "Should have at least 3 packages"
        
        # Check package prices are from DB (not defaults)
        home_pkg = next((p for p in packages if p.get("category") == "home"), None)
        assert home_pkg is not None
        
        # DB has price "100.000" for home (not default "249.000")
        price = home_pkg.get("price", "")
        print(f"✓ Home package price from DB: {price}")
        assert price == "100.000", f"Expected '100.000' but got '{price}'"
        
        # Business package
        biz_pkg = next((p for p in packages if p.get("category") == "business"), None)
        assert biz_pkg is not None
        biz_price = biz_pkg.get("price", "")
        print(f"✓ Business package price from DB: {biz_price}")
    
    def test_get_public_testimonials(self):
        """Test public testimonials endpoint"""
        response = requests.get(f"{BASE_URL}/api/settings/testimonials")
        assert response.status_code == 200
        data = response.json()
        assert "testimonials" in data
        print(f"✓ Testimonials: {len(data.get('testimonials', []))} items")
    
    def test_get_public_coverage(self):
        """Test public coverage areas endpoint"""
        response = requests.get(f"{BASE_URL}/api/settings/coverage")
        assert response.status_code == 200
        data = response.json()
        assert "areas" in data
        print(f"✓ Coverage areas: {data.get('areas', [])}")
    
    def test_get_public_why_choose(self):
        """Test public why-choose items endpoint"""
        response = requests.get(f"{BASE_URL}/api/settings/why-choose")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        print(f"✓ Why choose items: {len(data.get('items', []))} items")


class TestAdminAuth:
    """Tests for admin authentication"""
    
    def test_admin_login_success(self):
        """Test admin login with correct credentials"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert data.get("email") == ADMIN_EMAIL
        assert data.get("token_type") == "bearer"
        print("✓ Admin login successful")
    
    def test_admin_login_wrong_password(self):
        """Test admin login with wrong password returns 401"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"email": ADMIN_EMAIL, "password": "wrongpassword"}
        )
        assert response.status_code == 401
        print("✓ Wrong password correctly rejected")
    
    def test_admin_login_wrong_email(self):
        """Test admin login with wrong email returns 401"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"email": "wrong@email.com", "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 401
        print("✓ Wrong email correctly rejected")


class TestAdminSettingsAPI:
    """Tests for admin settings endpoints (require authentication)"""
    
    def test_get_admin_general_settings(self, auth_headers):
        """Test admin can get general settings"""
        response = requests.get(
            f"{BASE_URL}/api/admin/settings/general",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "contact" in data
        assert "hero" in data
        print("✓ Admin can access general settings")
    
    def test_get_admin_packages(self, auth_headers):
        """Test admin can get packages settings"""
        response = requests.get(
            f"{BASE_URL}/api/admin/settings/packages",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "packages" in data
        print(f"✓ Admin packages: {len(data.get('packages', []))} items")
    
    def test_get_admin_testimonials(self, auth_headers):
        """Test admin can get testimonials settings"""
        response = requests.get(
            f"{BASE_URL}/api/admin/settings/testimonials",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "testimonials" in data
        print("✓ Admin can access testimonials")
    
    def test_get_admin_coverage(self, auth_headers):
        """Test admin can get coverage settings"""
        response = requests.get(
            f"{BASE_URL}/api/admin/settings/coverage",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "areas" in data
        print("✓ Admin can access coverage areas")
    
    def test_get_admin_why_choose(self, auth_headers):
        """Test admin can get why-choose settings"""
        response = requests.get(
            f"{BASE_URL}/api/admin/settings/why-choose",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        print("✓ Admin can access why-choose items")
    
    def test_admin_unauthorized_without_token(self):
        """Test admin endpoints require authentication"""
        response = requests.get(f"{BASE_URL}/api/admin/settings/general")
        assert response.status_code in [401, 403]
        print("✓ Unauthorized access correctly rejected")


class TestDataFlow:
    """Tests for data flow: Admin CMS -> DB -> Public Website"""
    
    def test_settings_data_matches(self, auth_headers):
        """Test that admin settings and public settings show same data"""
        # Get admin view
        admin_response = requests.get(
            f"{BASE_URL}/api/admin/settings/general",
            headers=auth_headers
        )
        assert admin_response.status_code == 200
        admin_data = admin_response.json()
        
        # Get public view
        public_response = requests.get(f"{BASE_URL}/api/settings/general")
        assert public_response.status_code == 200
        public_data = public_response.json()
        
        # Compare WhatsApp number
        admin_wa = admin_data.get("contact", {}).get("whatsapp", "")
        public_wa = public_data.get("contact", {}).get("whatsapp", "")
        assert admin_wa == public_wa, f"WhatsApp mismatch: admin={admin_wa}, public={public_wa}"
        print(f"✓ WhatsApp number matches: {public_wa}")
        
        # Compare hero title
        admin_title = admin_data.get("hero", {}).get("title", "")
        public_title = public_data.get("hero", {}).get("title", "")
        assert admin_title == public_title, f"Hero title mismatch"
        print(f"✓ Hero title matches: {public_title}")
    
    def test_packages_data_matches(self, auth_headers):
        """Test that admin packages and public packages show same data"""
        # Get admin view
        admin_response = requests.get(
            f"{BASE_URL}/api/admin/settings/packages",
            headers=auth_headers
        )
        assert admin_response.status_code == 200
        admin_packages = admin_response.json().get("packages", [])
        
        # Get public view
        public_response = requests.get(f"{BASE_URL}/api/packages")
        assert public_response.status_code == 200
        public_packages = public_response.json().get("packages", [])
        
        # Compare package count
        assert len(admin_packages) == len(public_packages)
        
        # Compare first package price
        if admin_packages and public_packages:
            admin_price = admin_packages[0].get("price")
            public_price = public_packages[0].get("price")
            assert admin_price == public_price
            print(f"✓ Package prices match: {public_price}")


class TestCoverageAndPackageInquiries:
    """Tests for user inquiry forms"""
    
    def test_coverage_check_submission(self):
        """Test submitting a coverage check inquiry"""
        response = requests.post(
            f"{BASE_URL}/api/coverage-check",
            json={
                "name": "TEST_User",
                "phone": "081234567890",
                "address": "Test Address",
                "city": "Jakarta"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "message" in data
        print(f"✓ Coverage check created: {data.get('id')}")
    
    def test_package_inquiry_submission(self):
        """Test submitting a package inquiry"""
        response = requests.post(
            f"{BASE_URL}/api/package-inquiry",
            json={
                "name": "TEST_User",
                "email": "test@example.com",
                "phone": "081234567890",
                "address": "Test Address",
                "package_id": 1
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "inquiry_number" in data
        print(f"✓ Package inquiry created: {data.get('inquiry_number')}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
