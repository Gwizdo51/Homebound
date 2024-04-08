class Building:
    # parent class for all types of buildings
    # defines a basic building:
    # - costs nothing to build
    # - no power consumption
    # - no resource/item production
    # - no storage
    # - no assigned workers
    # - cannot upgrade
    # - can enable/disable

    def __init__(self, colony_data):
        self.colony_data = colony_data
        # construction costs
        # self.construction_cost = {
        #     "iron": 0,
        #     "aluminium": 0,
        #     "copper": 0,
        #     "titanium": 0
        # }
        # building level
        # 0: not built
        # 1, 2, 3: current building level
        self.level = 0
        # resource consumption
        # self.resource_consumption = {
        #     "power": 0,
        #     "water": 0
        # }
        # resources required for upgrades
        # self.upgrade_costs = {
        #     1: {
        #         "iron": 0,
        #         "aluminium": 0,
        #         "copper": 0,
        #         "titanium": 0
        #     },
        #     2: {
        #         "iron": 0,
        #         "aluminium": 0,
        #         "copper": 0,
        #         "titanium": 0
        #     }
        # }
        # storage
        self.storage = {
            "power": 0,
            "food": 0,
            "water": 0,
            "oxygen": 0,
            "hydrogen": 0,
            "iron ore": 0,
            "iron": 0,
            "aluminium ore": 0,
            "aluminium": 0,
            "copper ore": 0,
            "copper": 0,
            "titanium ore": 0,
            "titanium": 0
        }
        # assigned/maximum workers:
        self.has_jobs = False
        self.production_jobs = {
            "engineers": {
                "assigned": 0,
                "maximum": 0
            },
            "scientists": {
                "assigned": 0,
                "maximum": 0
            }
        }
        self.construction_jobs = {
            "engineers": {
                "assigned": 0,
                "maximum": 0
            },
            "scientists": {
                "assigned": 0,
                "maximum": 0
            }
        }
        # construction/upgrade timer
        self.is_constructing = True
        self.construction_percent = 0
        # production type:
        # 0: doesn't produce
        # 1: produces continuously
        # 2: produces by cycle
        # self.production_type = 0
        # flags
        self.enabled = True

    @property
    def can_upgrade(self):
        return False

    def upgrade(self):
        # upgrade the building (+1 lvl)
        raise NotImplementedError

    def assign_worker(self, add: bool, worker_type, work_type):
        # assign or unassign a worker to a job in this building
        pass

    def update(self, dt):
        # update the time required for upgrading
        # update the colony resources
        raise NotImplementedError


class BuildingHeadQuarters(Building):
    # implements the Building class

    # cannot be constructed or upgraded
    # construction_cost = {
    #     0: {
    #         "iron": 0,
    #         "aluminium": 0,
    #         "copper": 0,
    #         "titanium": 0
    #     },
    #     1: {
    #         "iron": 0,
    #         "aluminium": 0,
    #         "copper": 0,
    #         "titanium": 0
    #     },
    #     2: {
    #         "iron": 0,
    #         "aluminium": 0,
    #         "copper": 0,
    #         "titanium": 0
    #     }
    # }

    def __init__(self, colony_data):
        super().__init__(colony_data)
        # max amount of workers
        # assigned workers
        # resources necessary to upgrade
        # manufacture queue

    def upgrade(self):
        pass

    def update(self, dt):
        pass


class BuildingSolarPanels(Building):

    def __init__(self, colony_data):
        super().__init__(colony_data)

    def upgrade(self):
        pass

    def update(self, dt):
        pass


class BuildingDrillingStation(Building):
    pass


class BuildingWarehouse(Building):
    pass


class BuildingLiquidTank(Building):
    pass


class BuildingElectrolysisStation(Building):
    pass


class BuildingFurnace(Building):
    pass


class BuildingSchool(Building):
    pass


class BuildingGreenhouse(Building):
    pass


class BuildingFactory(Building):
    pass


class BuildingSpaceport(Building):
    pass


class BuildingResearchLabs(Building):
    # forget for now
    pass
