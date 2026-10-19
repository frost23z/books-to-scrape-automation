import allure
import pytest
from playwright.sync_api import Page

BOOKS_HOME_URL: str = "https://books.toscrape.com/index.html"


@pytest.fixture(scope="session")
def books_home_url() -> str:
    return BOOKS_HOME_URL


@pytest.fixture
def books_home_page(page: Page, books_home_url: str) -> Page:
    with allure.step(f"Navigate to: {books_home_url}"):
        page.goto(books_home_url)
    return page
