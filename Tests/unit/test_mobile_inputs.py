import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestMobileInputSizing:
    """Test form input sizing for mobile responsiveness."""

    def test_task_modal_inputs_have_min_font_size(self, client, user, harada_chart, pillars, tasks):
        """Test that task modal inputs have at least 16px font size for mobile."""
        client.force_login(user)
        task = tasks[0]
        url = reverse('task_modal', args=[harada_chart.id, task.id])
        response = client.get(url)
        assert response.status_code == 200
        content = response.content.decode()

        # Check for text-[16px] or text-base on input/textarea/select
        # Red phase: this should fail initially as they don't have these classes explicitly
        assert "text-[16px]" in content or "text-base" in content
