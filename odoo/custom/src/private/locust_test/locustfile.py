# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from locust import HttpUser, between, task


class OdooUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def on_start(self):
        # Perform login
        self.client.post(
            "/web/session/authenticate",
            json={
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "db": "prod-SIT-test",
                    "login": "admin@egov.or.th",
                    "password": "1234",
                },
            },
            name="Login",
        )

    @task
    def create_pr(self):
        # Create PR
        data = {
            "jsonrpc": "2.0",
            "params": {
                "model": "purchase.request",
                "vals": {
                    "procurement_type_id": 1,  # ซื้อ/จ้าง/เช่า
                    "procurement_method_id": 1,  # เฉพาะเจาะจง
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "product_id": 5,  # ซื้อ/จ้าง/เช่า
                                "activity_id": 1,
                                "estimated_cost": 100.0,
                                "product_qty": 1,
                                "analytic_account_id": 1,
                            },
                        )
                    ],
                },
            },
        }
        # Send the request to create the PR until approved
        self.client.post("/create_pr", json=data, name="Create PR")

    @task
    def create_ex(self):
        # Create EX
        data = {
            "jsonrpc": "2.0",
            "params": {
                "model": "hr.expense.sheet",
                "vals": {
                    "name": "EX Test",
                    "pr_for": "expense",
                    "expense_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "EX#1",
                                "product_id": 1,
                                "unit_amount": 100.0,
                                "analytic_account_id": 1,
                            },
                        )
                    ],
                },
            },
        }
        # Send the request to create the EX until approved
        self.client.post("/create_ex", json=data, name="Create EX")
