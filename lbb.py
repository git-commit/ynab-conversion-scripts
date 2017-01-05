import csv
import argparse

def main():
    csv.register_dialect('sparkasse', delimiter=';', quoting=csv.QUOTE_ALL)
    csv.register_dialect('lbb', delimiter=';')
    csv.register_dialect('ynab', delimiter=",", quoting=csv.QUOTE_MINIMAL)


    parser = argparse.ArgumentParser(description='Convert LBB CSV files to YNAB compatible format.')
    parser.add_argument('input', help='input file')
    args = parser.parse_args()

    buff = []

    with open(args.input) as csvfile:
        reader = csv.reader(csvfile, dialect="lbb")

        for row in reader:
            # skip empty rows
            if not len(row) is 7:
                continue
            # skip rows without a charge
            if not any(char.isdigit() for char in row[6]):
                continue
            # Replace , with .
            row[6] = str.replace(row[6], ",", ".")
            print(row)

            buff.append(row)


    output_filename = args.input[:-4] + "-ynab.csv"
    with open(output_filename, "wb") as csvout:
        fieldnames_ynab = ["Date","Payee","Category","Memo","Outflow","Inflow"]
        writer = csv.DictWriter(csvout, dialect="ynab", fieldnames=fieldnames_ynab)
        writer.writeheader()
        for b in buff:
            entry = {}
            entry["Date"] = b[2]
            entry["Payee"] = b[3]

            # parse value
            betrag = b[6]
            if (betrag.startswith("-")):
                entry["Outflow"] = betrag[1:]
            else:
                entry["Inflow"] = betrag

            writer.writerow(entry)

def strip_long_spaces(input):
    loc = input.find("  ")
    if loc > 0:
        return input[:loc]
    return input

if __name__ == '__main__':
    main()