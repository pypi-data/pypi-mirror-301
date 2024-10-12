import matplotlib.pyplot as plt
import numpy as np

from pymsaviz import MsaViz
import tempfile
import os

def write_alignment_to_fasta(aln, fasta_file):
    """
    Writes the alignment result to a FASTA file to be visualized by pymsaviz.

    Parameters:
    - aln: Lifton_Alignment object containing the alignment information.
    - fasta_file: The output FASTA file to write the alignment to.
    """
    with open(fasta_file, "w") as f:
        f.write(f">Query\n{aln.traceback.query}\n")
        f.write(f">Reference\n{aln.traceback.ref}\n")

def visualize_alignment_with_pymsaviz(aln, wrap_length=60, output_file="alignment_viz.png"):
    """
    Visualizes the pairwise alignment result using pymsaviz and saves the visualization as an image.

    Parameters:
    - aln: Lifton_Alignment object containing the alignment information.
    - wrap_length: Number of characters per line for wrapping the sequence.
    - output_file: Path to save the alignment visualization.
    """
    if aln is None:
        print("No alignment found.")
        return

    # Write the alignment to a temporary FASTA file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".fa") as temp_fasta:
        write_alignment_to_fasta(aln, temp_fasta.name)

    # Visualize the alignment using pymsaviz
    mv = MsaViz(temp_fasta.name, wrap_length=wrap_length, show_count=True)
    mv.savefig(output_file)
    print(f"Alignment visualization saved to {output_file}")

    # Clean up the temporary file
    os.remove(temp_fasta.name)



import parasail
from Bio.Seq import Seq
from cigar import Cigar
from lifton import get_id_fraction, lifton_class


def adjust_cdss_protein_boundary(cdss_protein_aln_boundary, cigar_accum_len, length):
    """
        This function adjust CDS protein boundaries based on CIGAR string on protein alignment.

        Parameters:
        - cdss_protein_aln_boundary: CDS protein alignment boundary
        - cigar_accum_len: accumulated length of CIGAR string
        - length: length of CIGAR string

        Returns:
        cdss_protein_aln_boundary: adjusted CDS protein alignment boundary
    """
    cds_boundary_shift = 0
    for i in range(len(cdss_protein_aln_boundary)):
        cdss_start = cdss_protein_aln_boundary[i][0] + cds_boundary_shift
        cdss_end = cdss_protein_aln_boundary[i][1] + cds_boundary_shift
        if (cdss_start <= cigar_accum_len) and (cdss_end >= cigar_accum_len):
            cds_boundary_shift += length
            cdss_end += length
        cdss_protein_aln_boundary[i] = (cdss_start, cdss_end)
    return cdss_protein_aln_boundary


def get_cdss_protein_boundary(cdss_lens):
    """
        This function maps the CDSs boundaries on to the protein.

        Parameters:
        - cdss_lens: list of CDS lengths

        Returns:
        cdss_protein_boundary: CDS protein boundary
    """
    cdss_cumulative = [sum(cdss_lens[:i+1]) for i in range(len(cdss_lens))]
    cdss_cumulative_div = [x / 3 for x in cdss_cumulative]
    cdss_protein_boundary = {}
    for idx in range(len(cdss_cumulative_div)):
        start = cdss_cumulative_div[idx-1] if idx > 0 else 0
        end = cdss_cumulative_div[idx]
        cdss_protein_boundary[idx] = (start, end)
    return cdss_protein_boundary


def parasail_align_protein_base(protein_seq, ref_protein_seq):
    """
        This is the base function that uses parasail to align the protein sequence to the reference protein sequence.

        Parameters:
        - protein_seq: protein sequence in string format
        - ref_protein_seq: reference protein sequence in string format

        Returns:
        extracted_parasail_res: parasail alignment result
    """
    matrix = parasail.Matrix("blosum62")
    gap_open = 11
    gap_extend = 1
    protein_seq = "*" if protein_seq == "" else protein_seq
    # Return: (Query, Target)
    extracted_parasail_res = parasail.nw_trace_scan_sat(protein_seq, ref_protein_seq, gap_open, gap_extend, matrix)
    return extracted_parasail_res


def protein_align(protein_seq, ref_protein_seq):
    """
        This function aligns the protein sequence to the reference protein sequence and extracts the alignment information.

        Parameters:
        - protein_seq: protein sequence in string format
        - ref_protein_seq: reference protein sequence in string format

        Returns:
        lifton_aln: Lifton_Alignment object
    """
    extracted_parasail_res = parasail_align_protein_base(protein_seq, ref_protein_seq)
    visualize_alignment_with_pymsaviz(extracted_parasail_res, wrap_length=60, output_file="alignment_protein_viz.png")
    alignment_query = extracted_parasail_res.traceback.query
    alignment_comp = extracted_parasail_res.traceback.comp
    alignment_ref = extracted_parasail_res.traceback.ref
    extracted_matches, extracted_length = get_id_fraction.get_AA_id_fraction(extracted_parasail_res.traceback.ref, extracted_parasail_res.traceback.query)
    extracted_identity = extracted_matches/extracted_length
    lifton_aln = lifton_class.Lifton_Alignment(extracted_identity, None, alignment_query, alignment_comp, alignment_ref, None, None, protein_seq, ref_protein_seq, None)
    return lifton_aln


