import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestPerformanceOptimizations:
    """Test performance optimizations in base.html."""

    def test_scripts_are_deferred_or_at_bottom(self, client):
        """Test that non-critical scripts are deferred or placed at the bottom."""
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200
        content = response.content.decode()

        # Check for defer attribute on Clerk script
        assert 'clerk-js@5/dist/clerk.browser.js' in content
        assert 'defer' in content
        
        # Check for HTMX defer
        assert 'htmx.org@1.9.10' in content
        
        # Check if the main custom script is still there
        assert 'window.addEventListener(\'load\', async () => {' in content
