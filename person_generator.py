from random import choice, choices, randint
from datetime import date, timedelta
import pandas as pd

class GENERATE_PERSONS:
    """
    Generates a number of SSNs with corresponding first- and lastname. 
    Use randomness for year and date of year
    TODO   
    * Should only be 18 years or older
    * Sanity check of numbers? Or complete check? Correct number of numbers

    Sources of information:
    https://skatteverket.se/privat/folkbokforing/personnummerochsamordningsnummer.4.3810a01c150939e893f18c29.html
    https://sv.wikipedia.org/wiki/Personnummer_i_Sverige
    https://www.scb.se/hitta-statistik/sverige-i-siffror/namnsok/
    """
    
    def __init__(self):
        """
        Init function.
        """

        self.counts = 1000 # Number of SSNs to generate
        self.manprop = 0.5 # Proportion of men in output
        self.numbers_odd = [1, 3, 5, 7, 9]
        self.numbers_even = [0, 2, 4, 6, 8]
        self.dist_decade = {30: 0.1, 
                            40: 0.1, 
                            50: 0.15, 
                            60: 0.15, 
                            70: 0.15, 
                            80: 0.15, 
                            90: 0.1, 
                            00: 0.1} # Distribution of SSNs per decade of birth
        self.names = self.load_names()


    def get_persons(self):
        """
        Takes self.counts and generates persons with SSN and firstname, lastname
        from the input distribution of names in Sweden.
        Return set of persons with SSNs.
        """

        persons = {}
        for ssn in self.get_ssns():
            woman = int(ssn[-2])%2
            firstname, lastname = self.get_random_name(woman)
            persons[ssn] = {"firstname": firstname,
                            "lastname": lastname,
                            "first_and_lastname": f"{firstname} {lastname}"}
        return persons


    def get_random_name(self, woman):
        """
        Takes input woman True(1)/False(0), and fetches a first- and lastname.
        Returns first- and lastname
        """
        
        if woman:
            firstname = choices(self.names["firstnames_woman"][0], weights=self.names["firstnames_woman"][1], k=1)[0]
        else:
            firstname = choices(self.names["firstnames_men"][0], weights=self.names["firstnames_men"][1], k=1)[0]
        lastname = choices(self.names["lastnames"][0], weights=self.names["lastnames"][1], k=1)[0]
        return firstname, lastname

    def get_ssns(self):
        """
        Takes self.counts and generates that number of independent SSNs.
        Return set of SSNs, to not provide duplicates.
        """

        dist_counts = self.get_decade_distribution_counts()
        ssns = []
        for decade, decades in dist_counts["decade"].items():
            for sex, sex_counts in decades.items():
                ssns += [self.get_one_ssn(sex, decade) for _ in range(decades[sex])]
        return set(ssns)


    def get_decade_distribution_counts(self):
        """
        Takes the distribution input and creates a dictionary with corresponding
        number of SSNs to create for each part.
        Return config-dictionary
        """

        # Get distributions
        dist_counts = {"decade": {}}
        # Dist_decade must sum to 1
        if not sum([y for x, y in self.dist_decade.items()]) == 1:
            return "Error, decade-distribution must sum  to 1.0"

        for decade, pct in self.dist_decade.items():
            dist_counts["decade"][decade] = {"man": None, "women": None}
            dist_counts["decade"][decade]["man"] = int(pct * self.counts * self.manprop)
            dist_counts["decade"][decade]["women"] = int((pct * self.counts)) - dist_counts["decade"][decade]["man"]
        return dist_counts


    def load_names(self):
        """
        Loads common last- and firstnames together with number of occurances in 
        Sweden according to SCB. Source https://www.scb.se/hitta-statistik/sverige-i-siffror/namnsok/.
        Return dictionary with lists of values.
        """
        
        names = {"lastnames": [], 
                "firstnames_men": [],
                "firstnames_woman": []}

        df_lastnames = pd.read_excel("namn-2021_20220404.xlsx", "Efternamn")
        df_men = pd.read_excel("namn-2021_20220404.xlsx", "Tilltalsnamn_men")
        df_woman = pd.read_excel("namn-2021_20220404.xlsx", "Tilltalsnamn_woman")
        names["lastnames"].append(df_lastnames["Efternamn"].to_list())
        names["lastnames"].append(df_lastnames["Antal"].to_list())
        names["firstnames_men"].append(df_men["Tilltalsnamn"].to_list())
        names["firstnames_men"].append(df_men["Antal"].to_list())
        names["firstnames_woman"].append(df_woman["Tilltalsnamn"].to_list())
        names["firstnames_woman"].append(df_woman["Antal"].to_list())
        return names 

    def get_one_ssn(self, sex, decade):
        """
        Function that initiates to get a ssn, calls methods to bring up a SSN.
        Return SSN
        """

        year = self.get_one_year(decade)
        date_pick = self.get_one_date_in_year()
        two_numbers = str(choice(range(100))).zfill(2)
        
        if sex == "man":
            third_number = choice(self.numbers_odd)
        else:
            third_number = choice(self.numbers_even)
        
        control_number = self.calculate_control_number(f"{year}{date_pick}{two_numbers}{third_number}")
        return f"{year}{date_pick}-{two_numbers}{third_number}{control_number}"


    def get_one_year(self, decade):
        """
        Takes decade, and pick random number from decade to decade + 10.
        Return random number
        """

        return str(choice(range(decade, decade+10))).zfill(2)


    def get_one_date_in_year(self):
        """
        Takes a random date from a given year that is not leapyear.
        Return random date without year in string format.
        """

        date_pick = date(2022, 1, 1) + timedelta(days=randint(0, 365))
        return date_pick.strftime("%m%d")


    def calculate_control_number(self, ninedigits):
        """
        Takes the first nine digits in SSN, and calculates the last digit in SSN.
        Return control number
        """

        calc_vector = [2, 1]*4
        calc_vector.append(2)
        
        multiply_nine_and_vector = [int(digit)*calc_vector[idx] for idx, digit in enumerate(ninedigits)]
        control_sum = 0
        for number in multiply_nine_and_vector:
            for digit in str(number):
                control_sum += int(digit)
        control_number = (10-(control_sum%10))%10
        return control_number




ssn = GENERATE_PERSONS()
ssn.counts = 100
#ssn.dist_decade = {50: 1} # Get only persons born in the 50s
    
#ssns = ssn.get_ssns()
#print(ssns)
#print(ssn.load_names())
persons = ssn.get_persons()
print(persons)