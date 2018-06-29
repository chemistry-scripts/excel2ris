#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018, E Nicolas
#
# --- Insert License Here ---

import argparse
import logging
import sys
import csv


def main():
    """Main function"""
    # Setup logging
    setup_logger()

    # Retrieve command-line args
    args = get_input_arguments()

    # Parse input file
    bibliography = parse_csv(args['input_file'], args['data_type'])

    # Create RIS format for every bibliography entry
    ris_entries = [bib.to_ris() for bib in bibliography]

    # Print the whole thing to a global RIS file
    write_ris(args['output_file'], ris_entries)


def write_ris(output_file, ris_entries):
    """Write all RIS entries to output file"""
    with open(output_file, mode='w', encoding='UTF-8') as out:
        for entry in ris_entries:
            print(entry)
    return


def setup_logger():
    """Setup logger"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return


def get_input_arguments():
    """Parse command line"""
    logger = logging.getLogger()
    parser = argparse.ArgumentParser()
    parser.formatter_class = argparse.RawDescriptionHelpFormatter

    parser.add_argument('-i', '--input_file', type=str, nargs=1,
                        help='Tab-separated file containing the crude data')
    parser.add_argument('-o', '--output_file', type=str, nargs=1,
                        help='Output-file in which to store the extracted data')
    parser.add_argument('-d', '--data_type', type=str, nargs=1,
                        help="ScientificProduction, Conferences, Grants, Dissemination and Others")
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as error:
        logger.error(str(error))
        sys.exit(2)

    input_data = dict.fromkeys(['input_file', 'output_file', 'data_type'])
    if args.input_file:
        input_data['input_file'] = args.input_file[0]
    else:
        logger.error("No input file")
        sys.exit(2)
    if args.output_file:
        input_data['output_file'] = args.output_file[0]
    else:
        logger.error("No output file")
        sys.exit(2)
    if args.data_type:
        input_data['data_type'] = args.data_type[0]
    else:
        logger.error("No data type selected")
        sys.exit(2)
    return input_data


def parse_csv(input_file, data_type):
    """Parse tab-separated csv file exported from Excel"""
    logger = logging.getLogger()
    # Blank bibliography
    bibliography = []
    logger.debug(input_file)
    with open(input_file, mode='r', encoding='cp1252') as in_file:
        # Setup reader
        reader = csv.reader(in_file, delimiter=';')
        # Skip header
        reader.__next__()
        # Read lines
        for row in reader:
            bib_item = BibItem()
            if data_type == 'ScientificProduction':
                bib_item.type = row[0]
                bib_item.title = row[1]
                bib_item.authors = row[2]
                bib_item.year = row[3]
                if row[4]:
                    bib_item.number = row[4]
                bib_item.institution = row[5]
            elif data_type == 'Conferences':
                bib_item.type = row[0]
                bib_item.title = row[1]
                bib_item.conference_name = row[2]
                bib_item.location = row[3]
                bib_item.authors = row[4]
                bib_item.year = row[5]
                bib_item.month = row[6]
            elif data_type == 'Grants':
                bib_item.type = row[0]
                bib_item.title = row[1]
                bib_item.authors = row[2]
                bib_item.keywords = row[3]
                bib_item.year = row[4]
                bib_item.number = row[5]
                bib_item.institution = row[6]
            elif data_type == 'Dissemination':
                bib_item.type = row[0]
                bib_item.title = row[1]
                bib_item.authors = row[2]
                bib_item.year = row[3]
                bib_item.location = row[4]
                bib_item.comments = row[5]
            elif data_type == 'Others':
                bib_item.type = row[0]
                bib_item.title = row[1]
                bib_item.authors = row[2]
                bib_item.year = row[3]
                bib_item.location = row[4]
                bib_item.comments = row[5]
            else:
                logger.error('Unrecognized file type')
                sys.exit(2)
            bibliography.append(bib_item)

    return bibliography


class BibItem:
    """
    Class that describes a bibliography item, with getters and setters
    """

    def __init__(self):
        """Build the object"""
        self.__type = ""
        self.__authors = list()
        self.__title = ""
        self.__year = int()
        self.__keywords = list()
        self.__number = ""
        self.__institution = ""
        self.__conference_name = ""
        self.__location = ""
        self.__comments = list()

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, value):
        self.__comments.append(value)

    @property
    def keywords(self):
        return self.__keywords

    @keywords.setter
    def keywords(self, value):
        self.__keywords.append(value)

    @property
    def conference_name(self):
        return self.__conference_name

    @conference_name.setter
    def conference_name(self, value):
        self.__conference_name = value

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        self.__location = value

    @property
    def institution(self):
        return self.__institution

    @institution.setter
    def institution(self, value):
        self.__institution = value

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        self.__number = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, value):
        # Set the type and potential keywords depending on value
        # --- 1 --- Conferences
        if value == "Invited (Conference)":
            self.__type = "CPAPER"
            self.__keywords.append("Invited Conference")
        elif value == "Invited (Workshop)":
            self.__type = "CPAPER"
            self.__keywords.append("Invited Workshop")
        elif value == "Invited (Lab)":
            self.__type = "CPAPER"
            self.__keywords.append("Invited Seminar")
        elif value == "Selected (Conference)":
            self.__type = "CPAPER"
            self.__keywords.append("Conference")
        elif value == "Selected (Workshop)":
            self.__type = "CPAPER"
            self.__keywords.append("Workshop")
        elif value == "Poster":
            self.__type = "CPAPER"
            self.__keywords.append("Poster")
        # --- 2 --- Patents, Thesis, Reports, etc.
        elif value == "Patent":
            self.__type = "PAT"
        elif value == "PhD Thesis":
            self.__type = "THES"
            self.__keywords.append("PhD Thesis")
        elif value == "HDR Thesis":
            self.__type = "THES"
            self.__keywords.append("HDR Thesis")
        elif value == "Report":
            self.__type = "RPRT"
        # --- 3 --- Prizes, Grants, etc.
        elif value == "Prize":
            self.__type = "GRANT"
            self.__keywords.append("Prize")
        elif value == "Grant":
            self.__type = "GRANT"
            # TODO: Include Grant role somewhere
            self.__keywords.append("Grant")
        elif value == "Travel Grant":
            self.__type = "GRANT"
            self.__keywords.append("Travel Grant")
        # --- 4 --- Dissemination
        elif value == "Article":
            self.__type = "MGZN"
            self.__keywords.append("Dissemination")
        elif value == "Conference":
            self.__type = "CPAPER"
            self.__keywords.append("Dissemination")
        elif value == "High-school":
            self.__type = "CPAPER"
            self.__keywords.append("Dissemination")
        elif value == "TV/Radio":
            self.__type = "GEN"
            self.__keywords.append("Dissemination")
            self.__keywords.append("TV Radio")
        elif value == "Video":
            self.__type = "GEN"
            self.__keywords.append("Dissemination")
            self.__keywords.append("Video")
        elif value == "Website page":
            self.__type = "ELEC"
            self.__keywords.append("Dissemination")
            self.__keywords.append("Web page")
        # --- 5 --- Others
        elif value == "Computer Program":
            self.__type = "COMP"
        elif value == "CSD Private Communication":
            self.__type = "GEN"
            self.__keywords.append("CSD Private Communication")
        elif value == "Conference Organization":
            self.__type = "GEN"
            self.__keywords.append("Conference Organization")
        elif value == "Jury/Committee Participation":
            self.__type = "GEN"
            self.__keywords.append("Jury/Committee Participation")
        elif value == "Others":
            self.__type = "GEN"
            self.__keywords.append("Others")
        else:
            logging.error("Unrecognized value: " + value)

    @property
    def authors(self):
        return self.__authors

    @authors.setter
    def authors(self, value):
        self.__authors.append(value)

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value

    def to_ris(self):
        ris_text = list()
        ris_text.append('TY  - ' + self.type)
        ris_text.append('AU  - ' + self.authors[0])
        ris_text.append('TI  - ' + self.title)
        ris_text.append('YE  - ' + str(self.year))
        ris_text.append('KW  - ') + '; '.join(self.keywords)

        if self.type == 'PAT':
            ris_text.append('IS  - ' + self.number)
            ris_text.append('PB  - ' + self.institution)
        elif self.type == 'THES':
            ris_text.append('PB  - ' + self.institution)
        elif self.type == 'RPRT':
            ris_text.append('PB  - ' + self.institution)
        elif self.type == 'CPAPER':
            ris_text.append('CY  - ' + self.location)
            ris_text.append('T2  - ' + self.conference_name)
        ris_text.append('RE  - ')
        return ris_text


if __name__ == "__main__":
    main()
