from src.infer.infer_activities import InferActivities


class Inference:
    def __init__(self, paths: dict):
        self.paths = paths

    def infer(self):
        """
        infer all sections and return a dictionary of inferred
        """
        inferred = {}
        inferred["activities"] = InferActivities(self.paths["activities"]).infer()
        ...
        return inferred
