import allure
from playwright.sync_api import Page, expect


@allure.feature("Failed Test Case")
@allure.title("Failed Test Case")
def test_fail(books_home_page: Page, books_home_url: str) -> None:
    """
    This test is designed to fail intentionally to demonstrate the reporting capabilities of Allure.
    """
    with allure.step("Verify page URL"):
        expect(books_home_page).to_have_url("https://example.com/invalid-url")
