from typing import Any


class Building:
    # parent class for all types of buildings
    # defines a basic building:
    # - can assign/remove workers
    # - can enable/disable
    # - can build and upgrade

    parameters_per_level: dict[int, Any]

    def __init__(self, colony_data: dict[str]):
        if type(self) is Building:
            raise TypeError("The Building class should not be instanciated directly")
        self.colony_data = colony_data
        # building level
        # 0: not built
        # 1, 2, 3: current building level
        self.level = 0
        self.level_max = 3
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
        self.construction_workload_completed = 0
        # flags
        self.enabled = True

    @property
    def parameters(self) -> dict[str, Any]:
        return self.parameters_per_level[self.level]

    # @property
    # def can_construct(self):
    #     return False

    def can_upgrade(self) -> bool:
        # checks if building/upgrading is possible
        # construction is possible if every required resource is available in the colony
        if self.level == self.level_max or self.is_constructing:
            construction_possible = False
        else:
            construction_possible = True
            for resource_name in self.parameters["construction_costs"].keys():
                if self.colony_data["resources"][resource_name] < self.parameters["constuction_costs"][resource_name]:
                    construction_possible = False
                    break
        return construction_possible

    def upgrade(self):
        # upgrade the building (+1 lvl)
        # only called when upgrade is possible
        self.is_constructing = True
        self.construction_workload_completed = 0
        # remove every required construction resources from the colony resources
        for resource_name in self.parameters["construction_costs"].keys():
            self.colony_data["resources"][resource_name] -= self.parameters["constuction_costs"][resource_name]

    def can_assign_worker(self, add: bool, job_type: str, worker_type: str) -> bool:
        assignment_possible = False
        if add:
            # if there are vacant jobs in the building ...
            if self.assigned_workers[job_type][worker_type] < self.parameters["jobs"][job_type][worker_type]:
                # if there are available workers ...
                if self.colony_data["workers"][worker_type]["available"] > 0:
                    assignment_possible = True
        else:
            # if there are assigned workers ...
            if self.assigned_workers[job_type][worker_type] > 0:
                assignment_possible = True
        return assignment_possible

    def assign_worker(self, add: bool, job_type: str, worker_type: str, all: bool = False):
        # assign / unassign a job to a worker in this building
        # assign / unassign all of them if "all" is True
        # only called when assignment / unassignment is possible
        # work_type = "construction" or "production"
        # job_type = "engineers" or "scientists"
        if add:
            if all:
                # fill as many vacant jobs as possible
                available_jobs = self.parameters["jobs"][job_type][worker_type] - self.assigned_workers[job_type][worker_type]
                workers_to_assign = min(available_jobs, self.colony_data["workers"][worker_type]["available"])
                self.colony_data["workers"][worker_type]["available"] -= workers_to_assign
                self.assigned_workers[job_type][worker_type] += workers_to_assign
            else:
                # assign a worker to the job
                # remove an available worker from the colony
                self.colony_data["workers"][worker_type]["available"] -= 1
                # add the worker to the job
                self.assigned_workers[job_type][worker_type] += 1
        else:
            if all:
                # remove all workers
                self.colony_data["workers"][worker_type]["available"] += self.assigned_workers[job_type][worker_type]
                self.assigned_workers[job_type][worker_type] = 0
            else:
                # add an available worker to the colony
                self.colony_data["workers"][worker_type]["available"] += 1
                # remove a worker from the job
                self.assigned_workers[job_type][worker_type] -= 1

    def remove_all_workers(self):
        self.assign_worker(add=False, job_type="engineers", work_type="construction", all=True)
        self.assign_worker(add=False, job_type="engineers", work_type="production", all=True)
        # no scientists can work in a construction job
        # self.assign_worker(add=False, job_type="scientists", work_type="construction", all=True)
        self.assign_worker(add=False, job_type="scientists", work_type="production", all=True)

    def can_use_power_switch(self) -> bool:
        # whether the building can be turned on/off
        return False

    def use_power_switch(self):
        # only used if building can be turned on/off
        if self.enabled:
            # fire every worker from the production jobs
            self.assign_worker(add=False, job_type="engineers", work_type="production", all=True)
            self.assign_worker(add=False, job_type="scientists", work_type="production", all=True)
        self.enabled = not self.enabled

    def update(self, dt):
        # update construction status
        if self.is_constructing:
            # every assigned worker at the "construction" job makes 1 construction workload per second
            self.construction_workload_completed += self.assigned_workers["construction"]["engineers"] * dt
            # check if construction is finished
            if self.construction_workload_completed >= self.parameters["construction_workload"]:
                # stop the construction
                self.is_constructing = False
                # upgrade the building
                self.level += 1
                # fire every worker at the construction jobs
                self.assign_worker(add=False, job_type="engineers", work_type="construction", all=True)


class BuildingHeadQuarters(Building):

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

    def __init__(self, colony_data: dict[str]):
        super().__init__(colony_data)
        # headquarters are always at level 1
        self.level = 1
        self.level_max = 1
        self.is_constructing = False
        # assigned workers
        # self.assigned_jobs = {
        #     "engineers": 0,
        #     "scientists": 0
        # }
        # manufacture queue

    # @property
    # def parameters(self):
    #     return self.parameters_per_level[self.level]

    # def can_construct(self):
    #     # cannot build or upgrade the headquarters
    #     return False

    # def upgrade(self):
    #     # can't upgrade headquarters
    #     pass

    # def update(self, dt):
    #     # super().update(dt)
    #     pass


class BuildingSolarPanels(Building):

    parameters_per_level = {
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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

    # def __init__(self, colony_data):
    #     super().__init__(colony_data)

    # @property
    # def can_construct(self):
    #     # checks if building/upgrading is possible
    #     # construction is possible if every required resource is available in the colony
    #     if self.level < 3:
    #         construction_possible = True
    #         for resource in self.parameters[]
    #     else:
    #         construction_possible = False
    #     return construction_possible

    # def upgrade(self):
    #     pass

    # def update(self, dt):
    #     super().update(dt)

    def can_use_power_switch(self):
        # can only be turned off if the power it produces isn't used in the colony -> check at the colony level
        return True


class BuildingDrillingStation(Building):

    parameters_per_level = {
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
            "construction_workload": 0,
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
            },
            "production_speed": 1
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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

    def __init__(self, colony_data: dict[str]):
        super().__init__(colony_data)
        # self.resource_produced = "water", "iron ore", "aluminium ore", "copper ore" or "titanium ore"
        self.resource_produced = None

    def produce(self, resource_type: str):
        self.resource_produced = resource_type


class BuildingWarehouse(Building):

    parameters_per_level = {
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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


class BuildingLiquidTank(Building):

    parameters_per_level = {
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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


class BuildingElectrolysisStation(Building):

    parameters_per_level = {
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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


class BuildingFurnace(Building):

    parameters_per_level = {
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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


class BuildingSchool(Building):

    parameters_per_level = {
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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


class BuildingGreenhouse(Building):

    parameters_per_level = {
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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


class BuildingFactory(Building):
    parameters_per_level = {
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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


class BuildingSpaceport(Building):
    parameters_per_level = {
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
            "construction_workload": 0,
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
            "construction_workload": 0,
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


class BuildingResearchLabs(Building):
    # forget for now
    pass
