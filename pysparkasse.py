import csv
import argparse

def strip_long_spaces(input):
    loc = input.find("  ")
    if loc > 0:
        return input[:loc]
    return input

csv.register_dialect('sparkasse', delimiter=';', quoting=csv.QUOTE_ALL)
csv.register_dialect('ynab', delimiter=",", quoting=csv.QUOTE_MINIMAL)


parser = argparse.ArgumentParser(description='Convert Sparkasse CSV-CAMT files to YNAB compatible format.')
parser.add_argument('input', help='input file')
args = parser.parse_args()

with open(args.input) as csvfile:
    reader = csv.DictReader(csvfile, dialect="sparkasse")

    buff = []

    for row in reader:
        # Replace , with .
        row["Betrag"] = str.replace(row["Betrag"], ",", ".")

        # Replace long payee
        row["Beguenstigter/Zahlungspflichtiger"] = strip_long_spaces(row["Beguenstigter/Zahlungspflichtiger"])

        buff.append(row)

    with open("out.csv", "wb") as csvout:
        fieldnames_ynab = ["Date","Payee","Category","Memo","Outflow","Inflow"]
        writer = csv.DictWriter(csvout, dialect="ynab", fieldnames=fieldnames_ynab)
        writer.writeheader()
        for b in buff:
            entry = {}
            entry["Date"] = b["Buchungstag"]
            entry["Payee"] = b["Beguenstigter/Zahlungspflichtiger"]
            entry["Memo"] =  b["Verwendungszweck"]

            # parse value
            betrag = b["Betrag"]
            if (betrag.startswith("-")):
                entry["Outflow"] = betrag[1:]
            else:
                entry["Inflow"] = betrag

            writer.writerow(entry)
