import allure
import requests
from playwright.sync_api import Page


@allure.feature("Books to Scrape")
@allure.title("TC4: Broken Link Validation")
def test_no_broken_links(
    books_home_page: Page, http_session: requests.Session, request_timeout_seconds: int
) -> None:
    """
    Verify that all unique hyperlinks on the homepage return successful
    HTTP response status codes by collecting anchor elements, extracting
    their href values, removing duplicate URLs, and sending requests to
    each URL.
    """
    page = books_home_page

    with allure.step("Collect all anchor elements"):
        anchor_elements = page.locator("a[href]")

    with allure.step("Extract all href attributes"):
        hrefs: list[str] = anchor_elements.evaluate_all(
            "elements => elements.map(element => element.href)"
        )

    with allure.step("Remove duplicate URLs"):
        hrefs = [href for href in dict.fromkeys(hrefs) if href]

    results: dict[str, int | str] = {}
    with allure.step(f"Send requests to {len(hrefs)} unique URLs"):
        for url in hrefs:
            try:
                results[url] = http_session.get(url, timeout=request_timeout_seconds).status_code
            except requests.RequestException as error:
                results[url] = type(error).__name__

    with allure.step("Verify every URL returned HTTP 200"):
        broken_links = [
            f"{url} (Status: {status})" for url, status in results.items() if status != 200
        ]
        if broken_links:
            allure.attach(
                "\n".join(broken_links),
                name="Broken Links",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not broken_links, "Broken links found:\n" + "\n".join(broken_links)
