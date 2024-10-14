import onkopus


class AllModulesClient:

    def __init__(self, genome_version):
        self.queryid = 'q_id'
        self.genome_version = genome_version

    def process_data(self, biomarker_data):

        biomarker_data = onkopus.annotate_variant_data(biomarker_data)

        return biomarker_data
