import pytest
from django.urls import reverse
from django.contrib.auth.models import User


class TestResponsiveDesign:
    """Test responsive design across different viewport sizes."""

    def test_dashboard_responsive_layout(self, client, user):
        """Test that dashboard layout is responsive."""
        client.force_login(user)
        response = client.get(reverse("dashboard"))
        assert response.status_code == 200
        content = response.content.decode()

        # Check viewport meta tag is present
        assert "viewport" in content
        assert "width=device-width" in content
        assert "initial-scale=1.0" in content

        # Check responsive container is used
        assert "max-w-7xl" in content
        assert "px-4" in content  # Padding for small screens

    def test_wizard_responsive_forms(self, client, user, harada_chart):
        """Test that wizard forms are responsive."""
        client.force_login(user)
        response = client.get(reverse("wizard_step1", args=[harada_chart.id]))
        assert response.status_code == 200
        content = response.content.decode()

        # Check responsive input fields
        assert "max-w" in content  # Max width constraint
        assert "rounded" in content  # Rounded corners (modern mobile-friendly)

    def test_matrix_grid_responsive(self, client, user, harada_chart, pillars, tasks):
        """Test that matrix grid uses responsive grid layout."""
        client.force_login(user)
        harada_chart.is_draft = False
        harada_chart.save()

        response = client.get(reverse("matrix_view", args=[harada_chart.id]))
        assert response.status_code == 200
        content = response.content.decode()

        # Check for responsive grid
        assert "grid-template-columns: repeat(9" in content
        assert "minmax" in content  # Grid uses minmax for responsiveness
        assert "overflow-x-auto" in content  # Horizontal scroll on small screens

    def test_modal_responsive_sizing(self, client, user, harada_chart, pillars):
        """Test that modals are responsive on small screens."""
        client.force_login(user)
        pillar = pillars[0]

        response = client.get(
            reverse("pillar_modal", args=[harada_chart.id, pillar.id])
        )
        assert response.status_code == 200
        content = response.content.decode()

        # Check modal has responsive max width
        assert "max-w-md" in content  # Medium max width on desktop
        assert "w-full" in content  # Full width on mobile

    def test_nav_responsive(self, client):
        """Test that navigation is responsive."""
        response = client.get(reverse("login"))
        assert response.status_code == 200
        content = response.content.decode()

        # Check nav uses flex for responsive alignment
        assert "flex justify-between items-center" in content
        assert "gap-4" in content  # Responsive gap between nav items

    def test_forms_have_mobile_friendly_inputs(self, client):
        """Test that forms use mobile-friendly input types."""
        response = client.get(reverse("register"))
        assert response.status_code == 200
        content = response.content.decode()

        # Check for proper input types
        assert 'type="email"' in content or "email" in content
        assert 'type="password"' in content or "password" in content
        # Form fields should be full width on mobile
        assert "w-full" in content

    def test_button_sizing_accessible(self, client):
        """Test that buttons are properly sized for touch interaction."""
        response = client.get(reverse("login"))
        assert response.status_code == 200
        content = response.content.decode()

        # Buttons should have adequate padding for touch targets (min 44x44px)
        assert "py-2 px-4" in content or "py-3" in content
        assert "rounded" in content  # Modern button styling

    def test_dark_mode_colors_responsive(self, client, user, harada_chart, pillars):
        """Test that dark mode colors are properly applied for responsive UI."""
        client.force_login(user)
        harada_chart.is_draft = False
        harada_chart.save()

        response = client.get(reverse("matrix_view", args=[harada_chart.id]))
        assert response.status_code == 200
        content = response.content.decode()

        # Check dark mode classes are present
        assert "dark:bg-slate-800" in content
        assert "dark:text-" in content
        # Check for theme consistency
        assert "transition-colors" in content

    def test_text_readability_responsive(
        self, client, user, harada_chart, pillars, tasks
    ):
        """Test that text remains readable at all viewport sizes."""
        client.force_login(user)
        harada_chart.is_draft = False
        harada_chart.save()

        response = client.get(reverse("matrix_view", args=[harada_chart.id]))
        assert response.status_code == 200
        content = response.content.decode()

        # Check for text clipping to prevent overflow
        assert "line-clamp-" in content  # Text clamping for truncation
        assert "text-xs" in content or "text-sm" in content  # Reasonable font sizes

    def test_dashboard_cards_responsive(self, client, user):
        """Test that dashboard cards are responsive."""
        client.force_login(user)
        response = client.get(reverse("dashboard"))
        assert response.status_code == 200
        content = response.content.decode()

        # Check for responsive card layout
        assert "rounded-lg" in content  # Card styling
        assert "shadow" in content  # Card shadow for depth
        assert "p-" in content  # Padding classes
