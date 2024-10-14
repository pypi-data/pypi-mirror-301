import unittest
import onkopus as op
import adagenes


class TestBiomarkerTypeConversion(unittest.TestCase):

    def test_protein_to_genomic(self):
        bframe = adagenes.BiomarkerFrame(data_type="p")
        bframe.data = {"NRAS:Q61L": {}}

        bframe = op.ProteinToGenomic().process_data(bframe)

        print(bframe)

