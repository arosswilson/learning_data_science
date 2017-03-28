import sys, csv, os


class Record(object):
    """Represents a row"""

class Case(Record):
    """Represents a case from Force"""

class Table(object):
    """list of objects"""

    def __init__(self):
        self.records = []

    def __len__(self):
        return len(self.records)

    def ReadFile(self, data_dir, filename, constructor, n=None):
        """ Reads a file and makes a object for each row

        Args:
            data_dir: string directory name
            filename: string name of the file
            fields: sequence of (name, start, end, case) tuples specifying the fields to extract

            constructor: what kind of object to create
        """

        filename = os.path.join(data_dir, filename)
        with open(filename, 'r') as f:
            sheet = csv.DictReader(f)

            for i, row in enumerate(sheet):
                if i == n:
                    break

                record = self.MakeRecord(row, constructor)
                self.AddRecord(record)

    def MakeRecord(self, row, constructor):
        """ Takes the csv row and returns and object with fields

        Args:
            line: line number of row
            fields: sequence of (name, start, end, case) tuples specifying the fields to extract
            constructor: callable that makes an object for the record

        return:
            record with fields defined by columns in csv
        """

        obj = constructor()
        for title, value in row.items():
            try:
                val = float(value)
            except:
                val = value


            if val == 'FALSE':
                val = False
            elif val == 'TRUE':
                val = True

            title = title.strip().lower().replace(' ', '_')
            
            setattr(obj, title, val)

        return obj

    def AddRecord(self, record):
        """adds a record to its Table

        Args:
            record: and object of one of the record types
        """
        self.records.append(record)

    def ExtendRecords(self, records):
        """ Adds records to this Table

        Args:
            records: an iterable of record obj

        """
        self.recrods.extend(records)

    def Recode(self):
        """ Child classes can override this to recode values"""
        pass

class Cases(Table):
    """Represents the cases Table. """

    def ReadRecords(self, data_dir='.', n=None):
        filename = self.GetFilename()
        self.ReadFile(data_dir, filename, Case, n)
        self.Recode()

    def GetFilename(self):
        return 'force_connectivity_report.csv'

    def get_number_of_sms_cases(self):
        return len([case for case in self.records if case.accepted_sms])

    def average_percent_of_outcomes_submitted(self):
        percent = float(0)
        for case in self.records:
            percent += case.percent_outcomes_submitted
            print(case.percent_outcomes_submitted)
        return float(percent/len(self.records))


def main(name, data_dir='.'):
    cases = Cases()
    cases.ReadRecords(data_dir)

    print('Number of cases %s'% len(cases.records))
    print('number of cases accepted sms: %s'% cases.get_number_of_sms_cases())
    print('avg outcomes submitted: %s'% cases.average_percent_of_outcomes_submitted())

if __name__ == '__main__':
    main(*sys.argv)








