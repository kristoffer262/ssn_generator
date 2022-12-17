from ssn_generator import GENERATE_SSN

ssn = GENERATE_SSN()
ssn.counts = 100
#ssn.dist_decade = {50: 1} # Get only persons born in the 50s
    
ssns = ssn.get_ssns()
print(ssns)
