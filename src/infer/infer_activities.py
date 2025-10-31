import os


class InferActivities:
    def __init__(self, activities_path: str):
        self.activities_path = activities_path
        self.activities = self.load_activities()

    def load_activities(self) -> list:
        with open(self.activities_path, "r", encoding="utf-8") as file:
            return file.read()

    def infer(self) -> dict:
        """
        infer activity information and return as dict

        returns: dict({"name": str, "items": list of str, "hrefs": list of str})
        """
        pass
