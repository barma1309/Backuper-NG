import argparse  # arg parser

if "__name__" == "__main__":
    parser = argparse.ArgumentParser(description="Parser backup files")
    parser.add_argument("-y", dest="year_backup", help="date(year) which directory will parse", type=int, required=True)
    parser.add_argument("-m", dest="month", help="date(month) which directory will parse", type=int, required=True)
    parser.add_argument("-d", dest="debug", help="debug mode - input 1 for debug", type=int, required=False)

    args = parser.parse_args()
