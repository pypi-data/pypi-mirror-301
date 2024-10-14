import unittest
import onkopus as op


class ScanNetTestCase(unittest.TestCase):

    def test_bindingsite_client(self):
        genome_version = 'hg38'

        qid = "chr7:140753336A>T"
        data = {qid: {}, "chr12:25245350C>T": {}}

        variant_data = op.UTAAdapterClient(
            genome_version=genome_version).process_data(data)
        print("uta response", variant_data)

        pdb_data = op.PDBClient(
            genome_version=genome_version).process_data(variant_data[qid])

        #print(variant_data)

        variant_data = op.ScanNetBindingSiteClient(
            genome_version=genome_version).process_data(pdb_data,variant_data[qid]["UTA_Adapter"]["gene_name"])

        print("ScanNet response ",variant_data)
