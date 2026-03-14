import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestGlobalResponsiveness:
    """Test global responsive elements in base.html."""

    def test_safe_area_insets_and_padding(self, client):
        """Test that base template includes safe-area insets and responsive padding."""
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200
        content = response.content.decode()

        # Check for safe-area-inset-bottom (Red phase: this should fail)
        assert "env(safe-area-inset-bottom)" in content
        
        # Check for responsive padding px-4 md:px-8
        # Current is px-4, let's see if we can find md:px-8
        assert "px-4 md:px-8" in content
