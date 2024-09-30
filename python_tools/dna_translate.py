"""
Tool to take a nucleotide sequence and convert it to a peptide.

In current version, this tool ignores searching for start and stop codons.
It will naively translate all 6 frames of the full nucleotide sequence.
If a stop codon is encountered when translating, it will be ignored.
"""

import json

# Codon Table Dictionary:

codons: dict[str, dict[str, str]] = {
    "ttt": {
        "letter": 'F',
        "abbreviation": 'Phe',
        "amino_acid": "Phenyalanine"
    },
    "ttc": {
        "letter": 'F',
        "abbreviation": 'Phe',
        "amino_acid": "Phenyalanine"
    },
    "tta": {
        "letter": 'L',
        "abbreviation": 'Leu',
        "amino_acid": "Leucine"
    },
    "ttg": {
        "letter": 'L',
        "abbreviation": 'Leu',
        "amino_acid": "Leucine"
    },
    "ctt": {
        "letter": 'L',
        "abbreviation": 'Leu',
        "amino_acid": "Leucine"
    },
    "ctc": {
        "letter": 'L',
        "abbreviation": 'Leu',
        "amino_acid": "Leucine"
    },
    "cta": {
        "letter": 'L',
        "abbreviation": 'Leu',
        "amino_acid": "Leucine"
    },
    "ctg": {
        "letter": 'L',
        "abbreviation": 'Leu',
        "amino_acid": "Leucine"
    },
    "att": {
        "letter": 'I',
        "abbreviation": 'Ile',
        "amino_acid": "Isoleucine"
    },
    "atc": {
        "letter": 'I',
        "abbreviation": 'Ile',
        "amino_acid": "Isoleucine"
    },
    "ata": {
        "letter": 'I',
        "abbreviation": 'Ile',
        "amino_acid": "Isoleucine"
    },
    "atg": {
        "letter": 'M',
        "abbreviation": 'Met',
        "amino_acid": "Methionine"
    },
    "gtt": {
        "letter": 'V',
        "abbreviation": 'Val',
        "amino_acid": "Valine"
    },
    "gtc": {
        "letter": 'V',
        "abbreviation": 'Val',
        "amino_acid": "Valine"
    },
    "gta": {
        "letter": 'V',
        "abbreviation": 'Val',
        "amino_acid": "Valine"
    },
    "gtg": {
        "letter": 'V',
        "abbreviation": 'Val',
        "amino_acid": "Valine"
    },
    "tct": {
        "letter": 'S',
        "abbreviation": 'Ser',
        "amino_acid": "Serine"
    },
    "tcc": {
        "letter": 'S',
        "abbreviation": 'Ser',
        "amino_acid": "Serine"
    },
    "tca": {
        "letter": 'S',
        "abbreviation": 'Ser',
        "amino_acid": "Serine"
    },
    "tcg": {
        "letter": 'S',
        "abbreviation": 'Ser',
        "amino_acid": "Serine"
    },
    "cct": {
        "letter": 'P',
        "abbreviation": 'Pro',
        "amino_acid": "Proline"
    },
    "ccc": {
        "letter": 'P',
        "abbreviation": 'Pro',
        "amino_acid": "Proline"
    },
    "cca": {
        "letter": 'P',
        "abbreviation": 'Pro',
        "amino_acid": "Proline"
    },
    "ccg": {
        "letter": 'P',
        "abbreviation": 'Pro',
        "amino_acid": "Proline"
    },
    "act": {
        "letter": 'T',
        "abbreviation": 'Thr',
        "amino_acid": "Threonine"
    },
    "acc": {
        "letter": 'T',
        "abbreviation": 'Thr',
        "amino_acid": "Threonine"
    },
    "aca": {
        "letter": 'T',
        "abbreviation": 'Thr',
        "amino_acid": "Threonine"
    },
    "acg": {
        "letter": 'T',
        "abbreviation": 'Thr',
        "amino_acid": "Threonine"
    },
    "gct": {
        "letter": 'A',
        "abbreviation": 'Ala',
        "amino_acid": "Alanine"
    },
    "gcc": {
        "letter": 'A',
        "abbreviation": 'Ala',
        "amino_acid": "Alanine"
    },
    "gca": {
        "letter": 'A',
        "abbreviation": 'Ala',
        "amino_acid": "Alanine"
    },
    "gcg": {
        "letter": 'A',
        "abbreviation": 'Ala',
        "amino_acid": "Alanine"
    },
    "tat": {
        "letter": 'Y',
        "abbreviation": 'Tyr',
        "amino_acid": "Tyrosine"
    },
    "tac": {
        "letter": 'Y',
        "abbreviation": 'Tyr',
        "amino_acid": "Tyrosine"
    },
    "taa": {
        "letter": '*',
        "abbreviation": 'Sto',
        "amino_acid": "Stop"
    },
    "tag": {
        "letter": '*',
        "abbreviation": 'Sto',
        "amino_acid": "Stop"
    },
    "cat": {
        "letter": 'H',
        "abbreviation": 'His',
        "amino_acid": "Histidine"
    },
    "cac": {
        "letter": 'H',
        "abbreviation": 'His',
        "amino_acid": "Histidine"
    },
    "caa": {
        "letter": 'Q',
        "abbreviation": 'Gln',
        "amino_acid": "Glutamine"
    },
    "cag": {
        "letter": 'Q',
        "abbreviation": 'Gln',
        "amino_acid": "Glutamine"
    },
    "aat": {
        "letter": 'N',
        "abbreviation": 'Asn',
        "amino_acid": "Asparagine"
    },
    "aac": {
        "letter": 'N',
        "abbreviation": 'Asn',
        "amino_acid": "Asparagine"
    },
    "aaa": {
        "letter": 'K',
        "abbreviation": 'Lys',
        "amino_acid": "Lysine"
    },
    "aag": {
        "letter": 'K',
        "abbreviation": 'Lys',
        "amino_acid": "Lysine"
    },
    "gat": {
        "letter": 'D',
        "abbreviation": 'Asp',
        "amino_acid": "Aspartic acid"
    },
    "gac": {
        "letter": 'D',
        "abbreviation": 'Asp',
        "amino_acid": "Aspartic acid"
    },
    "gaa": {
        "letter": 'E',
        "abbreviation": 'Glu',
        "amino_acid": "Glutamic acid"
    },
    "gag": {
        "letter": 'E',
        "abbreviation": 'Glu',
        "amino_acid": "Glutamic acid"
    },
    "tgt": {
        "letter": 'C',
        "abbreviation": 'Cys',
        "amino_acid": "Cysteine"
    },
    "tgc": {
        "letter": 'C',
        "abbreviation": 'Cys',
        "amino_acid": "Cysteine"
    },
    "tga": {
        "letter": '*',
        "abbreviation": 'Sto',
        "amino_acid": "Stop"
    },
    "tgg": {
        "letter": 'W',
        "abbreviation": 'Trp',
        "amino_acid": "Tryptophan"
    },
    "cgt": {
        "letter": 'R',
        "abbreviation": 'Arg',
        "amino_acid": "Arginine"
    },
    "cgc": {
        "letter": 'R',
        "abbreviation": 'Arg',
        "amino_acid": "Arginine"
    },
    "cga": {
        "letter": 'R',
        "abbreviation": 'Arg',
        "amino_acid": "Arginine"
    },
    "cgg": {
        "letter": 'R',
        "abbreviation": 'Arg',
        "amino_acid": "Arginine"
    },
    "agt": {
        "letter": 'S',
        "abbreviation": 'Ser',
        "amino_acid": "Serine"
    },
    "agc": {
        "letter": 'S',
        "abbreviation": 'Ser',
        "amino_acid": "Serine"
    },
    "aga": {
        "letter": 'R',
        "abbreviation": 'Arg',
        "amino_acid": "Arginine"
    },
    "agg": {
        "letter": 'R',
        "abbreviation": 'Arg',
        "amino_acid": "Arginine"
    },
    "ggt": {
        "letter": 'G',
        "abbreviation": 'Gly',
        "amino_acid": "Glycine"
    },
    "ggc": {
        "letter": 'G',
        "abbreviation": 'Gly',
        "amino_acid": "Glycine"
    },
    "gga": {
        "letter": 'G',
        "abbreviation": 'Gly',
        "amino_acid": "Glycine"
    },
    "ggg": {
        "letter": 'G',
        "abbreviation": 'Gly',
        "amino_acid": "Glycine"
    }
}

