import os
from typing import List, Optional
from dataclasses import dataclass
from RosettaPy import Rosetta, RosettaScriptsVariableGroup, RosettaEnergyUnitAnalyser, MPI_node
from RosettaPy.utils import timing

script_dir = os.path.dirname(os.path.abspath(__file__))


@dataclass
class CartesianDDG:
    pdb: str

    def relax(self): ...

    def cartesian_ddg(self): ...

    @staticmethod
    def mut2mutfile(): ...
