################################################################################
#   Salary          s   ~20,000
#   Tax rate        t   0.4
#   Earn ratio      e   0.1
#   Penalty rate    p   0.1
#   Number of year  N   
################################################################################
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class _401k_():
    def __init__( self, salary, taxrate, earnrate, penaltyrate ):
        self.salary     = salary
        self.taxrate    = taxrate
        self.earnrate   = earnrate
        self.penaltyrate= penaltyrate
    
    def compute( self, n ):
        #   s * {[1-(1+e)**(n)]/[1-(1+e)]}  # n>=1, means to take the money out at least from year 2
        total   = self.salary * ( ( (1+self.earnrate)**n -1 )/self.earnrate  )  #   total earnings plus earnings
        tax     = total * self.taxrate                          #   tax to pay before 59.5 if withdraw
        penalty = (total - tax) * self.penaltyrate
        remain  = total - tax - penalty
        
        return int(total), int(remain)


class _roth_():
    def __init__( self, salary, taxrate, earnrate, penaltyrate ):
        self.salary     = salary
        self.taxrate    = taxrate
        self.earnrate   = earnrate
        self.penaltyrate= penaltyrate
    
    def compute( self, n ):
        #   s * (1-t) * {[1-(1+e)**(n)]/[1-(1+e)]}
        total   = self.salary * (1 - self.taxrate) * ( ( (1+self.earnrate)**n -1 )/self.earnrate )  #   total earnings plus earnings
        base    = self.salary * (1 - self.taxrate) * n                                   # the salary part, which is also the taxed part
        earning = total - base
        earn_tax= earning * self.taxrate                            #   tax to pay before 59.5 if withdraw
        penalty = (earning - earn_tax) * self.penaltyrate
        remain  = total - earn_tax - penalty

        # if this account is older than 5 years
        year5   = total - earning*self.penaltyrate

        return int(total), int(remain), int(year5)


class _stock_():
    def __init__( self, salary, taxrate, earnrate ):
        self.salary     = salary
        self.taxrate    = taxrate
        self.earnrate   = earnrate
    
    def compute( self, year ):
        account = 0
        for y in range(year):
            new_invest      = self.salary * (1 - self.taxrate)
            earn_per_year   = (account + new_invest)*self.earnrate*(1-self.taxrate)
            account         = account + new_invest + earn_per_year
        
        return int(account)

def main():

    salary      = 20000
    taxrate     = 0.3
    earnrate    = 0.15
    penaltyrate = 0.1
    matchrate   = 1.5   

    _401k = _401k_(salary,              taxrate, earnrate, penaltyrate)
    match = _401k_(salary*matchrate,    taxrate, earnrate, penaltyrate)
    _roth = _roth_(salary,              taxrate, earnrate, penaltyrate)
    stock = _stock_(salary,             taxrate, earnrate)

    _401k_total =   []
    _401k_early =   []
    match_total =   []
    match_early =   []
    _roth_total =   []
    _roth_early =   []
    _roth_5year =   []
    stock_all   =   []   

    years = range(1,20)

    for year in years:
        total, early = _401k.compute(year)
        _401k_total.append(total)
        _401k_early.append(early)

        total, early = match.compute(year)
        match_total.append(total)
        match_early.append(early)

        total, early, year5 = _roth.compute(year)
        _roth_total.append(total)
        _roth_early.append(early)  
        _roth_5year.append(year5)

        total       = stock.compute(year)
        stock_all.append(total)

    print(match_total)
    print(match_early)
    print(_401k_total)
    print(_401k_early)
    print(_roth_total)
    print(_roth_early)
    print(stock_all)

    '''
    '''

    #fig = plt.figure()# num=None, figsize=(16, 9), dpi=400 ) 
    #   plt.plot( years, match_total,   'r^-.', label='match_total')
    #   plt.plot( years, match_early,   'rv-.', label='match_early')     
    plt.plot( years, _401k_total,   'b^-',  label='401k_total')
    plt.plot( years, _401k_early,   'bv-',  label='401k_early')
    plt.plot( years, _roth_total,   'k^--', label='roth_total')
    plt.plot( years, _roth_early,   'kv--', label='roth_early')
    plt.plot( years, _roth_5year,   'ko--', label='roth_5year')
    plt.plot( years, stock_all,     'ys-.',  label='stock')

    plt.grid(b=None, which='both', axis='both')

    plt.legend(loc='center left')
    plt.show()


if __name__ == '__main__':
    main()
