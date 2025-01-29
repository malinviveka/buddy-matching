import pytest
from playwright.sync_api import sync_playwright
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

@pytest.mark.django_db
def test_login_page(live_server):
    """tests login page"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # tests for chrome
        page = browser.new_page()

        # go to url
        page.goto(live_server.url + reverse("login"))  

        # fill out form
        page.fill("input[name='email']", "testuser@stud.tu-darmstadt.de")  
        page.fill("input[name='password']", "testpassword")  
        page.click("button[type='submit']")

        browser.close()

