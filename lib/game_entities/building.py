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
        self.can_disable = True

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

    # def can_use_power_switch(self) -> bool:
    #     # whether the building can be turned on/off
    #     return False

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
        self.can_disable = False
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

    def __init__(self, colony_data):
        super().__init__(colony_data)
        self.can_disable = False

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

    # def can_use_power_switch(self):
    #     # can only be turned off if the power it produces isn't used in the colony -> check at the colony level
    #     return True


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
            },
            "production_speed": 1
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
            },
            "production_speed": 1
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
            },
            "production_speed": 1
        }
    }

    def __init__(self, colony_data):
        super().__init__(colony_data)
        # self.resource_produced = "water", "iron ore", "aluminium ore", "copper ore" or "titanium ore"
        self.resource_produced = None

    def produce(self, resource_type: str):
        self.resource_produced = resource_type

    def update(self, dt):
        super().update(dt)
        # dump the produced resources into the colony resource buffer
        # only produce if enabled, at least level 1, and a resource to produce has been selected
        if self.enabled and (self.level > 0) and (self.resource_produced is not None):
            self.colony_data["resources_buffer"][self.resource_produced] += dt \
                * (self.assigned_workers["production"]["engineers"] + self.assigned_workers["production"]["scientists"]) \
                * self.parameters["production_speed"] * self.colony_data["production_factors"][self.resource_produced]


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
            "storage": {
                "food": 0,
                "iron ore": 0,
                "iron": 0,
                "aluminium ore": 0,
                "aluminium": 0,
                "copper ore": 0,
                "copper": 0,
                "titanium ore": 0,
                "titanium": 0
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
            "storage": {
                "food": 0,
                "iron ore": 0,
                "iron": 0,
                "aluminium ore": 0,
                "aluminium": 0,
                "copper ore": 0,
                "copper": 0,
                "titanium ore": 0,
                "titanium": 0
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
        },
        3: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": {
                "food": 0,
                "iron ore": 0,
                "iron": 0,
                "aluminium ore": 0,
                "aluminium": 0,
                "copper ore": 0,
                "copper": 0,
                "titanium ore": 0,
                "titanium": 0
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
        self.can_disable = False


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
            "storage": {
                "water": 0,
                "oxygen": 0,
                "hydrogen": 0
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
            "storage": {
                "water": 0,
                "oxygen": 0,
                "hydrogen": 0
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
        },
        3: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": {
                "water": 0,
                "oxygen": 0,
                "hydrogen": 0
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
        self.can_disable = False


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
            },
            "production_speed": 1
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
            },
            "production_speed": 1
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
            },
            "production_speed": 1
        }
    }

    def update(self, dt):
        super().update(dt)
        # dump the produced resources into the colony resource buffer
        # only produce if enabled and at least level 1
        if self.enabled and (self.level > 0):
            # consume water
            water_required_from_storage = dt * self.parameters["production_speed"] \
                * (self.assigned_workers["production"]["engineers"] + self.assigned_workers["production"]["scientists"])
            water_obtained = min(water_required_from_storage, self.colony_data["resources"]["water"])
            self.colony_data["resources"]["water"] -= water_obtained
            # produce oxygen
            self.colony_data["resources_buffer"]["oxygen"] += water_obtained * (1/2)
            # produce hydrogen
            self.colony_data["resources_buffer"]["hydrogen"] += water_obtained * 1


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
            },
            "production_speed": 1,
            "production_per_cycle": 1
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
            },
            "production_speed": 1,
            "production_per_cycle": 1
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
            },
            "production_speed": 1,
            "production_per_cycle": 1
        }
    }

    def __init__(self, colony_data):
        super().__init__(colony_data)
        # self.resource_produced = "iron", "aluminium", "copper" or "titanium"
        self.resource_produced = None
        self.smelting_completed_percent = 0

    def switch_production(self, resource_type: str):
        if self.resource_produced != resource_type:
            # reset the smelting cycle
            self.smelting_completed_percent = 0
        self.resource_produced = resource_type

    def use_power_switch(self):
        # reset the smelting cycle if the building is turned off
        if self.enabled:
            self.smelting_completed_percent = 0
        super().use_power_switch()

    def update(self, dt):
        super().update(dt)
        # dump the produced resources into the colony resource buffer
        # only produce if enabled, at least level 1, and a resource to produce has been selected
        if self.enabled and (self.level > 0) and (self.resource_produced is not None):
            self.smelting_completed_percent += dt * self.parameters["production_speed"] \
                * (self.assigned_workers["production"]["engineers"] + self.assigned_workers["production"]["scientists"])
            # if the cycle is completed ...
            if self.smelting_completed_percent >= 100:
                # add the resource to the buffer
                self.colony_data["resources_buffer"][self.resource_produced] += self.parameters["production_per_cycle"]
                # reset the cycle
                self.smelting_completed_percent = 0


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
        self.can_disable = False


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
            },
            "production_speed": 1
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
            },
            "production_speed": 1
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
            },
            "production_speed": 1
        }
    }

    def update(self, dt):
        super().update(dt)
        # dump the produced resources into the colony resource buffer
        # only produce if enabled and at least level 1
        if self.enabled and (self.level > 0):
            # consume water
            water_required_from_storage = dt * self.parameters["production_speed"] \
                * (self.assigned_workers["production"]["engineers"] + self.assigned_workers["production"]["scientists"])
            water_obtained = min(water_required_from_storage, self.colony_data["resources"]["water"])
            self.colony_data["resources"]["water"] -= water_obtained
            # produce food
            self.colony_data["resources_buffer"]["food"] += water_obtained * 5
            # produce oxygen
            self.colony_data["resources_buffer"]["oxygen"] += water_obtained * 1


