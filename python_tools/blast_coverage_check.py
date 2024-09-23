import csv
import os
from argparse import ArgumentParser, Namespace

def blast_sequence_coverage(file: str, q_length: int) -> list[str] | None:
    coverage_gap: set = {x for x in range(1, q_length + 1)}
    temp_set: set = {}
    with open(file, 'r') as f:
        reader: csv.reader = csv.reader(f, delimiter=',')

        for line in reader:
            start: int = int(line[-2])
            end: int = int(line[-1])
            temp_set = {x for x in range(start, end + 1)}
            coverage_gap -= temp_set
    # print(coverage_gap)
    if len(coverage_gap) == 0:
        return None
    cov_gap_list: list[int] = list(coverage_gap)
    cov_gap_list.sort()
    largest_num : int = max(coverage_gap)
    gap_ranges: list[str] = []
    temp_range: str = f"{cov_gap_list[0]}"
    previous_num: int = cov_gap_list[0]
    for num in cov_gap_list[1:]:
        if previous_num + 1 != num:
            temp_range += '-' + str(previous_num)
            gap_ranges.append(temp_range)
            temp_range = str(num)

        if num == largest_num:
            temp_range += '-' + str(num)
            gap_ranges.append(temp_range)

        previous_num = num

    return gap_ranges

def dir_coverage_check(directory: str, q_length: int) -> dict[str, list]:

    files: list = os.listdir(directory)
    def filter_condition(file: str) -> str | None:
        return file if file.endswith(".out") else None

    files = list(filter(filter_condition, files))
    gaps_per_file: dict[str, list] = {}
    for file in files:
        coverage_gap: list[str] | None = blast_sequence_coverage(f"{directory}/{file}", q_length)
        if coverage_gap:
            gaps_per_file[file] = coverage_gap
    
    return gaps_per_file

def file_coverage_check(file: str, q_length: int) -> dict[str, list]:
    gaps: list[str] = blast_sequence_coverage(file, q_length)
    return gaps

def main() -> None:
    
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-f", "--file", help="Pass single csv file", type=str)
    group.add_argument("-d", "--dir", help="Pass directory with csv files", type=str)
    parser.add_argument("q_length", help="Length of the query sequence used to given blast output", type=int)

    args: Namespace = parser.parse_args()
    # print(args.q_length)
    gaps_per_file: dict[str, list] = {}
    if args.file:
        gaps_per_file[args.file.split('/')[-1]] = file_coverage_check(args.file, args.q_length)
    elif args.dir:
        gaps_per_file = dir_coverage_check(args.dir, args.q_length)
    else:
        parser.error("Please pass in a file-path with -f or directory with -d")

    print("Gaps in blast output coverage for the given csv files:")
    for k,v in gaps_per_file.items():
        print(f"{k}: {v}")

    return

if __name__ == '__main__':
    main()