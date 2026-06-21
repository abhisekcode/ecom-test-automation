"""One-off DB provisioning script run by CI before the test job."""

from utils.db_utils import create_cart_table

if __name__ == "__main__":
    create_cart_table()
    print("Database setup completed.")
