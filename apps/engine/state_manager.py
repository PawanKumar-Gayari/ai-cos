"""
Pipeline state manager.
"""

from datetime import datetime


class StateManager:

    def __init__(self):

        self.state = {
            "status": "pending",
            "current_step": None,
            "started_at": None,
            "completed_at": None,
            "data": {},
            "errors": [],
        }

    def start_pipeline(self):

        self.state["status"] = "running"

        self.state["started_at"] = str(datetime.utcnow())

    def complete_pipeline(self):

        self.state["status"] = "completed"

        self.state["completed_at"] = str(datetime.utcnow())

    def fail_pipeline(self, error):

        self.state["status"] = "failed"

        self.state["errors"].append(str(error))

    def set_step(self, step):

        self.state["current_step"] = step

    def update_data(self, key, value):

        self.state["data"][key] = value

    def get_state(self):

        return self.state