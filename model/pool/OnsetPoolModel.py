class OnsetPoolModel:
    def __init__(self):
        self.items = {}

    def add(
        self,
        onset_data,
        parent_song,
        parent_filter_name=None,
        pool_number=None,
        name=None,
    ):
        if pool_number is not None:
            if pool_number in self.items:
                raise ValueError(
                    f"An item with pool_number {pool_number} already exists."
                )
        else:
            if self.items:
                highest_pool_number = max([int(key) for key in self.items.keys()])
                pool_number = highest_pool_number + 1
            else:
                pool_number = 1
        if name is None:
            name = "onset_" + str(pool_number)
            print(f"initializing with default name {name}")
        key = str(pool_number)
        self.items[key] = onset_pool_item(
            name, onset_data, parent_song, parent_filter_name
        )


class onset_pool_item:
    def __init__(self, name, onset_data, parent_song, parent_filter_name):
        self.name = name
        self.onset_data = onset_data
        self.parent_song = parent_song
        self.parent_filter_name = parent_filter_name
