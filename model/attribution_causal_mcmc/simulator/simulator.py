from typing import List
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt

# Basic Simulation of Game between Content Consumer (User) and Platform


class UserSelectionStrategy(Enum):
    FIXED = 1,
    UNIFORM = 2,
    STRICT = 3


class PlatformSelectionStrategy(Enum):
    UNIFORM = 1,


class InitialUserPreferenceStrategy(Enum):
    IDENTICAL = 1,
    UNIFORM = 2,


class User:
    def __init__(self, inventory_size: int, strategy: UserSelectionStrategy, update_blacklist: bool, initial_preferences: np.array, initial_blacklist: set):
        self.preferences = initial_preferences or np.array(range(inventory_size))
        self.update_blacklist = update_blacklist
        self.blacklist = initial_blacklist
        self._selection_history = []
        self._selection_frequency = np.zeros(inventory_size)

        if strategy == UserSelectionStrategy.FIXED:
            self.selection_strategy = self._fixed_strategy
        elif strategy == UserSelectionStrategy.UNIFORM:
            self.selection_strategy = self._uniform_strategy
        elif strategy == UserSelectionStrategy.STRICT:
            self.selection_strategy = self._strict_strategy

    def select_item(self, items: np.array) -> int:
        if all([item in self.blacklist for item in items]):
            return -1

        selection = self.selection_strategy(items)

        self._selection_frequency[selection] += 1
        self._selection_history.append(selection)

        if self.update_blacklist:
            self.blacklist.add(selection)

        return selection

    @property
    def selection_history(self):
        return self._selection_history

    @property
    def selection_frequency(self):
        return self._selection_frequency

    def _fixed_strategy(self, items: np.array) -> int:
        selected_position = 0

        while items[selected_position] in self.blacklist:
            selected_position += 1

        return items[selected_position]

    def _uniform_strategy(self, items: np.array) -> int:
        k = len(items)

        selected_position = np.random.randint(k)

        while items[selected_position] in self.blacklist:
            selected_position = np.random.randint(k)

        return items[selected_position]

    def _strict_strategy(self, items: np.array) -> int:
        selected_position = 0

        items = sorted(items, key=lambda x: self.preferences[x])

        while items[selected_position] in self.blacklist:
            selected_position += 1

        return items[selected_position]


class Platform:
    def __init__(self, inventory_size: int, presentation_size: int, strategy: PlatformSelectionStrategy, update_blacklist: bool):
        self.inventory = list(range(inventory_size))
        self.blacklist = [set()]

        self.presentation_size = presentation_size
        self.update_blacklist = update_blacklist

        if strategy == PlatformSelectionStrategy.UNIFORM:
            self.selection_strategy = self._uniform_strategy

    def add_user(self):
        self.blacklist.append(set())

    def add_item_to_user_blacklist(self, item: int, user_id: int):
        if self.update_blacklist:
            self.blacklist[user_id].add(item)

    def select_items_for_user(self, user_id: int) -> np.array:
        return self.selection_strategy(user_id)

    def _uniform_strategy(self, user_id: int) -> np.array:
        presented_items = np.random.choice(self.inventory, self.presentation_size, replace=False)

        while all([item in self.blacklist[user_id] for item in presented_items]):
            presented_items = np.random.choice(self.inventory, self.presentation_size, replace=False)
        return presented_items


class Simulator:
    def __init__(self,
                 inventory_size: int,
                 presentation_size: int,
                 num_users: int,
                 user_strategy:  UserSelectionStrategy,
                 user_has_blacklist: bool,
                 platform_strategy: PlatformSelectionStrategy,
                 platform_has_blacklist: bool,
                 initial_user_preference_strategy: InitialUserPreferenceStrategy):
        self.inventory_size = inventory_size
        self.num_users = num_users

        if initial_user_preference_strategy == InitialUserPreferenceStrategy.IDENTICAL:
            self.initial_user_preference_strategy = self._identical_initial_user_preference_strategy
        elif initial_user_preference_strategy == InitialUserPreferenceStrategy.UNIFORM:
            self.initial_user_preference_strategy = self._uniform_user_preference_strategy

        self.users = [User(inventory_size, user_strategy, user_has_blacklist, self.initial_user_preference_strategy()[user], set()) for user in range(self.num_users)]

        self.platform = Platform(inventory_size, presentation_size, platform_strategy, platform_has_blacklist)
        for _ in range(self.num_users):
            self.platform.add_user()

    def simulate(self, num_user_interactions: int) -> np.array:
        total_selection_frequency = np.zeros(self.inventory_size)
        for user in range(self.num_users):
            for _ in range(num_user_interactions):
                presented_items = self.platform.select_items_for_user(user)
                selected_item = self.users[user].select_item(presented_items)

                self.platform.add_item_to_user_blacklist(selected_item, user)

            total_selection_frequency += self.users[user].selection_frequency
        return total_selection_frequency

        np.random.shuffle(user_preferences)

        return [user_preferences.copy() for _ in range(self.num_users)]

    def _uniform_user_preference_strategy(self) -> List[np.array]:
        user_preferences = [list(range(self.inventory_size)) for _ in range(self.num_users)]
        for user in range(self.num_users):
            np.random.shuffle(user_preferences[user])
        return user_preferences

