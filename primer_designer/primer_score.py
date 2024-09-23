import json
from primer_class import Primer

def variables_access(file_path):
    with open(file_path, "r") as file:
        primer_variables = json.load(file)

    return primer_variables
    
def primer_score_calc(primer, args):
    primer_score = 0
        
    if primer.length in range(args["primerLengthLow"], args["primerLengthHigh"]):
        primer_score += 2

    if int(primer.gc_percentage) in range(args["gcPercentLow"], args["gcPercentHigh"]):
        primer_score += 2

    if primer.last_nucleotide_check():
        primer_score += 2

    if int(primer.melting_temperature) in range(args["meltingTempLow"], args["meltingTempHigh"]):
        primer_score += 2

    if primer.homopolymer_check() >= args["homoPolymerLength"]:
        primer_score -= 2

    if primer.hairpin_check() > args["hairpinPercentage"]:
        primer_score -= 2

    if primer.primer_dimer_check() > args["primerDimerPercentage"]:
        primer_score -= 1
    
    return primer_score

def main():
    file_path = "variables.json"
    input_variables = variables_access(file_path)
    print(input_variables)
    test = Primer("TDSP1712", "tgaggccgccatccacgc", "reverse")
    primer_score = primer_score_calc(test, input_variables)
    print(f"Primer score for {test.name} is {primer_score}")
    return 0

if __name__ == '__main__':
    main()