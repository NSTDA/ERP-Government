from locust import HttpUser, task


class MyLocust(HttpUser):
    @task
    def on_start(self):
        # Login to Odoo
        self.client.post(
            "/web/session/authenticate",
            json={
                "jsonrpc": "2.0",
                "method": "call",
                "params": {"db": "prod-test", "login": "ba", "password": "1234"},
            },
            name="Login",
        )

    @task
    def view_product(self):
        # View all products
        self.client.get(
            "/web/dataset/search_read",
            json={
                "jsonrpc": "2.0",
                "params": {
                    "model": "product.product",
                    "domain": [],
                    "fields": ["name", "list_price"],
                    "offset": 0,
                    "limit": 80,
                },
            },
            name="View Product",
        )

    @task
    def view_budget_control(self):
        # View all products
        self.client.get(
            "/web/dataset/search_read",
            json={
                "jsonrpc": "2.0",
                "params": {
                    "model": "budget.control",
                    "domain": [],
                    "fields": ["name", "analytic_account_id", "budget_period"],
                    "offset": 0,
                    "limit": 80,
                },
            },
            name="View Budget Control",
        )

    @task
    def create_product(self):
        # Create new product
        self.client.post(
            "/web/dataset/call_kw",
            json={
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "model": "product.template",
                    "method": "create",
                    "args": [
                        {
                            "name": "Test Product",
                            "type": "product",
                            "list_price": 100.0,
                            "standard_price": 50.0,
                        }
                    ],
                },
            },
            name="Create Product",
        )

    @task
    def create_analytic_account(self):
        # Create new analytic account
        self.client.post(
            "/web/dataset/call_kw",
            json={
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "model": "account.analytic.account",
                    "method": "create",
                    "args": [
                        {
                            "name": "Test Analytic",
                        }
                    ],
                },
            },
            name="Create Analytic Account",
        )
