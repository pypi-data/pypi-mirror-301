import unittest,os
import adagenes
import onkopus


class TreatmentExportTestCase(unittest.TestCase):

    def test_export_treatment_data(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        oncokb_key = os.getenv("ONCOKB_KEY")

        data = {"chr7:140753336A>T":{}, "chr17:7673776G>A":{}}
        genome_version = "hg38"
        bf = adagenes.BiomarkerFrame(genome_version=genome_version,data=data)
        bf = onkopus.annotate(bf, genome_version="hg38",oncokb_key=oncokb_key)

        #print(bf.data["chr7:140753336A>T"]["oncokb"])

        outfile=__location__ + "/../test_files/test_writer.out.csv"
        onkopus.ClinSigWriter().write_evidence_data_to_file(outfile,bf)

        #file = open(outfile)
        #contents = file.read()
        #contents_expected = """genomic_location_hg38,chrom,pos_hg38,pos_hg19,ref,alt,mutation_type,hgnc_gene_symbol,aa_exchange,aa_exchange_long,ncbi_transcript_mane_select,ncbi_cdna_string,ncbi_cds_start,ncbi_cds_end,ncbi_cds_strand,ncbi_prot_location,ncbi_protein_id,clinvar_clinical_significance,clinvar_review_status,clinvar_cancer_type,clinvar_id,dbsnp_population_frequency,dbsnp_rsid,gnomAD_exomes_ac,gnomAD_exomes_af,1000genomes_af,1000genomes_ac,alfa_total_af,alfa_total_ac,ExAC_AF,ExAC_AC,revel_score,alphamissense_score,mvp_score,loftool_score,vuspredict_score,missense3D_pred,CADD_score_raw,Polyphen2_HDIV_score,Polyphen2_HDIV_pred,Polyphen2_HVAR_score,Polyphen2_HVAR_pred,SIFT_score,SIFT_pred,GERP++_score,MetaLR_score,MetaSVM_score,phastCons17way_primate_score,phyloP17way_primate,MutationAssessor_score,MutationTaster_score,fathmm-MKL_coding_score,fathmm-XF_coding_score,uniprot_id,alphamissense_class,Interpro_domain,protein_sequence_MANE_Select,Secondary_protein_structure,RelASA,BLOSUM62
        #,7,140753336,,A,T,,BRAF,V600E,Val600Glu,NM_004333.6,,,,,,,,,,,,,1,3.979940e-06,.,.,.,.,1.647e-05,2,,,,,,,4.2,0.97,D (probably damaging),0.94,D (probably damaging),0.0,,5.65,0.2357,-0.7685,0.999000,0.750000,0.65,1.0,0.99,0.91,,,|Serine-threonine/tyrosine-protein kinase  catalytic domain||Protein kinase domain||Protein kinase domain;Serine-threonine/tyrosine-protein kinase  catalytic domain||Protein kinase domain||Protein kinase domain;Serine-threonine/tyrosine-protein kinase  catalytic domain||Protein kinase domain||Protein kinase domain;Serine-threonine/tyrosine-protein kinase  catalytic domain||Protein kinase domain||Protein kinase domain|,,,,\n"""
        #self.assertEqual(contents, contents_expected, "")
        #file.close()