def parasail_align_DNA_base(trans_seq, ref_trans_seq):
    """
        This is the base function that uses parasail to align the transcript sequence to the reference transcript sequence.

        Parameters:
        - trans_seq: transcript sequence in string format
        - ref_trans_seq: reference transcript sequence in string format

        Returns:
        extracted_parasail_res: parasail alignment result
    """
    matrix = parasail.matrix_create("ACGT*", 1, -3)
    gap_open = 5
    gap_extend = 2
    # Return: (Query, Target)
    extracted_parasail_res = parasail.nw_trace_scan_sat(trans_seq, ref_trans_seq, gap_open, gap_extend, matrix)
    return extracted_parasail_res


def trans_align(trans_seq, ref_trans_seq):
    """
        This function aligns the transcript sequence to the reference transcript sequence and extracts the alignment information.

        Parameters:
        - trans_seq: transcript sequence in string format
        - ref_trans_seq: reference transcript sequence in string format

        Returns:
        lifton_aln: Lifton_Alignment object
    """
    extracted_parasail_res = parasail_align_DNA_base(trans_seq, ref_trans_seq)

    visualize_alignment_with_pymsaviz(extracted_parasail_res, wrap_length=60, output_file="alignment_DNA_viz.png")

    alignment_query = extracted_parasail_res.traceback.query
    alignment_comp = extracted_parasail_res.traceback.comp
    alignment_ref = extracted_parasail_res.traceback.ref
    # print("alignment_query: ", alignment_query) 
    # print("alignment_comp: ", alignment_comp) 
    # print("alignment_ref: ", alignment_ref) 
    extracted_matches, extracted_length = get_id_fraction.get_DNA_id_fraction(extracted_parasail_res.traceback.ref, extracted_parasail_res.traceback.query)
    extracted_identity = extracted_matches/extracted_length
    lifton_aln = lifton_class.Lifton_Alignment(extracted_identity, None, alignment_query, alignment_comp, alignment_ref, None, None, trans_seq, ref_trans_seq, None)
    return lifton_aln


def LiftOn_translate(lifton_trans, fai, ref_proteins, ref_trans_id):
    """
        This function translates the given annotation.
        
        Parameters:
        - lifton_trans: LiftOn transcript instance
        - fai: fasta index
        - ref_proteins: reference protein dictionary
        - ref_trans_id: reference transcript ID

        Returns:
        Referece protein sequence (in string), translated protein sequence (in string), CDS lengths, CDS children
    """
    coding_seq, cds_children, cdss_lens = lifton_trans.get_coding_seq(fai)
    coding_seq, _ = lifton_trans.get_coding_trans_seq(fai)
    protein_seq = lifton_trans.translate_coding_seq(coding_seq)
    # print("protein_seq: ", protein_seq)
    return str(ref_proteins[ref_trans_id]), protein_seq, cdss_lens, cds_children


def lifton_parasail_align(lifton_trans, db_entry, fai, ref_proteins, ref_trans_id):
    """
        This function aligns the annotated protein sequence to the reference protein sequence

        Parameters:
        - lifton_trans: LiftOn transcript instance
        - db_entry: database entry
        - fai: fasta index
        - ref_proteins: reference protein dictionary
        - ref_trans_id: reference transcript ID
        - lifton_status: LiftOn status

        Returns:
        aln: Lifton_Alignment object
    """
    # Step 1: Check if the ref_trans_id is in the reference protein dictionary
    aln = None
    if ref_trans_id not in ref_proteins.keys():
        return aln
    # Step 2: Translate the given annotation
    ref_protein_seq, protein_seq, cdss_lens, cds_children = LiftOn_translate(lifton_trans, fai, ref_proteins, ref_trans_id)
    # Step 3: Get the corresponding protein boundaries for each CDS
    cdss_protein_boundary = get_cdss_protein_boundary(cdss_lens)
    # Step 4: Protein alignment
    if protein_seq == None:
        return aln
    extracted_parasail_res = parasail_align_protein_base(protein_seq, ref_protein_seq)



    # Step 5: Extract the alignment information
    alignment_query = extracted_parasail_res.traceback.query
    alignment_comp = extracted_parasail_res.traceback.comp
    alignment_ref = extracted_parasail_res.traceback.ref
    cigar = extracted_parasail_res.cigar
    decoded_cigar = cigar.decode.decode()
    cigar_ls = list(Cigar(decoded_cigar).items())
    # Step 6: Change the CDS protein boundaries based on CIGAR string.
    cigar_accum_len = 0
    cdss_protein_aln_boundary = cdss_protein_boundary.copy()
    for length, symbol in cigar_ls:
        if symbol == "D":
            # print(length, symbol)
            cdss_protein_aln_boundary = adjust_cdss_protein_boundary(cdss_protein_aln_boundary, cigar_accum_len, length)
        cigar_accum_len += length
        # print("cigar_accum_len: ", cigar_accum_len)
    extracted_matches, extracted_length = get_id_fraction.get_AA_id_fraction(extracted_parasail_res.traceback.ref, extracted_parasail_res.traceback.query)
    extracted_identity = extracted_matches/extracted_length
    aln = lifton_class.Lifton_Alignment(extracted_identity, cds_children, alignment_query, alignment_comp, alignment_ref, cdss_protein_boundary, cdss_protein_aln_boundary, protein_seq, ref_protein_seq, db_entry)
    return aln


