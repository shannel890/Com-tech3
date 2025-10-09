from playwright.sync_api import sync_playwright, expect

def run_verification(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Register a new user
        page.goto("http://127.0.0.1:5000/auth/register")
        page.wait_for_load_state('networkidle')
        page.get_by_placeholder("First Name").fill("Jules")
        page.get_by_placeholder("Last Name").fill("Test")
        page.get_by_placeholder("Email").fill("jules.test@example.com")
        page.get_by_placeholder("Password", exact=True).fill("password")
        page.get_by_placeholder("Confirm Password").fill("password")
        page.get_by_role("button", name="Register").click()

        # Log in
        page.goto("http://127.0.0.1:5000/auth/login")
        page.wait_for_load_state('networkidle')
        page.get_by_placeholder("Email").fill("jules.test@example.com")
        page.get_by_placeholder("Password", exact=True).fill("password")
        page.get_by_role("button", name="Login").click()
        expect(page).to_have_url("http://127.0.0.1:5000/dashboard/")

        # Create a new group
        page.wait_for_load_state('networkidle')
        page.get_by_role("link", name="Create New Group").click()
        page.wait_for_load_state('networkidle')
        page.get_by_placeholder("Group Name").fill("Test Group")
        page.get_by_placeholder("Description").fill("This is a test group.")
        page.get_by_role("button", name="Create Group").click()
        expect(page.locator("text=Test Group")).to_be_visible()

        # Navigate to group chat
        page.wait_for_load_state('networkidle')
        page.get_by_role("link", name="Chat").first.click()
        expect(page.locator("text=Test Group")).to_be_visible()

        # Send a message
        page.wait_for_load_state('networkidle')
        page.get_by_placeholder("Type your message...").fill("Hello, world!")
        page.get_by_role("button", name="Send").click()
        expect(page.locator("text=Hello, world!")).to_be_visible()

        # Go back to dashboard
        page.goto("http://127.0.0.1:5000/dashboard/")

        # Navigate to the call page
        page.get_by_role("link", name="Call").first.click()
        expect(page.locator("text=Group Call: Test Group")).to_be_visible()

        # Take a screenshot of the call page
        page.screenshot(path="jules-scratch/verification/verification.png")

    finally:
        browser.close()

with sync_playwright() as p:
    run_verification(p)