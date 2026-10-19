import re

import allure
from playwright.sync_api import Page, expect


@allure.feature("Books to Scrape")
@allure.title("TC1: Homepage Validation")
def test_home_page(books_home_page: Page, books_home_url: str) -> None:
    """
    Verify that the page URL and title match the expected values,
    all visible headings (h1-h6) are displayed and contain non-empty
    text, and the Books section is visible and contains at least
    one book item.
    """
    page = books_home_page
    headings = page.locator("h1, h2, h3, h4, h5, h6")
    books_section = page.locator("section:has(ol.row)")
    books = page.locator("section:has(ol.row) ol.row li")

    with allure.step("Verify page URL"):
        expect(page).to_have_url(books_home_url)

    with allure.step("Verify page title"):
        expect(page).to_have_title("All products | Books to Scrape - Sandbox")

    with allure.step("Verify all headings are visible"):
        expect(headings.first).to_be_visible()
        for heading in headings.all():
            expect(heading).to_be_visible()

    with allure.step("Verify every heading contains non-empty text"):
        for heading in headings.all():
            expect(heading).to_have_text(re.compile(r"\S"))

    with allure.step("Verify books section is visible"):
        expect(books_section).to_be_visible()

    with allure.step("Verify books section contains at least one book"):
        expect(books.first).to_be_visible()
        assert books.count() >= 1
