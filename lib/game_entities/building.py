class Building:
    # parent class for all types of buildings

    def __init__(self):
        # assigned workers
        # power consumption
        # resource consumption
        # resource prodution
        # resources required for next upgrade
        pass

    def upgrade(self):
        # upgrade the building (+1 lvl)
        raise NotImplementedError

    def update(self, dt):
        # update the time required for upgrading
        raise NotImplementedError


class HeadQuarters(Building):
    # implements the Building class

    def __init__(self):
        # max amount of workers
        # resources necessary to upgrade
        pass

    def upgrade(self):
        pass

    def update(self, dt):
        pass


class PowerGenerator(Building):
    pass
