"""
A basic model for predicting the duration of an RCA reaction using dNTP exhaustion as the primary variable. Once a dNTP molecule count becomes zero, the RCA reaction is considered complete.

Assumptions in the current model:
- S1 primer is in excess.
- Phi29 is in excess.
- Viscosity is not a factor.
- Phi29 synthesises indefinitely once primed to a template strand.

Algorithm:

Calculate the dNTP exhaustion rate given key reaction variables:
- Reaction volume (ml)
- dNTP concentration (mM)
- Template DNA mass
- Template DNA sequence
- Phi29 synthesis rate (nucleotides/minute)

"""

def molar_to_molecule(concentration: str, reaction_volume: float):
    dilution_factor = {
        "mM": 1000,
        "uM": 1_000_000,
        "nM": 1_000_000_000
    }
    values = concentration.split()
    conc = float(values[0])
    dilution = values[1]
    moles = reaction_volume * (conc / (dilution_factor[dilution] * 1000))
    molecule_count = moles * (6.022 * 10**23)
    
    return molecule_count

def dna_mass_to_moles(dna_mass: str, sequence: str):
    dilution_factor = {
        "g": 1,
        "mg": 1000,
        "ug": 1_000_000,
        "ng": 1_000_000_000,
        "pg": 1_000_000_000_000
    }
    values = dna_mass.split()
    mass = float(values[0])
    dilution = values[1]
    moles = (mass / dilution_factor[dilution]) / ((617.96 * len(sequence)) + 36.04)
    molecules_of_template = moles * (6.022 * 10**23)
    
    return molecules_of_template

def units_to_molecule(unit_conc: int, specific_activity: int, volume: float):

    phi29_molar_mass = 67000 # g/mol
    phi29_mass = unit_conc / specific_activity * volume # in mg
    molecules_in_reaction = (phi29_mass / (1000 * phi29_molar_mass)) * (6.022 * 10**23)
    print(phi29_mass, molecules_in_reaction)

    return molecules_in_reaction

def base_complement(nucleotide):
    base_pairs = {
        "A": "T",
        "T": "A",
        "G": "C",
        "C": "G"
    }
    return base_pairs[nucleotide]

def count_nt(sequence: str):
    nt_count = {
        "A": 0,
        "T": 0,
        "G": 0,
        "C": 0
    }

    for nt in sequence:
        try:
            nt_count[nt.upper()] += 1
            nt_count[base_complement(nt.upper())] += 1
        except KeyError:
            print("Invalid nucleotide in sequence")

    return nt_count

def rca_time(nt_count: dict, ntp_molecules: float, phi29_molecules: float, template_molecules: float):
    """Calculate incubate time necessary for phi29 to reach RCA completion"""
    phi29_speed = 2280 # nt/min
    nt_list = nt_count.values()
    highest_nt_count = max(nt_list)
    ntps_per_molecule = sum(nt_list)/2
    number_of_rca_cycles = 1 + (((ntp_molecules / 4)-(highest_nt_count * template_molecules)) / (highest_nt_count * 2 * template_molecules))
    print(number_of_rca_cycles, ntps_per_molecule)
    print(phi29_molecules > 2*template_molecules)
    total_rca_time = (number_of_rca_cycles * ntps_per_molecule) / (phi29_speed) # in minutes
    print(f"Estimated time for RCA completion by way of dNTP exhaustion: {total_rca_time/(60*24)} days")
    
    return total_rca_time

