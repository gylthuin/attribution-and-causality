import numpy as np
import matplotlib.pyplot as plt

# Basic Simulation of Game between Content Consumer (User) and Platform

def platform_select_items(inventory: list, subset_size: int, blacklist: set) -> np.array:
    presented_items = np.random.choice(inventory, subset_size, replace=False)

    while any([item in blacklist for item in presented_items]):
        presented_items = np.random.choice(inventory, subset_size, replace=False)
    
    return presented_items

def user_select_items(items: np.array, preferences: list, strategy: str, blacklist: set) -> int:
    strategies = {'fixed', 'uniform', 'strict'}

    if strategy not in strategies:
        raise Exception('Unknown strategy in user_select_actions')

    if all([item in blacklist for item in items]):
        raise Exception('No available item to select')
    
    if strategy == 'fixed':
        selected_position = 0

        while items[selected_position] in blacklist:
            selected_position += 1

    elif strategy == 'uniform':
        n = len(items)
        
        selected_position = np.random.randint(n)
        
        while items[selected_position] in blacklist:
            selected_position = np.random.randint(n)
    
    elif strategy == 'strict':
        items = sorted(items, key=lambda x: preferences[x])
        selected_position = 0

        while items[selected_position] in blacklist:
            selected_position += 1

    return items[selected_position]

def simulate(inventory_size: int, inventory_subset_size: int, num_user_interactions: int, num_users: int, user_strategy: str, user_has_memory: bool, initial_user_preference_strategy: str, platform_strategy: str, platform_has_memory: bool, plot_results: bool) -> np.array:
    inventory = list(range(inventory_size))
    selection_probabiliity = np.zeros((num_users, inventory_size))

    user_strategies = {'fixed', 'uniform', 'strict'}
    platform_strategies = {'uniform'}
    initial_user_preference_strategies = {'identical', 'uniform', 'clustered'}

    if user_strategy not in user_strategies or platform_strategy not in platform_strategies or initial_user_preference_strategy not in initial_user_preference_strategies:
        raise Exception('Unsupported simulation strategy')

    user_preferences = list(range(inventory_size))

    if user_has_memory or platform_has_memory:
        for user in range(num_users):
            user_item_blacklist = set()
            platform_item_blacklist = set()

            if initial_user_preference_strategy == 'uniform':
                np.random.shuffle(user_preferences)
            elif initial_user_preference_strategy == 'clustered':
                choices = np.random.choice(inventory_size, 2, False)
                user_preferences[choices[0]], user_preferences[choices[1]] = user_preferences[choices[1]], user_preferences[choices[0]]

            for _ in range(num_user_interactions):
                presented_items = platform_select_items(inventory, inventory_subset_size, platform_item_blacklist)
                selected_item = user_select_items(presented_items, user_preferences, user_strategy, user_item_blacklist)

                if user_has_memory:
                    user_item_blacklist.add(selected_item)
                
                if platform_has_memory:
                    platform_item_blacklist.add(selected_item)

                selection_probabiliity[user][selected_item] += 1/num_user_interactions
            
            if initial_user_preference_strategy == 'clustered':
                user_preferences[choices[0]], user_preferences[choices[1]] = user_preferences[choices[1]], user_preferences[choices[0]]

    else:
        for user in range(num_users):

            if initial_user_preference_strategy == 'uniform':
                np.random.shuffle(user_preferences)
            elif initial_user_preference_strategy == 'clustered':
                choices = np.random.choice(inventory_size, 2, False)
                user_preferences[choices[0]], user_preferences[choices[1]] = user_preferences[choices[1]], user_preferences[choices[0]]

            for _ in range(num_user_interactions):
                presented_items = platform_select_items(inventory, inventory_subset_size, set())
                selected_item = user_select_items(presented_items, user_preferences, user_strategy, set())

                selection_probabiliity[user][selected_item] += 1/num_user_interactions

            if initial_user_preference_strategy == 'clustered':
                user_preferences[choices[0]], user_preferences[choices[1]] = user_preferences[choices[1]], user_preferences[choices[0]]

    if plot_results:
        plt.bar(list(range(inventory_size)), np.mean(selection_probabiliity, axis=0))
        plt.show()
    
    return selection_probabiliity

# """
# Assumptions:
# - Platform selects subsets of items uniformly
# - User always selects first action, and is therefore oblivious to the content or past interactions
# - All Users follow identical selection strategies to one another
# """

# simulate(10000, 8, 100, 100, 'fixed', False, 'identical', 'uniform', False, True)

# """
# Assumptions:
# - Platform selects subsets of items uniformly
# - User always selects actions uniformly, independent of the content or past interactions
# - All Users follow identical selection strategies to one another
# """

# simulate(10000, 8, 100, 100, 'uniform', False, 'identical', 'uniform', False, True)

# """
# Assumptions:
# - Platform selects subsets of items uniformly
# - User always selects actions uniformly, but will not select an action that they have already selected in previous interactions
# - All Users follow identical selection strategies to one another
# """

# simulate(10000, 8, 100, 100, 'uniform', True, 'identical', 'uniform', False, True)

# """
# Assumptions:
# - Platform selects subsets of items uniformly, but only from the subset of items that the User hasn't selected before
# - User always selects actions uniformly
# - All Users follow identical selection strategies to one another
# """

# simulate(10000, 8, 100, 100, 'uniform', False, 'identical', 'uniform', True, True)

# """
# Assumptions:
# - Platform selects subsets of items uniformly, but only from the subset of items that the User hasn't selected before
# - User always selects actions uniformly, but will not select an action that they have already selected in previous interactions
# - All Users follow identical selection strategies to one another
# """

# simulate(10000, 8, 100, 100, 'uniform', True, 'identical', 'uniform', True, True)

# """
# Assumptions:
# - Platform selects subsets of items uniformly
# - User always selects items based on strict monotonic preferences (always selects the lowest item)
# - All Users follow identical selection strategies to one another
# """

# simulate(10000, 8, 100, 100, 'strict', False, 'identical', 'uniform', False, True)

# """
# Assumptions:
# - Platform selects subsets of items uniformly
# - User always selects items based on strict monotonic preferences (always selects the lowest item) but does not select the same item twice
# - All Users follow identical selection strategies to one another
# """

# simulate(10000, 8, 100, 100, 'strict', True, 'identical', 'uniform', False, True)

# """
# Assumptions:
# - Platform selects subsets of items uniformly, but only from the subset of items that the User hasn't selected before
# - User always selects items based on strict monotonic preferences (always selects the lowest item) but does not select the same item twice
# - All Users follow identical selection strategies to one another
# """

# simulate(10000, 8, 100, 100, 'strict', True, 'identical', 'uniform', True, True)

# """
# Assumptions:
# - Platform selects subsets of items uniformly, but only from the subset of items that the User hasn't selected before
# - User always selects items based on strict preferences but does not select the same item twice
# - All Users follow identical selection strategies to one another, but with different preferences. The preferences are uniformly distributed.
# """

# simulate(10000, 8, 100, 100, 'strict', True, 'uniform', 'uniform', True, True)

# """
# Assumptions:
# - Platform selects subsets of items uniformly, but only from the subset of items that the User hasn't selected before
# - User always selects items based on strict preferences but does not select the same item twice
# - All Users follow identical selection strategies to one another, but with different preferences. The preferences are clustered together.
# """

simulate(10000, 8, 100, 100, 'strict', True, 'clustered', 'uniform', True, True)
