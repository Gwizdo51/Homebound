class Building:
    # parent class for all types of buildings
    # defines a basic building:
    # - costs nothing to build
    # - no power consumption / production
    # - no resource/item production
    # - no storage
    # - no assigned workers
    # - cannot upgrade
    # - can enable/disable

    def __init__(self, colony_data):
        if type(self) is Building:
            raise TypeError("The Building class should not be instanciated directly")
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
        # power
        # self.power = {
        #     "consumed": 0,
        #     "produced": 0
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
        # self.storage = {
        #     "power": 0,
        #     "food": 0,
        #     "water": 0,
        #     "oxygen": 0,
        #     "hydrogen": 0,
        #     "iron ore": 0,
        #     "iron": 0,
        #     "aluminium ore": 0,
        #     "aluminium": 0,
        #     "copper ore": 0,
        #     "copper": 0,
        #     "titanium ore": 0,
        #     "titanium": 0
        # }
        # assigned/maximum workers:
        # self.has_jobs = False
        # self.production_jobs = {
        #     "engineers": {
        #         "assigned": 0,
        #         "maximum": 0
        #     },
        #     "scientists": {
        #         "assigned": 0,
        #         "maximum": 0
        #     }
        # }
        # self.construction_jobs = {
        #     "engineers": {
        #         "assigned": 0,
        #         "maximum": 0
        #     },
        #     "scientists": {
        #         "assigned": 0,
        #         "maximum": 0
        #     }
        # }
        self.assigned_workers = {
            "construction": {
                "engineers": 0,
                "scientists": 0
            },
            "production": {
                "engineers": 0,
                "scientists": 0
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
        self.enabled = False

    @property
    def parameters(self):
        return self.parameters_per_level[self.level]

    @property
    def can_upgrade(self):
        return False

    def upgrade(self):
        # upgrade the building (+1 lvl)
        pass

    def assign_worker(self, add: bool, worker_type, work_type):
        # assign or unassign a worker to a job in this building
        pass

    def update(self, dt):
        # update the time required for upgrading
        # update the colony resources
        pass

    def enable(self):
        pass

    def disable(self):
        pass


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

    # parameters = {
    #     # "construction_costs": {
    #     #     0: {
    #     #         "iron": 0,
    #     #         "aluminium": 0,
    #     #         "copper": 0,
    #     #         "titanium": 0
    #     #     }
    #     # },
    #     "power": {
    #         1: {
    #             "consumed": 100,
    #             "produced": 100
    #         }
    #     },
    #     "has_production_jobs": False,
    #     # "jobs": {
    #     #     # 0: {
    #     #     #     "construction": {
    #     #     #         "engineers": 0,
    #     #     #         "scientists": 0
    #     #     #     }
    #     #     1: {
    #     #         ""
    #     #     }
    #     #     }
    #     "storage": {
    #         1: {
    #             "food": 50,
    #             "water": 50,
    #             "oxygen": 50,
    #             "hydrogen": 50,
    #             "iron ore": 250,
    #             "iron": 250,
    #             "aluminium ore": 250,
    #             "aluminium": 250,
    #             "copper ore": 250,
    #             "copper": 250,
    #             "titanium ore": 250,
    #             "titanium": 250
    #         }
    #     }
    # }

    parameters_per_level = {
        1: {
            "power": {
                "consumed": 100,
                "produced": 100
            },
            "storage": {
                "food": 50,
                "water": 50,
                "oxygen": 50,
                "hydrogen": 50,
                "iron ore": 250,
                "iron": 250,
                "aluminium ore": 250,
                "aluminium": 250,
                "copper ore": 250,
                "copper": 250,
                "titanium ore": 250,
                "titanium": 250
            },
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        }
    }

    def __init__(self, colony_data):
        super().__init__(colony_data)
        # headquarters are always at level 1
        self.level = 1
        self.is_constructing = False
        self.construction_percent = 100
        # assigned workers
        # self.assigned_jobs = {
        #     "engineers": 0,
        #     "scientists": 0
        # }
        # manufacture queue

    # @property
    # def parameters(self):
    #     return self.parameters_per_level[self.level]

    def upgrade(self):
        # can't upgrade headquarters
        pass

    def update(self, dt):
        # can't
        pass


class BuildingSolarPanels(Building):

    parameters = {
        0: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        1: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        2: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        3: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        }
    }

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
