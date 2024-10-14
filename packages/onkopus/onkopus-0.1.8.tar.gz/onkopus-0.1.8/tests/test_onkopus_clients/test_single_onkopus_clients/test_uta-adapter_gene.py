import unittest, copy
import onkopus.onkopus_clients


class UTAAdapterGeneAnnotationTestCase(unittest.TestCase):

    def test_uta_adapter_genetogenomic_client(self):
        genome_version = 'hg38'
        data = {"NRAS:Q61L": {}, "TP53:R282W": {}}
        variant_data = onkopus.onkopus_clients.CCSGeneToGenomicClient(
            genome_version=genome_version).process_data(data)
        print("Response ",variant_data)
        qids = ["chr1:114713908T>A", "chr17:7673776G>A"]
        self.assertListEqual(list(variant_data.keys()), qids, "Error UTA adapter GeneToGenomic")

    def test_uta_adapter_client_batch(self):
        genome_version = 'hg38'

        #infile='../../test_files/somaticMutations.l100.vcf'
        infile = '../../test_files/somaticMutations.vcf'
        #onkopus.annotate_file(file, file+'.clinvar', 'clinvar', genome_version=genome_version)

        #data = onkopus.read_file(file, genome_version=genome_version)

        #infile="../../test_files/somaticMutations.ln_12.vcf"
        #infile="../../test_files/medium_input.vcf"
        #infile="../../test_files/99_input.vcf"
        #data = onkopus.VCFReader(genome_version).read_file(infile=infile)
        #data = onkopus.read_file(infile)
        #data.data = onkopus.onkopus_clients.UTAAdapterClient(genome_version=genome_version).process_data(data.data)
        #variant_data = onkopus.onkopus_clients.CCSGeneToGenomicClient(
        #    genome_version=genome_version).process_data(data.data)
        #print("Response ",variant_data)
