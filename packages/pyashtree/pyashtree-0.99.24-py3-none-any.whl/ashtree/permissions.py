from typing import Dict, List, Iterable


class PermissionManager:

    actions: Dict[str, int]
    numeric: Dict[int, str]

    def __init__(self):
        self.actions = {}
        self.numeric = {}

    def setup_actions(self, actions: Iterable[str]):
        actions = sorted(actions)
        self.actions = {}
        self.numeric = {}
        for idx, action in enumerate(actions):
            self.actions[action] = 2**idx
            self.numeric[2**idx] = action

    def add_action(self, action: str):
        if action not in self.actions:
            actions = set(self.actions.keys())
            actions.add(action)
            self.setup_actions(actions)

    def from_numeric(self, grants: int) -> List[str]:
        actions = []
        bin_grants = bin(grants)[2:]
        for idx, check in enumerate(reversed(bin_grants)):
            if check == "1":
                action_numeric = self.numeric.get(2**idx)
                if action_numeric is not None:
                    actions.append(action_numeric)
        return actions

    def to_numeric(self, grants: Iterable[str]) -> int:
        numeric = 0
        for action in grants:
            action_numeric = self.actions.get(action, 0)
            numeric = numeric | action_numeric
        return numeric

    def check(self, grants: int, required: Iterable[str] | int):
        if isinstance(required, int):
            bin_required = required
        else:
            bin_required = self.to_numeric(required)

        return grants & bin_required == bin_required


pm = PermissionManager()