def main():
    ntp_conc = "20 mM"
    reaction_volume = 1 # in mL
    no_of_ntp_molecules = molar_to_molecule(ntp_conc, reaction_volume)
    print(f"dNTP molecules in the reaction: {no_of_ntp_molecules}")

    phi29_conc = 10_000 # units/ml
    phi29_activity = 83_333 # units/mg
    phi29_volume = 0.001 # ml
    no_of_phi29_molecules = units_to_molecule(phi29_conc, phi29_activity, phi29_volume)
    print(f"Phi29 molecules in the reaction: {no_of_phi29_molecules}")

    sequence_dbc = "gcgtataatggactattgtgtgctgatatgtacaCCTgAGGacacaggtacaggactcagcttaaGtaatacgactcactataAggACATTTGCTTCTGACACAACTGTGTTCACTAGCAACCTCAAACAGACACCATGGAAGATGCCAAAAACATTAAGAAGGGCCCAGCGCCATTCTACCCACTCGAAGACGGGACCGCCGGCGAGCAGCTGCACAAAGCCATGAAGCGCTACGCCCTGGTGCCCGGCACCATCGCCTTTACCGACGCACATATCGAGGTGGACATTACCTACGCCGAGTACTTCGAGATGAGCGTTCGGCTGGCAGAAGCTATGAAGCGCTATGGGCTGAATACAAACCATCGGATCGTGGTGTGCAGCGAGAATAGCTTGCAGTTCTTCATGCCCGTGTTGGGTGCCCTGTTCATCGGTGTGGCTGTGGCCCCAGCTAACGACATCTACAACGAGCGCGAGCTGCTGAACAGCATGGGCATCAGCCAGCCCACCGTCGTATTCGTGAGCAAGAAAGGGCTGCAAAAGATCCTCAACGTGCAAAAGAAGCTACCGATCATACAAAAGATCATCATCATGGATAGCAAGACCGACTACCAGGGCTTCCAAAGCATGTACACCTTCGTGACTTCCCATTTGCCACCCGGCTTCAACGAGTACGACTTCGTGCCCGAGAGCTTCGACCGGGACAAAACCATCGCCCTGATCATGAACAGTAGTGGCAGTACCGGATTGCCCAAGGGCGTAGCCCTACCGCACCGCACCGCTTGTGTCCGATTCAGTCATGCCCGCGACCCCATCTTCGGCAACCAGATCATCCCCGACACCGCTATCCTCAGCGTGGTGCCATTTCACCACGGCTTCGGCATGTTCACCACGCTGGGCTACTTGATCTGCGGCTTTCGGGTCGTGCTCATGTACCGCTTCGAGGAGGAGCTATTCTTGCGCAGCTTGCAAGACTATAAGATTCAATCTGCCCTGCTGGTGCCCACACTATTTAGCTTCTTCGCTAAGAGCACTCTCATCGACAAGTACGACCTAAGCAACTTGCACGAGATCGCCAGCGGCGGGGCGCCGCTCAGCAAGGAGGTAGGTGAGGCCGTGGCCAAACGCTTCCACCTACCAGGCATCCGCCAGGGCTACGGCCTGACAGAAACAACCAGCGCCATTCTGATCACCCCCGAAGGGGACGACAAGCCTGGCGCAGTAGGCAAGGTGGTGCCCTTCTTCGAGGCTAAGGTGGTGGACTTGGACACCGGTAAGACACTGGGTGTGAACCAGCGCGGCGAGCTGTGCGTCCGTGGCCCCATGATCATGAGCGGCTACGTTAACAACCCCGAGGCTACAAACGCTCTCATCGACAAGGACGGCTGGCTGCACAGCGGCGACATCGCCTACTGGGACGAGGACGAGCACTTCTTCATCGTGGACCGGCTGAAGtctCTGATCAAATACAAGGGCTACCAGGTAGCCCCAGCCGAACTGGAGAGCATCCTGCTGCAACACCCCAACATCTTCGACGCCGGGGTCGCCGGCCTGCCCGACGACGATGCCGGCGAGCTGCCCGCCGCAGTCGTCGTGCTGGAACACGGTAAAACCATGACCGAGAAGGAGATCGTGGACTATGTGGCCAGCCAGGTTACAACCGCCAAGAAGCTGCGCGGTGGTGTTGTGTTCGTGGACGAGGTGCCTAAAGGACTGACCGGCAAGTTGGACGCCCGCAAGATCCGCGAGATTCTCATTAAGGCCAAGAAGGGCGGCAAGATCGCCGTGTAAGCTCGCTTTCTTGCTGTCCAATTTCTATTAAAGGTTCCTTTGTTCCCTAAGTCCAACTACTAAACTGGGGGATATTATGAAGGGCCTTGAGCATCTGGATTCTGCCTAATAAAAAACATTTATTTTCATTGCAagtacAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaacGAAGAGCtagcAGATAACAGATACttcgGtatctgttatctgttTTTTTTcAACAGATAGCCGCGttcgCGCGGCtatctgttTTTTTTgcatgCCtcacaGGCagatctatcagcacacaattgcccattatacgc"
    sequence_pdna = "gcgtataatggactattgtgtgctgatatgtacaCCTgAGGacacaggtacaggactcagcttaaGtaatacgactcactataAggACATTTGCTTCTGACACAACTGTGTTCACTAGCAACCTCAAACAGACACCATGGAAGATGCCAAAAACATTAAGAAGGGCCCAGCGCCATTCTACCCACTCGAAGACGGGACCGCCGGCGAGCAGCTGCACAAAGCCATGAAGCGCTACGCCCTGGTGCCCGGCACCATCGCCTTTACCGACGCACATATCGAGGTGGACATTACCTACGCCGAGTACTTCGAGATGAGCGTTCGGCTGGCAGAAGCTATGAAGCGCTATGGGCTGAATACAAACCATCGGATCGTGGTGTGCAGCGAGAATAGCTTGCAGTTCTTCATGCCCGTGTTGGGTGCCCTGTTCATCGGTGTGGCTGTGGCCCCAGCTAACGACATCTACAACGAGCGCGAGCTGCTGAACAGCATGGGCATCAGCCAGCCCACCGTCGTATTCGTGAGCAAGAAAGGGCTGCAAAAGATCCTCAACGTGCAAAAGAAGCTACCGATCATACAAAAGATCATCATCATGGATAGCAAGACCGACTACCAGGGCTTCCAAAGCATGTACACCTTCGTGACTTCCCATTTGCCACCCGGCTTCAACGAGTACGACTTCGTGCCCGAGAGCTTCGACCGGGACAAAACCATCGCCCTGATCATGAACAGTAGTGGCAGTACCGGATTGCCCAAGGGCGTAGCCCTACCGCACCGCACCGCTTGTGTCCGATTCAGTCATGCCCGCGACCCCATCTTCGGCAACCAGATCATCCCCGACACCGCTATCCTCAGCGTGGTGCCATTTCACCACGGCTTCGGCATGTTCACCACGCTGGGCTACTTGATCTGCGGCTTTCGGGTCGTGCTCATGTACCGCTTCGAGGAGGAGCTATTCTTGCGCAGCTTGCAAGACTATAAGATTCAATCTGCCCTGCTGGTGCCCACACTATTTAGCTTCTTCGCTAAGAGCACTCTCATCGACAAGTACGACCTAAGCAACTTGCACGAGATCGCCAGCGGCGGGGCGCCGCTCAGCAAGGAGGTAGGTGAGGCCGTGGCCAAACGCTTCCACCTACCAGGCATCCGCCAGGGCTACGGCCTGACAGAAACAACCAGCGCCATTCTGATCACCCCCGAAGGGGACGACAAGCCTGGCGCAGTAGGCAAGGTGGTGCCCTTCTTCGAGGCTAAGGTGGTGGACTTGGACACCGGTAAGACACTGGGTGTGAACCAGCGCGGCGAGCTGTGCGTCCGTGGCCCCATGATCATGAGCGGCTACGTTAACAACCCCGAGGCTACAAACGCTCTCATCGACAAGGACGGCTGGCTGCACAGCGGCGACATCGCCTACTGGGACGAGGACGAGCACTTCTTCATCGTGGACCGGCTGAAGtctCTGATCAAATACAAGGGCTACCAGGTAGCCCCAGCCGAACTGGAGAGCATCCTGCTGCAACACCCCAACATCTTCGACGCCGGGGTCGCCGGCCTGCCCGACGACGATGCCGGCGAGCTGCCCGCCGCAGTCGTCGTGCTGGAACACGGTAAAACCATGACCGAGAAGGAGATCGTGGACTATGTGGCCAGCCAGGTTACAACCGCCAAGAAGCTGCGCGGTGGTGTTGTGTTCGTGGACGAGGTGCCTAAAGGACTGACCGGCAAGTTGGACGCCCGCAAGATCCGCGAGATTCTCATTAAGGCCAAGAAGGGCGGCAAGATCGCCGTGTAAGCTCGCTTTCTTGCTGTCCAATTTCTATTAAAGGTTCCTTTGTTCCCTAAGTCCAACTACTAAACTGGGGGATATTATGAAGGGCCTTGAGCATCTGGATTCTGCCTAATAAAAAACATTTATTTTCATTGCAAgtacGAGACCgccgccgtgttgactcctGTTGATAGATCCAGTAATGACCTCAGAACTCCATCTGGATTTGTTCAGAACGCTCGGTTGCCGCCGGGCGTTTTTTATTGGTGAGAATcgccgctcccgCCTCAGcggaccgatcctgcaggtgcacatatgcgatcgcttaattaatgcgcatcgatgctctagattaacccccctgacaatttaaatcaaagcccgccgaaaggcgggcttttctgtggatccacgtgcccccctgacaccattatacgctCgtgtctcaaaatctctgatgttacattgcacaagataaaaatatatcatcatgaacaataaaactgtctgcttacataaacagtaatacaaggggtgttACGTatgattgaacaagatggattgcacgcaggttctccggccgcggccgcttgggtggagaggctattcggctatgactgggcacaacagacaatcggctgctctgatgccgccgtgttccggctgtcagcgcaggggcgcccggttctttttgtcaagaccgacctgtccggtgccctgaacgaactgcaagacgaggcagcgcggctatcgtggctggccacgacgggcgttccttgcgcagcagtgctcgacgttgtcactgaagcgggaagggactggctgctattgggcgaagtgccggggcaggatctcctgtcatctcaccttgctcctgccgagaaagtatccatcatggctgatgcaatgcggcggctgcatacgctggatccggctacctgcccattcgaccaccaagcgaaacatcgcatcgagcgggcacgtactcggatggaagccggtcttgtcgatcaggatgatctggacgaagagcatcaggggctcgcgccagccgaactgttcgccaggctcaaggcgagaatgcccgacggcgaggatctcgtcgtgacccacggcgatgcctgcttgccgaatatcatggtggaaaatggccgcttttctggattcatcgactgtggccggctgggtgtggcggaccgctatcaggacatagcgttggctacccgtgatattgctgaagagcttggcggcgaatgggctgaccgcttcctcgtgctttacggtatcgccgctcccgattcgcagcgcatcgccttctatcgccttcttgacgagttcttctaacccccctgacagccgccgtgttccattatacgcgcacaacgtgcgggcaggataggtgaagtaggcccacccgcgagcgggtgttccttcttcactgtcccttattcgcacctggcggtgctcaacgggaatcctgctctgcgaggctggccggcgtataatggtgtcaggggggTCGCGAgttaattaatgcgcatcgataatcctgcaggtgcacatatgcgatcgcggaccgtctagaGCTcgctcgcttctagaggccggtgcaccgaaacggtgcaccgacgggatccgctttgcggatcccggcctctagaagcgagcgGGGGCGGCGACCTCagctccccgtagaaaagatcaaaggatcttcttgagatcctttttttctgcgcgtaatctgctgcttgcaaacaaaaaaaccaccgctaccagcggtggtttgtttgccggatcaagagctaccaactctttttccgaaggtaactggcttcagcagagcgcagataccaaatactgttcttctagtgtagccgtagttaggccaccacttcaagaactctgtagcaccgcctacatacctcgctctgctaatcctgttaccagtggctgctgccagtggcgataagtcgtgtcttaccgggttggactcaagacgatagttaccggataaggcgcagcggtcgggctgaacggggggttcgtgcacacagcccagcttggagcgaacgacctacaccgaactgagatacctacagcgtgagctatgagaaagcgccacgcttcccgaagggagaaaggcggacaggtatccggtaagcggcagggtcggaacaggagagcgcacgagggagcttccagggggaaacgcctggtatctttatagtcctgtcgggtttcgccacctctgacttgagcgtcgatttttgtgatgcttgtcaggggggcggagcctatggaaaaacgccagcaacgcggcctttttacggttcctggccttttgctggccttttgctcgtttAAACggatccatttgtcctactcaggagagcgttcaccgacaaacaacagataaaacgaaaggcccagtctttcgactgagcctttcgttttatttggcgtataatggcgccgctcccgTGTCAGGGGGGTTAATTAatgcgcATCGATtcggaccggatcctgcagGTGCACATATgCGATCgctctagacatgtCCTgAGGtgtacagGGTCTCAaacGAAGAGCtagcAGATAACAGATACttcgGtatctgttatctgttTTTTTTcAACAGATAGCCGCGttcgCGCGGCtatctgttTTTTTTgcatgCCtcacaGGCagatctatcagcacacaattgcccattatacgc"
    sequence_nt_count = count_nt(sequence_pdna)
    print(sequence_nt_count)

    template_molecules = dna_mass_to_moles("2000 ng", sequence_pdna)
    print(f"Template DNA molecules in the reaction: {template_molecules}")
    rca_time(sequence_nt_count, no_of_ntp_molecules, no_of_phi29_molecules, template_molecules)

    return 0

if __name__ == '__main__':
    main()

# Source 1: https://uk.neb.com/faqs/2011/01/20/at-what-rate-does-phi29-dna-polymerase-add-nucleotides-to-a-primed-single-stranded-template
# Source 2: https://www.qiagen.com/us/products/oem-by-qiagen/oem-enzymes/oem-dna-polymerase/29-dna-polymerase
# Source 3: https://www.physiologyweb.com/calculators/units_per_volume_solution_concentration_calculator.html