def reverse_complement(sequence: str) -> str:
    base_pairs: dict[str, str] = {
        "a": "t",
        "t": "a",
        "g": "c",
        "c": "g"
    }
    sense_direction: str = sequence.lower()
    sense_reverse: str = sense_direction[::-1] # no built-in function to reverse. Use splicing in reverse direction.
    # print(sense_reverse)
    sense_reverse_complement: str = ""
    for letter in sense_reverse:
        sense_reverse_complement += base_pairs[letter]

    return sense_reverse_complement

def translation_helper(sequence: str) -> dict[str, str]:

    frames: list[str] = []
    i: int = 0
    while i < 3:
        translation: str = ""
        temp: str = sequence[i:].lower()
        start: int = 0
        end: int = start + 3
        while end <= len(temp):
            codon = temp[start:end]
            # print(end)
            # print(codon)
            translation += codons[codon]["letter"]
            start += 3
            end = start + 3

        frames.append(translation)
        i += 1

    return frames

def translate_dna(sequence: str) -> dict[str, str]:
    f1 = translation_helper(sequence)
    f2 = translation_helper(reverse_complement(sequence))
    f1 = f1 + f2
    frames: dict[str, str] = {}
    for i, seq in enumerate(f1):
        frames[f"f{i+1}"] = seq
    return frames

def main() -> None:
    temp: str = "ATCATCGATCGATCGTCTAGCTAGCTAGCTGCTAGCT"
    translated: str = translate_dna(temp)
    print(len(temp))
    print(translated)
    return

if __name__ == '__main__':
    main()