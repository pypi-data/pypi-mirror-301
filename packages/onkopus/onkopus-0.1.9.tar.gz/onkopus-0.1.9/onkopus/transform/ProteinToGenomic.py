import copy
from adagenes.clients import client
import onkopus as op
import adagenes
import onkopus.tools


class ProteinToGenomic(client.Client):
    """
    Transforms biomarker data on protein level to genomic level

    """

    def process_data(self, bframe):
        if isinstance(bframe, adagenes.BiomarkerFrame):
            vdata = bframe.data
        else:
            vdata = bframe

        if bframe.data_type == "p":
            data = op.CCSGeneToGenomicClient(genome_version=bframe.genome_version).process_data(vdata)
            if isinstance(data, dict):
                new_data = {}
                for var in data.keys():
                    if isinstance(data[var],dict):
                        results_string = data[var]["UTA_Adapter_gene"]["results_string"]
                        new_data = onkopus.tools.protein_to_genomic(new_data, results_string, data[var],
                                                                 None, genome_version=bframe.genome_version)

                if isinstance(bframe, dict):
                    bf = adagenes.BiomarkerFrame(vdata, data_type="g")
                    return bf
                else:
                    bframe.data = copy.deepcopy(new_data)
                    bframe.data_type = "g"
                    return bframe
            else:
                return bframe
        else:
            return bframe

