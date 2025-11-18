# tests/e2e/conftest.py
import os
import pytest

pytest_plugins = (
    "pytest_django",
    "pytest_playwright",
)

@pytest.fixture(scope="session", autouse=True)
def _allow_sync_in_async():
    os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "artifacts/videos",
        "viewport": {"width": 1280, "height": 800},
    }


@pytest.fixture(autouse=True)
def screenshot_on_failure(page, request):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        page.screenshot(
            path=f"artifacts/screenshots/{request.node.name}.png"
        )
