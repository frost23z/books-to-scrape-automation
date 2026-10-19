# Enterprise UI Automation Framework – Books to Scrape

## Project Overview

A UI automation framework built with `pytest-playwright`. It validates
the practice sites [Books to Scrape](https://books.toscrape.com/index.html) and
[Quotes to Scrape](https://quotes.toscrape.com/): homepage content, navigation,
data consistency, broken links, images with pagination, login/logout.

It runs locally, in Docker, and in GitHub Actions, and produces both an HTML report and an Allure report.

## Features

- 6 functional test cases (see [Test Case Coverage](#test-case-coverage))
- Shared fixtures in `conftest.py` (URLs, ready-to-use pages, seeded random book selection,
  HTTP session, credentials)
- Allure steps for every verification, nested per book/image, so failures point at the exact item
- Failure screenshots attached to the Allure report; screenshots, videos and traces retained on failure
- HTML report (`pytest-html`) and Allure report, locally and in CI
- Docker image and `compose.yml`
- GitHub Actions pipeline that publishes artifacts and the Allure report
- Linting and formatting with Ruff, plus pre-commit hooks

## Tech Stack

| Area | Tool |
| --- | --- |
| Language | Python 3.14 |
| Browser automation | Playwright (sync API), Chromium by default |
| Test runner | Pytest with `pytest-playwright` |
| Reports | `pytest-html`, `allure-pytest` (Allure CLI for viewing) |
| HTTP checks | `requests` |
| Dependency management | [uv](https://docs.astral.sh/uv/) (`pyproject.toml` + `uv.lock`) |
| Code quality | Ruff, pre-commit |
| Containers | Docker, Docker Compose |
| CI/CD | GitHub Actions |

## Installation Guide

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Clone the repository and install dependencies. uv reads `.python-version` and
   downloads Python 3.14 automatically if needed:

   ```bash
   git clone https://github.com/frost23z/books-to-scrape-automation
   cd books-to-scrape-automation
   uv sync
   ```

3. Install the Playwright browser:

   ```bash
   uv run playwright install chromium
   # On a fresh Linux machine also install system libraries:
   uv run playwright install --with-deps chromium
   ```

4. (Optional) Install the Allure CLI to view Allure reports locally:

   ```bash
   npm install -g allure
   ```

   Check other ways to install allure cli <https://allurereport.org/docs/v3/install/>

## Environment Setup

No configuration is required. Defaults for pytest options (HTML/Allure output, tracing, video, screenshots, logging) live
in `pytest.ini`. Constants such as URLs and timeouts are at the top of `conftest.py`.

## Running Tests

```bash
uv run pytest                                  # all tests, headless Chromium
uv run pytest tests/test_case_2.py             # one file
uv run pytest --headed --slowmo 300            # watch the browser
uv run pytest --browser firefox                # other browser (install it first)
```

### Docker

```bash
# Run with Compose (mounts the project, so edits are picked up without a rebuild)
docker compose up --build
```

If you change dependencies, refresh Compose's cached virtualenv volume with
`docker compose up --build --renew-anon-volumes`.

The base image tag (`v1.64.0-resolute`) must match the `playwright` version in `uv.lock`.
Update both together.

### Linting

```bash
uv run ruff check .
uv run ruff format --check .
```

## Project Structure

```text
.
├── .github/workflows/playwright.yml   # CI pipeline
├── tests/
│   ├── test_case_1.py                 # Homepage validation
│   ├── test_case_2.py                 # Random book navigation
│   ├── test_case_3.py                 # Book data consistency
│   ├── test_case_4.py                 # Broken link validation
│   ├── test_case_5.py                 # Product images + pagination
│   ├── test_case_6.py                 # Quotes to Scrape login/logout
│   └── test_case_7.py                 # Bonus: mobile device emulation
├── conftest.py                        # Shared fixtures and hooks
├── pytest.ini                         # Pytest + Playwright + report options
├── pyproject.toml / uv.lock           # Dependencies (locked)
├── Dockerfile / docker-compose.yml    # Containerisation
├── .pre-commit-config.yaml            # Ruff + hygiene hooks
└── reports/                           # Generated output (git-ignored)
    ├── report.html                    # pytest-html report
    ├── allure-results/                # raw Allure data
    ├── allure-report/                 # generated Allure site (after `allure generate`)
    └── test-results/                  # failure screenshots, videos, traces
```

`reports/` is deleted and recreated at the start of every run, so it only ever contains
results from the latest run.

## Test Case Coverage

| # | Test | What it verifies |
| --- | --- | --- |
| 1 | `test_home_page` | URL, title, all h1–h6 visible with non-empty text, books section visible with at least one book |
| 2 | `test_random_book_navigation` | 5 random books open the right details page: URL, H1 matches the title, info table visible, back navigation works |
| 3 | `test_book_data_consistency` | Homepage title and price match the details page for 5 random books |
| 4 | `test_no_broken_links` | All unique homepage hyperlinks return HTTP 200 (all broken links reported together) |
| 5 | `test_product_images_across_pages` | Images visible with non-empty `src`/`alt` and class `thumbnail`, across up to 5 pages via Next |
| 6 | `test_login_and_logout_link` | Login on Quotes to Scrape succeeds; Logout link is visible and enabled |

## Report Generation Guide

Every `pytest` run writes both reports automatically (configured in `pytest.ini`):

| Output | Path | Created by |
| --- | --- | --- |
| HTML report | `reports/report.html` | `pytest-html` |
| Allure raw results | `reports/allure-results/` | `allure-pytest` |
| Allure report (site) | `reports/allure-report/` | `allure generate` (manual locally, automatic in CI) |
| Screenshots, videos, traces | `reports/test-results/` | Playwright, kept only for failed tests |

## HTML Report Guide

1. Run `uv run pytest`.
2. Open `reports/report.html` in any browser. It is self-contained (`--self-contained-html`),
   so it works by double-click and can be emailed or downloaded from CI as is.
3. Use the summary at the top to filter passed/failed tests, and expand a row for the
   traceback and captured log output.

To open a failure trace from `reports/test-results/`:

```bash
uv run playwright show-trace reports/test-results/<test-folder>/trace.zip
```

## Allure Report Guide

Requires the Allure CLI (and Java). See [Installation Guide](#installation-guide).

```bash
# Option A: generate and open in your browser in one step
allure serve reports/allure-results

# Option B: generate a static site, then serve it
allure generate reports/allure-results --clean -o reports/allure-report
allure open reports/allure-report
```

> Do not open `reports/allure-report/index.html` by double-clicking. Browsers block the
> report's data requests on `file://`, so it appears blank. Always serve it with
> `allure open`, `allure serve`, or any local web server
> (`python -m http.server --directory reports/allure-report`).

In the report, tests are grouped by feature, steps are nested per book/image, the random
book selection appears as a test parameter, and failed tests include a screenshot.

## GitHub Actions Setup

The workflow is `.github/workflows/playwright.yml`.

**Triggers:** push to `main` every pull request, and manual runs
(*Actions → Playwright Tests → Run workflow*).

### Jobs

1. `test`: checkout, install uv and dependencies, install Chromium, run all tests, generate
   the Allure report, upload `reports/` as the `test-reports` artifact (HTML report, Allure
   results and report, screenshots, videos, traces), and package the Allure report for Pages.
   Report steps run even when tests fail.
2. `deploy-report`: publishes the Allure report to GitHub Pages (push events only, not pull
   requests). This job is non-blocking.

### Getting the reports

- Artifacts: open the workflow run and download **test-reports** from the *Artifacts* section.
  Serve the extracted `allure-report` folder over HTTP (see above), or open `report.html` directly.
- GitHub Pages: enable it once under *Settings → Pages → Source: GitHub Actions*.

## Design Decisions

- **Direct tests with fixtures, no Page Object Model.** Tests use Playwright locators
  directly, with setup and shared data pulled into fixtures (`books_home_page`,
  `quotes_home_page`, `random_book_indices`, `http_session`, `quotes_credentials`).
  Simple to read; the trade-off is some repeated locators (see Known Limitations).
- **Randomness:** each test gets its own generator seeded from the run seed and test ID.
- **Link checking over HTTP:** hrefs are collected in the browser and requested through a
  shared `requests.Session`, which is much faster than navigating to each URL. All failures
  are collected before asserting.
- **Titles from the `title` attribute:** the visible link text on the homepage is truncated
  (`A Light in the ...`), so full titles are read from the attribute.
- **Clean reports on every run:** `conftest.py` recreates `reports/` at session start.
- **Reproducible environment:** locked dependencies (`uv.lock`) and a Docker base image
  matching the locked Playwright version.

## Known Limitations

- Tests depend on the public sandbox sites being reachable. Slow or unavailable sites cause
  failures that are not product bugs.
- Without a Page Object Model, locators such as `article.product_pod` and `h3 a` are repeated
  across tests 2, 3; a markup change means editing several files.
- Test 4 only checks links found on the homepage and sends requests sequentially. External
  links (if any are added) are requested without browser context such as cookies.
- Tests 2 and 3 stop at the first failing book, so later selected books are not checked in
  that run.
- Test 6 only proves the login flow: the site accepts any credentials, so it cannot check
  rejection of wrong ones.
- Chromium is the default browser; other browsers need `playwright install` and `--browser`.
- The Allure report needs Java and the Allure CLI locally, and must be served over HTTP.
- The Docker base image tag has to be bumped together with the Playwright version.
