
import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from config import Config

"""
Writing the full end to end test case
"""

@pytest.mark.regression
def test_add_product_to_cart(page):
    """
    Automated Test Case: Verify user can search and add a product to the cart.
    """

    # --- Test Data ---
    product_name = Config.product_name      # Get product name from configuration file
    quantity = Config.product_quantity      # Get product quantity from configuration file

    # --- Page Object Initialization ---
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # --- Step 1: Search for a Product ---
    home_page.enter_product_name(product_name)
    home_page.click_search()

    # --- Step 2: Select the Product from Search Results ---
    product_page = search_results_page.select_product(product_name)

    # --- Step 3: Set Quantity and Add to Cart ---
    product_page.set_quantity(quantity)
    product_page.add_to_cart()

    # --- Step 4: Verify Confirmation Message ---
    # Ensure the success message appears within 3 seconds after adding the product
    expect(product_page.get_confirmation_message()).to_be_visible(timeout=3000)
