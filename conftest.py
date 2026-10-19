import logging
import random
import shutil
from collections.abc import Generator
from pathlib import Path

import allure
import pytest
import requests
from playwright.sync_api import Page

BOOKS_HOME_URL: str = "https://books.toscrape.com/index.html"
QUOTES_HOME_URL: str = "https://quotes.toscrape.com/"
RANDOM_BOOK_COUNT: int = 5
SEED: int = 42
REQUEST_TIMEOUT_SECONDS: int = 5
QUOTES_USERNAME: str = "admin"
QUOTES_PASSWORD: str = "admin"
ALLURE_ATTACHMENT_TYPES = {
    ".png": allure.attachment_type.PNG,
    ".webm": allure.attachment_type.WEBM,
    ".zip": allure.attachment_type.ZIP,
}

logger = logging.getLogger(__name__)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session: pytest.Session) -> None:
    reports_dir = Path("reports")
    shutil.rmtree(reports_dir, ignore_errors=True)
    (reports_dir / "allure-results").mkdir(parents=True, exist_ok=True)
    (reports_dir / "test-results").mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    if report.when != "teardown":
        return

    for name, relative_path in report.user_properties:
        if name.startswith("playwright_"):
            path = item.config.invocation_params.dir / relative_path
            allure.attach.file(
                path,
                name=path.name,
                attachment_type=ALLURE_ATTACHMENT_TYPES.get(path.suffix),
            )


@pytest.fixture(scope="session")
def books_home_url() -> str:
    return BOOKS_HOME_URL


@pytest.fixture(scope="session")
def quotes_home_url() -> str:
    return QUOTES_HOME_URL


@pytest.fixture(scope="session")
def random_no_generator() -> random.Random:
    return random.Random(SEED)


@pytest.fixture(scope="session")
def request_timeout_seconds() -> int:
    return REQUEST_TIMEOUT_SECONDS


@pytest.fixture(scope="session")
def http_session() -> Generator[requests.Session]:
    with requests.Session() as session:
        yield session


@pytest.fixture(scope="session")
def quotes_credentials() -> dict[str, str]:
    return {"username": QUOTES_USERNAME, "password": QUOTES_PASSWORD}


@pytest.fixture
def books_home_page(page: Page, books_home_url: str) -> Page:
    with allure.step(f"Navigate to: {books_home_url}"):
        page.goto(books_home_url)
    return page


@pytest.fixture
def quotes_home_page(page: Page, quotes_home_url: str) -> Page:
    with allure.step(f"Navigate to: {quotes_home_url}"):
        page.goto(quotes_home_url)
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
