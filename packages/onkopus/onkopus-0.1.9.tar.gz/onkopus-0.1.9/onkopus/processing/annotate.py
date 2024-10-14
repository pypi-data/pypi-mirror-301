import adagenes
import onkopus as op


def annotate(bframe:adagenes.BiomarkerFrame,
             genome_version=None,
             oncokb_key=None,
             lo_hg19=None,
             lo_hg38=None,
             tumor_type=None) -> adagenes.BiomarkerFrame:
    """
    Runs the full Onkopus annotation pipeline to annotate biomarkers

    :param bframe:
    :return:
    """
    if genome_version is not None:
        bframe.genome_version = genome_version

    # Recognize biomarkers
    bframe = adagenes.recognize_biomarker_types(bframe)

    # Map biomarkers on protein and transcript level to genomic level (MANE Select)
    #bframe = op.map_protein_keys_to_genomic(bframe)

    # Liftover
    target_genome = None
    if bframe.genome_version != "hg38":
        target_genome = "hg38"
    bframe = adagenes.liftover(bframe, target_genome=target_genome)

    # Annotate biomarkers
    bframe.data = op.annotate_snvs(bframe.data,genome_version=bframe.genome_version,oncokb_key=oncokb_key,
                                   lo_hg19=lo_hg19,lo_hg38=lo_hg38,tumor_type=tumor_type)
    bframe.data = op.annotate_indels(bframe.data,genome_version=bframe.genome_version,oncokb_key=oncokb_key,tumor_type=tumor_type)
    bframe.data = op.annotate_fusions(bframe.data,genome_version=bframe.genome_version,tumor_type=tumor_type)
    bframe.data = op.annotate_genes(bframe.data, genome_version=bframe.genome_version,tumor_type=tumor_type)

    return bframe

