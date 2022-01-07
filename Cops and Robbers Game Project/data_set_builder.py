"""DATA SET GENERATION: in this file we are generating the dataset that will use for our project.
As our project requires the type of location as well, we are manually categorising the locations."""

import csv
##########
# Readers: All csv files that need to be read for our dataset
##########

# this is to read the dataset Areas_of_Interest_Centroids.csv which contains several locations
# in NYC. For the purposes of our project, we have only chosen the locations which are either a park
# or a cemetery.
with open('Areas_of_Interest_Centroids.csv', 'r') as f1:
    reader1 = csv.DictReader(f1)

    # this is to read the dataset New_York_Tourist_Locations.csv which contains tourist spots of NYC
    with open('New_York_Tourist_Locations.csv', 'r') as f2:
        reader2 = csv.reader(f2)
        next(f2)  # we are skipping the first row of the dataset as it contains the
        # title for that column

        # this is to read the dataset rows.csv which stores the location of health care
        # centres in NYC
        with open('rows.csv', 'r') as f3:
            reader3 = csv.reader(f3)

            # this is to read the dataset FDNY_Firehouse_Listing.csv which contains the name of the
            # fire stations in NYC. The fire stations follow a naming convention of their
            # engine type and their ladder type
            with open('FDNY_Firehouse_Listing.csv', 'r') as f4:
                reader4 = csv.reader(f4)

                # this is to read the dataset NYPD_Hate_Crimes.csv which contains the names of the
                # precincts in NYC. As the precincts only have a numeric name, we decided to add
                # 'precinct' before each precinct number to read as, precinct 1, etc.
                with open('NYPD_Hate_Crimes.csv', 'r') as f5:
                    reader5 = csv.reader(f5)
                    next(f5)  # we are skipping the first row of the dataset as it contains the
                    # title for that column

                    ######
                    # The csv file that we are writing:
                    ######
                    # with open('my_csv.csv', 'w') as w:
                    with open('large_location_data.csv', 'w') as w:
                        writer = csv.writer(w)
                        for line in reader1:
                            if line['AnnoLine3'] == 'Park':
                                writer.writerow([line['Name'], 'park'])
                            if line['AnnoLine3'] == 'Cemetery':
                                writer.writerow([line['Name'], 'cemetery'])

                        for line in reader2:
                            writer.writerow([line[0], 'tourist spot'])

                        for line in reader3:
                            writer.writerow([line[2], 'health'])

                        for line in reader4:
                            writer.writerow([line[0], 'fire station'])

                        visited = set()  # the dataset is a record of hate crimes committed in NYC,
                        # and in which precinct they were reported in. There is a lot of repetition,
                        # in the precinct numbers so we decided to just extract the precinct using
                        # the visited method
                        for line in reader5:
                            if line[2] not in visited:
                                visited.add(line[2])
                                writer.writerow(['precinct ' + str(line[2]), 'police station'])
