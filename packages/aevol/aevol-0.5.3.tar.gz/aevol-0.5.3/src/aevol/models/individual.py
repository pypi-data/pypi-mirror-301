# ************************************************************************
#                          individual  -  realization
# ************************************************************************

# ---------------------------------------------------------------- INCLUDE
import json
from typing import List

from aevol.models.phenotypic_function import PhenotypicFunction
from aevol.models.protein import Protein
from aevol.models.rna import Rna

# ---------------------------------------------------------------- INDIVIDUAL


class Individual:
    """
    An individual

    Attributes
    ----------
    genome_length : int
        the length of the genome
    rnas: List[Rna]
        list of RNAs on the genome
    proteins: List[Protein]
        list of proteins encoded on the genome
    phenotype: PhenotypicFunction
        phenotype of the individual
    """

    def __init__(
        self,
        genome_length: int,
        rnas: List[Rna],
        proteins: List[Protein],
        phenotype: PhenotypicFunction,
    ):
        self.genome_length = genome_length
        self.rnas = rnas
        self.proteins = proteins
        self.phenotype = phenotype

    @classmethod
    def from_json_file(cls, filename):
        try:
            with open(filename, encoding="utf-8") as file:
                individual = json.load(file)

                genome_len = individual["indiv"]["genome_len"]

                if genome_len <= 0:
                    raise NameError("The genome_length cannot be null or negative")

                rnas = []
                for rna in individual["indiv"]["rnas"]:
                    rnas.append(Rna.from_json_obj(rna))

                proteins = []
                for protein in individual["indiv"]["proteins"]:
                    proteins.append(Protein.from_json_obj(protein))

                phenotype = PhenotypicFunction(individual["indiv"]["phenotype"]["points"])

                return cls(genome_len, rnas, proteins, phenotype)

        except Exception as e:
            print(e)
