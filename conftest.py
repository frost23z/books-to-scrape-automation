import random
import shutil
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

BOOKS_HOME_URL: str = "https://books.toscrape.com/index.html"
RANDOM_BOOK_COUNT: int = 5
SEED: int = 42


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session: pytest.Session) -> None:
    reports_dir = Path("reports")
    shutil.rmtree(reports_dir, ignore_errors=True)
    (reports_dir / "allure-results").mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def books_home_url() -> str:
    return BOOKS_HOME_URL


@pytest.fixture(scope="session")
def random_no_generator() -> random.Random:
    return random.Random(SEED)


@pytest.fixture
def books_home_page(page: Page, books_home_url: str) -> Page:
    with allure.step(f"Navigate to: {books_home_url}"):
        page.goto(books_home_url)
    return page


@pytest.fixture
def random_book_indices(books_home_page: Page, random_no_generator: random.Random) -> list[int]:
    with allure.step("Collect all available books on the homepage"):
        total_books_on_page = books_home_page.locator("article.product_pod").count()
    with allure.step(
        f"Select {RANDOM_BOOK_COUNT} random books indices "
        f"from {total_books_on_page} available books"
    ):
        assert total_books_on_page >= RANDOM_BOOK_COUNT, (
            f"Not enough books on the homepage to select {RANDOM_BOOK_COUNT} random books."
        )
        indices = sorted(random_no_generator.sample(range(total_books_on_page), RANDOM_BOOK_COUNT))
        allure.dynamic.parameter("random_book_indices", indices)
    return indices
