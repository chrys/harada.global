import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_base_template_has_meta_description(client):
    """Test that the base template (via home page) includes a meta description tag."""
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    # This should fail initially because we haven't added the tag yet.
    assert '<meta name="description"' in response.content.decode()
