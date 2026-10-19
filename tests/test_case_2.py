import re

import allure
from playwright.sync_api import Page, expect


@allure.feature("Books to Scrape")
@allure.title("TC2: Random Book Navigation Validation")
def test_random_book_navigation(
    books_home_page: Page, books_home_url: str, random_book_indices: list[int]
) -> None:
    """
    Verify that five randomly selected books open successfully, their
    details pages load correctly, the H1 titles match the selected book
    titles, and book information is displayed properly. Navigate back
    to the homepage after verifying each book.
    """
    page = books_home_page
    books = page.locator("article.product_pod")

    for i, index in enumerate(random_book_indices):
        with allure.step(f"Verify book #{i + 1} at index {index}"):
            book_link = books.nth(index).locator("h3 a")

            with allure.step("Capture the book title"):
                title = book_link.get_attribute("title")
                assert title, f"Book at index {index} has no title attribute"

            with allure.step("Click the book"):
                book_link.click()

            with allure.step("Verify book details page loads"):
                expect(page).to_have_url(re.compile(r"/catalogue/.+/index\.html$"))

            with allure.step("Verify H1 matches the selected book title"):
                expect(page.locator("h1")).to_have_text(title)

            with allure.step("Verify book information is visible"):
                product_info = page.locator("table.table-striped")
                expect(product_info).to_be_visible()

            with allure.step("Navigate back to homepage"):
                page.go_back()
                expect(page).to_have_url(books_home_url)
