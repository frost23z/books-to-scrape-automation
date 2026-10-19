import re

import allure
from playwright.sync_api import Page, expect

MAX_PAGES: int = 5


@allure.feature("Books to Scrape")
@allure.title("TC5: Product Image Validation")
def test_product_images_across_pages(books_home_page: Page) -> None:
    """
    Verify that all product images on the homepage and subsequent
    pages are visible and have non-empty src and alt attributes,
    and that their class attributes contain 'thumbnail'. Click the
    Next button to validate images on subsequent pages, continuing
    for a maximum of five pages or until pagination ends.
    """
    page = books_home_page
    pages_validated = 0

    for page_number in range(1, MAX_PAGES + 1):
        with allure.step(f"Verify images on page {page_number}"):
            with allure.step("Collect all product images"):
                images = page.locator("article.product_pod img")
                expect(images.first).to_be_visible()

            for i, image in enumerate(images.all()):
                with allure.step(f"Verify image #{i + 1}"):
                    expect(image).to_be_visible()
                    expect(image).to_have_attribute("src", re.compile(r"\S"))
                    expect(image).to_have_attribute("alt", re.compile(r"\S"))
                    expect(image).to_have_class(re.compile(r"\bthumbnail\b"))
        pages_validated += 1

        next_button = page.locator("li.next a")
        if page_number == MAX_PAGES or next_button.count() == 0:
            break

        with allure.step(f"Click Next to go to page {page_number + 1}"):
            next_button.click()
            expect(page).to_have_url(re.compile(rf"/page-{page_number + 1}\.html$"))

    with allure.step("Verify pagination moved past the first page"):
        assert pages_validated > 1