# """
# Assumptions:
# - Platform selects subsets of items uniformly
# - User always selects first action, and is therefore oblivious to the content or past interactions
# - All Users follow identical selection strategies to one another
# """

# simulator = Simulator(10000, 8, 100, UserSelectionStrategy.FIXED, False, PlatformSelectionStrategy.UNIFORM, False, InitialUserPreferenceStrategy.IDENTICAL)

# """
# Assumptions:
# - Platform selects subsets of items uniformly
# - User always selects actions uniformly, independent of the content or past interactions
# - All Users follow identical selection strategies to one another
# """

# simulate(10000, 8, 10    def _identical_initial_user_preference_strategy(self) -> List[np.array]:
        user_preferences = list(range(self.inventory_size))0, 100, 'uniform', False, 'identical', 'uniform', False, True)
# simulator = Simulator(10000, 8, 100, UserSelectionStrategy.UNIFORM, False, PlatformSelectionStrategy.UNIFORM, False, InitialUserPreferenceStrategy.IDENTICAL)

# """
# Assumptions:
# - Platform selects subsets of items uniformly
# - User always selects actions uniformly, but will not select an action that they have already selected in previous interactions
# - All Users follow identical selection strategies to one another
# """

# simulator = Simulator(10000, 8, 100, UserSelectionStrategy.UNIFORM, True, PlatformSelectionStrategy.UNIFORM, False, InitialUserPreferenceStrategy.IDENTICAL)

# """
# Assumptions:
# - Platform selects subsets of items uniformly, but only from the subset of items that the User hasn't selected before
# - User always selects actions uniformly
# - All Users follow identical selection strategies to one another
# """

# simulator = Simulator(10000, 8, 100, UserSelectionStrategy.UNIFORM, True, PlatformSelectionStrategy.UNIFORM, True, InitialUserPreferenceStrategy.IDENTICAL)

# """
# Assumptions:
# - Platform selects subsets of items uniformly
# - User always selects items based on strict monotonic preferences (always selects the lowest item)
# - All Users follow identical selection strategies to one another
# """

# simulator = Simulator(10000, 8, 100, UserSelectionStrategy.STRICT, False, PlatformSelectionStrategy.UNIFORM, False, InitialUserPreferenceStrategy.IDENTICAL)

# """
# Assumptions:
# - Platform selects subsets of items uniformly
# - User always selects items based on strict monotonic preferences (always selects the lowest item) but does not select the same item twice
# - All Users follow identical selection strategies to one another
# """

# simulator = Simulator(10000, 8, 100, UserSelectionStrategy.STRICT, True, PlatformSelectionStrategy.UNIFORM, False, InitialUserPreferenceStrategy.IDENTICAL)

# """
# Assumptions:
# - Platform selects subsets of items uniformly, but only from the subset of items that the User hasn't selected before
# - User always selects items based on strict monotonic preferences (always selects the lowest item) but does not select the same item twice
# - All Users follow identical selection strategies to one another
# """

# simulator = Simulator(10000, 8, 100, UserSelectionStrategy.STRICT, True, PlatformSelectionStrategy.UNIFORM, True, InitialUserPreferenceStrategy.IDENTICAL)

# """
# Assumptions:
# - Platform selects subsets of items uniformly, but only from the subset of items that the User hasn't selected before
# - User always selects items based on strict preferences but does not select the same item twice
# - All Users follow identical selection strategies to one another, but with different preferences. The preferences are uniformly distributed.
# """

simulator = Simulator(10000, 8, 100, UserSelectionStrategy.STRICT, True, PlatformSelectionStrategy.UNIFORM, True, InitialUserPreferenceStrategy.UNIFORM)


total_selection_frequency = simulator.simulate(100)


plt.bar(list(range(10000)), total_selection_frequency)
plt.show()
