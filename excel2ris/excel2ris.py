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


def setup_logger():
    """Setup logger"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)


def get_input_arguments() -> dict:
    """Parse command line"""
    logger = logging.getLogger()
    parser = argparse.ArgumentParser()
    parser.formatter_class = argparse.RawDescriptionHelpFormatter

    parser.add_argument('-i', '--input_file', type=str, nargs=1,
                        help='Tab-separated file containing the crude data')
    # parser.add_argument('-d', '--data', type=str, nargs='+',
    #                     help='List of data to extract')
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as error:
        logger.error(str(error))
        sys.exit(2)

    input_data = dict.fromkeys(['input_file'])
    input_data['input_file'] = args.input_file
    return input_data


def csv_parser(input_file):
    """Parse tab-separated csv file exported from Excel"""

    # Blank bibliography
    bibliography = []

    # Setup reader
    reader = csv.reader(input_file, csv.excel_tab)
    # Ignore header
    reader.next()

    # Read lines
    for line in reader.next():
        bib_item = BibItem()
        bib_item.type = line['Type']
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
        self.__year = int()
        self.__keywords = list()
        
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
        elif value == "CSD Private Communication"
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
        self.__authors = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value

    def to_ris(self):
        pass


if __name__ == "__main__":
    main()
