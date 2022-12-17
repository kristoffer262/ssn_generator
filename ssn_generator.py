from random import choice, randint
from datetime import date, timedelta

class GENERATE_SSN:
    """
    Generates a number of SSNs. Use randomness for year and date of year
    TODO   
    * Should only be 18 years or older
    * Sanity check of numbers? Or complete check? Correct number of numbers

    Sources of information:
    https://skatteverket.se/privat/folkbokforing/personnummerochsamordningsnummer.4.3810a01c150939e893f18c29.html
    https://sv.wikipedia.org/wiki/Personnummer_i_Sverige        
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


    def get_ssns(self):
        """
        Takes self.counts and generates that number of independent SSNs.
        Return set of SSNs, to not provide duplicates.
        """

        dist_counts = self.get_distribution_counts()
        ssns = []
        for decade, decades in dist_counts["decade"].items():
            for sex, sex_counts in decades.items():
                ssns += [self.get_one_ssn(sex, decade) for _ in range(decades[sex])]
        return set(ssns)


    def get_distribution_counts(self):
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
