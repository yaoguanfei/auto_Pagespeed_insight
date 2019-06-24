import csv


def read_csv1(file):
    with open(file, 'r') as f:
        results = f.readlines()
        print(results)

    results = results[1:]
    csvresult = []
    for result in results:
        resu = result.strip('\n')
        resu = result.split(",")
        csvresult.append(resu)
    print(csvresult)
    return csvresult


def read_csv2(file):
    with open(file, "r") as f:
        reader = csv.reader(f)
        csvresult = [row for row in reader]
        csvresult = csvresult[1:]
    print(csvresult)
    return csvresult


if __name__ == '__main__':
    csvresult = read_csv1("webdata.csv")
    csvresult = read_csv2("webdata.csv")
