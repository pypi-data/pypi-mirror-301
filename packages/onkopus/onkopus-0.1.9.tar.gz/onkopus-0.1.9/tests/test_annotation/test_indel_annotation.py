import unittest
import onkopus as op


class TestInDelAnnotationPipeline(unittest.TestCase):

    def test_indel_annotation(self):
        data = {"chr16:68846077C>CTTCAA":{}}
        data = op.indel_request(data)
        #print(data["chr16:68846077C>CTTCAA"]["clinvar"])

        #self.assertListEqual(list(data["chr16:68846077C>CTTCAA"].keys()),["variant_data","gencode_genomic","clinvar"],"Sections do not match")
