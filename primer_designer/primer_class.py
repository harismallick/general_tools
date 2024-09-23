import math
## Reference for primer conditions to design or select optimal primers: https://dnacore.mgh.harvard.edu/new-cgi-bin/site/pages/sequencing_pages/primer_design.jsp

class Primer():

    def __init__(self, name, sequence, orientation="forward"):
        """ Initialize a primer object that binds to a given DNA sequence with a name, DNA sequence and the DNA strand to which the primer binds. By default, the binding is set to the forward strand."""

        self.primer_name = name
        self.primer_sequence = sequence.lower()
        self._orientation = orientation

    def __repr__(self):
        return f"Name: {self.primer_name}\nSequence: {self.primer_sequence}\nBinding Strand: {self.orientation}"
    
    def __iter__(self):
        """ Iterate over the nucleotides in the primer sequence of the Primer object """
        for nucleotide in self.primer_sequence:
            yield nucleotide
    
    @property
    def name(self):
        return self.primer_name
    
    @property
    def length(self):
        return len(self.primer_sequence)
    
    @property
    def sequence(self):
        return self.primer_sequence
    
    @property
    def orientation(self):
        return self._orientation
    
    @orientation.setter
    def orientation(self, bound_orientation: str):
        """Set orientation to 'reverse' if the primer binds to the antisense strand."""
        self._orientation = bound_orientation
    
    @property
    def gc_count(self):
        sequence = self.primer_sequence
        gc_count = 0
        for nucleotide in sequence:
            if nucleotide in ("g", "c"):
                gc_count += 1

        return gc_count
    
    @property
    def gc_percentage(self):
        """ Calculate the % of nucleotides in the primer sequence that are either guanine or cytosine """
            
        gc_percentage = round((self.gc_count/len(self.primer_sequence)), 4)

        return round(gc_percentage*100, 2)
    
    @property
    def melting_temperature(self):
        """ Calculate the melting temperature of the primer in Celcius """
        sequence = self.primer_sequence

        gc_count = self.gc_count
        at_count = self.length - gc_count

        if self.length <= 14:
            # Formula 1:
            melting_temp = (2*at_count) + (4*gc_count)
            # Formula 1 only works for oligos shorter than 14 bp.

        else:
        # Formula 2:
            melting_temp = 64.9 + ((41*(gc_count - 16.4))/self.length)
        ## Formula 2 gave similar numbers to the IDT oligo analyser tool under ideal conditions.
        # Formula 3 does not skew the numbers as bad under low GC% and long length conditions.

        # Formula 3:
        # melting_temp = 81.5 + (0.41*gc_count) - 675/len(sequence)
        ## Formula 3 gave comparable numbers (+/- 5 Celcius) to IDT tool: https://eu.idtdna.com/calc/analyzer
        # This formula becomes the most inaccurate for long oligos (>30 bases) with low GC% (<40%)

        # Formula 4:
        # melting_temp = 81.5 + ((41*gc_count)/len(sequence)) - (675/len(sequence)) + (16.6 * math.log(0.05, 10))#

        melting_temp_rounded = round(melting_temp, 2)

        return melting_temp_rounded
      
    @staticmethod
    def base_complement(nucleotide):
        base_pairs = {
            "a": "t",
            "t": "a",
            "g": "c",
            "c": "g"
        }
        return base_pairs[nucleotide]

    def reverse_complement(self):
        
        sense_direction = self.primer_sequence.lower()
        sense_reverse = sense_direction[::-1] # no built-in function to reverse. Use splicing in reverse direction.
        # print(sense_reverse)
        sense_reverse_complement = ""
        for letter in sense_reverse:
            complement = self.base_complement(letter)
            sense_reverse_complement += complement

        return sense_reverse_complement
    
    def homopolymer_check(self):
        sequence = self.primer_sequence

        last_nucleotide = ""
        current_nt_count = 1
        max_nt_count = 1
        for letter in sequence:
            if letter == last_nucleotide:
                current_nt_count += 1

            elif letter != last_nucleotide:
                current_nt_count = 1

            if max_nt_count < current_nt_count:
                max_nt_count = current_nt_count

            last_nucleotide = letter

        # Homopolymeric stretch in primers should not exceed 6 nucleotides        
        return max_nt_count
    
    def last_nucleotide_check(self):
        last_nucleotide = self.primer_sequence[len(self.primer_sequence)-1]

        if last_nucleotide in ("g", "c"):
            return True
        
        return False

    def hairpin_check(self):

        sequence = self.sequence
        length = len(sequence)
        
        max_hairpin = 0
        for index, _ in enumerate(sequence):
            i = index
            j = len(sequence)-1
            hairpin_length = 0
            hairpin_sequence = ""

            while j > i:
                x = sequence[i]
                y = sequence[j]
                if self.base_complement(x) == y:
                    hairpin_length += 1
                    i += 1
                    hairpin_sequence = hairpin_sequence + x

                elif self.base_complement(x) != y and hairpin_length != 0:
                    if max_hairpin < hairpin_length:
                        max_hairpin = hairpin_length

                    hairpin_length = 0
                    hairpin_sequence = ""

                if max_hairpin < hairpin_length:
                    max_hairpin = hairpin_length

                j -= 1
            # print(hairpin_sequence)

        # print(max_hairpin)
        hairpin_percentage = (2 * max_hairpin) / length * 100
        
        return round(hairpin_percentage, 2)
    
    def primer_dimer_check(self):
        seq = self.primer_sequence
        seq_reverse = seq[::-1]
        dimer_array = []

        for letter in seq_reverse:
            row = []
            for sense_letter in seq:
                letter_pairs = []
                letter_pairs.append(sense_letter)
                letter_pairs.append(letter)
                row.append(letter_pairs)

            dimer_array.append(row)

        # for row in dimer_array:
        #     for column in row:
        #         print(column, end=" ")

        #     print()
        # print(dimer_array)

        current_row = len(dimer_array) - 1
        current_column = 0
        row_increment = 0
        column_increment = 0
        dimer_length = 0
        overlap_length = 0
        max_dimer = 0
        max_dimer_overlap = 0
        switch = False
        while current_row >= 0 and current_column < len(dimer_array[0]):

            while current_row + row_increment < len(dimer_array) and current_column + column_increment < len(dimer_array[0]):
                if dimer_array[current_row + row_increment][current_column + column_increment][0] == self.base_complement(dimer_array[current_row + row_increment][current_column + column_increment][1]):
                    dimer_length += 1
                    # print(dimer_array[current_row + row_increment][current_column + column_increment][0])

                overlap_length += 1
                row_increment += 1
                column_increment += 1

            if max_dimer < dimer_length:
                max_dimer = dimer_length
                max_dimer_overlap = overlap_length

            if switch:
                current_column += 1
            else:    
                current_row -= 1

            row_increment = 0
            column_increment = 0
            dimer_length = 0
            overlap_length = 0
            
            if current_row == 0:
                switch = True

        dimer_percentage = round((max_dimer/max_dimer_overlap*100), 2)

        # return max_dimer, max_dimer_overlap
        return dimer_percentage
    
    def primer_qc_check(self):
        """Check to ensure all the letters in the primer nucleotide sequence are in ('a','g','c','t')."""

        for letter in self.sequence:
            if letter not in ('a','g','c','t'):
                return False
            
        return True
    
    # @property
    # def primer_score(self):
    #     """ Based on all the properties of the primer, giving it a score if it fulfills specified length, GC%, Tm, hairpin and primer-dimer check conditions"""

    #     primer_score = 0
        
    #     if self.length in range(16, 30):
    #         primer_score += 2

    #     if int(self.gc_percentage) in range(40, 60):
    #         primer_score += 2

    #     if self.last_nucleotide_check():
    #         primer_score += 2

    #     if int(self.melting_temperature) in range(45, 65):
    #         primer_score += 2

    #     if self.homopolymer_check() >= 6:
    #         primer_score -= 2

    #     if self.hairpin_check() > 60:
    #         primer_score -= 2

    #     if self.primer_dimer_check() > 75:
    #         primer_score -= 1
        
    #     return primer_score


    
def main():
    test = Primer("TDSP1712", "tgaggccgccatccacgc", "reverse") # acttggcagtacatctacgtattagtcatcgctatta
    print(f"length: {test.length}")
    print(f"gc%: {test.gc_percentage}")
    print(f"Is G/C last NT? {test.last_nucleotide_check()}")
    print(f"Melting temp: {test.melting_temperature}")
    print(f"Homopolymer length: {test.homopolymer_check()}")
    # print(test.reverse_complement())
    # print(test.last_nucleotide_check())
    print(f"Hairpin check result: {test.hairpin_check()}")
    print(f"Primer dimer check: {test.primer_dimer_check()}")
    print(f"Total primer score: {test.primer_score}")

if __name__ == "__main__":
    main()