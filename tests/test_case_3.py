import re

import allure
from playwright.sync_api import Page, expect


@allure.feature("Books to Scrape")
@allure.title("TC3: Book Data Consistency Validation")
def test_book_data_consistency(
    books_home_page: Page, books_home_url: str, random_book_indices: list[int]
) -> None:
    page = books_home_page
    books = page.locator("article.product_pod")

    for i, index in enumerate(random_book_indices):
        with allure.step(f"Verify book #{i + 1} at index {index}"):
            book = books.nth(index)
            book_link = book.locator("h3 a")

            with allure.step("Capture homepage title and price"):
                home_title = book_link.get_attribute("title")
                home_price = book.locator("p.price_color").inner_text()

            with allure.step("Open book details page"):
                book_link.click()
                expect(page).to_have_url(re.compile(r"/catalogue/.+/index\.html$"))

            with allure.step("Capture details page title and price"):
                details_title = page.locator("h1").inner_text()
                details_price = page.locator("div.product_main p.price_color").inner_text()

            with allure.step("Compare homepage and details page title"):
                assert home_title == details_title

            with allure.step("Compare homepage and details page price"):
                assert home_price == details_price

            with allure.step("Navigate back to homepage"):
                page.go_back()
                expect(page).to_have_url(books_home_url)