class BuildingSchool(Building):

    items_workload = {
        "engineers": 0,
        "scientists": 0,
        "pilots": 0
    }

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
            },
            "production_speed": 1,
            "items_workload": {
                "engineers": 0,
                "scientists": 0,
                "pilots": 0
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
            },
            "production_speed": 1,
            "items_workload": {
                "engineers": 0,
                "scientists": 0,
                "pilots": 0
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
            },
            "production_speed": 1,
            "items_workload": {
                "engineers": 0,
                "scientists": 0,
                "pilots": 0
            }
        }
    }

    def __init__(self, colony_data):
        super().__init__(colony_data)
        self.training_queue = []
        self.training_workload_completed = 0

    def add_worker_to_queue(self, worker_type):
        # worker_type = "engineers", "scientists" or "pilots"
        self.training_queue.append(worker_type)

    def can_cancel_training(self) -> bool:
        return len(self.training_queue) >= 1

    def cancel_training(self):
        # can be called even if impossible (update != on_draw)
        if self.can_cancel_training():
            # cancel the current training worker
            self.training_queue.pop(0)
            self.training_workload_completed = 0

    def can_clear_queue(self) -> bool:
        return len(self.training_queue) >= 2

    def clear_queue(self):
        # can be called even if impossible (update != on_draw)
        if self.can_clear_queue():
            # clear the queue (everything but the current training worker)
            self.training_queue = [self.training_queue[0]]

    def use_power_switch(self):
        # clear the queue and reset the training cycle if the building is turned off
        if self.enabled:
            self.training_queue = []
            self.training_workload_completed = 0
        super().use_power_switch()

    def update(self, dt):
        super().update(dt)
        # add the trained workers to the colony
        # only produce if enabled, at least level 1 and the training queue is not empty
        if self.enabled and (self.level > 0) and (len(self.training_queue) > 0):
            self.training_workload_completed += dt * self.parameters["production_speed"] \
                * (self.assigned_workers["production"]["engineers"] + self.assigned_workers["production"]["scientists"])
            # if the cycle is completed ...
            if self.training_workload_completed >= self.parameters["items_workload"][self.training_queue[0]]:
                # add the worker to the colony
                self.colony_data["workers"][self.training_queue[0]]["available"] += 1
                self.colony_data["workers"][self.training_queue[0]]["total"] += 1
                # remove the first element from the queue and reset the cycle
                self.training_queue.pop(0)
                self.training_workload_completed = 0


class BuildingFactory(Building):

    items_price = {
        "spaceship_small": {
            "resources": {
                ...: ...
            },
            "workload": 0
        },
        "spaceship_medium": {
            "resources": {
                ...: ...
            },
            "workload": 0
        },
        "spaceship_large": {
            "resources": {
                ...: ...
            },
            "workload": 0
        },
        "module_cargo_hold": {
            "resources": {
                ...: ...
            },
            "workload": 0
        },
        "module_liquid_tanks": {
            "resources": {
                ...: ...
            },
            "workload": 0
        },
        "module_passengers": {
            "resources": {
                ...: ...
            },
            "workload": 0
        },
        "module_headquarters": {
            "resources": {
                ...: ...
            },
            "workload": 0
        },
    }

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
            },
            "production_speed": 1
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
            },
            "production_speed": 1,
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
            },
            "production_speed": 1,
        }
    }

    def __init__(self, colony_data):
        super().__init__(colony_data)
        self.items_queue = []
        self.item_workload_completed = 0

    def can_make_item(self, item) -> bool:
        ...

    def add_item_to_queue(self, item):
        # pay the item price
        # add the item to the list
        self.training_queue.append(item)

    def can_cancel_training(self) -> bool:
        return len(self.training_queue) >= 1

    def cancel_training(self):
        # can be called even if impossible (update != on_draw)
        if self.can_cancel_training():
            # cancel the current training worker
            self.training_queue.pop(0)
            self.training_workload_completed = 0

    def can_clear_queue(self) -> bool:
        return len(self.training_queue) >= 2

    def clear_queue(self):
        # can be called even if impossible (update != on_draw)
        if self.can_clear_queue():
            # clear the queue (everything but the current training worker)
            self.training_queue = [self.training_queue[0]]

    def use_power_switch(self):
        # clear the queue and reset the training cycle if the building is turned off
        if self.enabled:
            self.training_queue = []
            self.training_workload_completed = 0
        super().use_power_switch()

    def update(self, dt):
        super().update(dt)
        # add the trained workers to the colony
        # only produce if enabled, at least level 1 and the training queue is not empty
        if self.enabled and (self.level > 0) and (len(self.training_queue) > 0):
            self.training_workload_completed += dt * self.parameters["production_speed"] \
                * (self.assigned_workers["production"]["engineers"] + self.assigned_workers["production"]["scientists"])
            # if the cycle is completed ...
            if self.training_workload_completed >= self.parameters["items_workload"][self.training_queue[0]]:
                # add the worker to the colony
                self.colony_data["workers"][self.training_queue[0]]["available"] += 1
                self.colony_data["workers"][self.training_queue[0]]["total"] += 1
                # remove the first element from the queue and reset the cycle
                self.training_queue.pop(0)
                self.training_workload_completed = 0


class BuildingResearchLabs(Building):

    # forget for now
    def __init__(self, colony_data):
        raise NotImplementedError("research labs not yet implemented")
