import re

import allure
from playwright.sync_api import Page, expect


@allure.feature("Quotes to Scrape")
@allure.title("TC6: Login Functionality and Logout Link Validation")
def test_login_and_logout_link(
    quotes_home_page: Page, quotes_home_url: str, quotes_credentials: dict[str, str]
) -> None:
    """
    Verify that the login functionality on Quotes to Scrape works
    correctly by opening the homepage, navigating to the login page,
    entering valid credentials, and submitting the login form. Verify
    that the login request completes successfully and that the Logout
    link is visible, enabled, and available for interaction.
    """
    page = quotes_home_page
    login_link = page.get_by_role("link", name="Login")
    logout = page.get_by_role("link", name="Logout")
    login_button = page.get_by_role("button", name="Login")
    username_input = page.locator("#username")
    password_input = page.locator("#password")

    with allure.step("Verify Quotes homepage loads successfully"):
        expect(page).to_have_url(quotes_home_url)
        expect(page).to_have_title("Quotes to Scrape")

    with allure.step("Verify Login link is visible and enabled"):
        expect(login_link).to_be_visible()
        expect(login_link).to_be_enabled()

    with allure.step("Click the Login link"):
        login_link.click()

    with allure.step("Verify login page loads successfully"):
        expect(page).to_have_url(re.compile(r"/login$"))
        expect(username_input).to_be_visible()
        expect(password_input).to_be_visible()

    with allure.step("Enter username"):
        username_input.fill(quotes_credentials["username"])

    with allure.step("Enter password"):
        password_input.fill(quotes_credentials["password"])

    with allure.step("Click Login and verify the login request completes successfully"):
        with page.expect_navigation() as navigation_info:
            login_button.click()
        response = navigation_info.value
        assert response is not None
        assert response.ok, f"Login did not complete successfully (status {response.status})"
        expect(page).not_to_have_url(re.compile(r"/login$"))

    with allure.step("Verify Logout link is visible"):
        expect(logout).to_be_visible()

    with allure.step("Verify Logout link is enabled"):
        expect(logout).to_be_enabled()
