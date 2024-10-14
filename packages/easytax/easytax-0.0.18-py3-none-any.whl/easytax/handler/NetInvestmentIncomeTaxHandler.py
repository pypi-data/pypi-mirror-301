# Local Imports
from ..brackets import NetInvestmentIncomeTaxBrackets
from . import RegionalTaxHandlerBase
from ..utils.InputValidator import InputValidator
from ..income.FederalIncomeHandler import FederalIncomeHandler
from ..utils.Constants import *


# Each handler can have its own AGI / MAGI
class NetInvestmentIncomeTaxHandler(RegionalTaxHandlerBase.RegionalTaxHandlerBase):
    def __init__(self, tax_year: int, filing_status: str, federal_income_handlers: list[FederalIncomeHandler]):
        """Create a NetInvestmentIncomeTaxHandler object.

        Keyword arguments:
        tax_year: int - The year for tax filling. 
        filing_status: str - The type of filling (Married Filing Jointly, Single, etc)
        federal_income_handlers: list[NetInvestmentIncomeHandler] - List of NetInvestmentIncomeHandler objects
        """
        
        InputValidator.validate_tax_year(tax_year)
        InputValidator.validate_filing_status(filing_status)

        self.tax_year = tax_year
        self.filing_status = filing_status
        self.total_incomes = [f.total_income for f in federal_income_handlers]
        self.taxable_incomes = [f.taxable_income for f in federal_income_handlers]
        self.long_term_capital_gains = [f.long_term_capital_gains for f in federal_income_handlers]
        self.region = "NetInvestmentIncome"

        self.income_tax_brackets = self._get_tax_brackets(tax_year, filing_status)
        
    @staticmethod
    def _get_tax_brackets(tax_year: int, filing_status: str):
        bracket_mapping = {
            MARRIED_FILING_JOINTLY: NetInvestmentIncomeTaxBrackets.married_filing_jointly_tax,
            MARRIED_FILING_SEPARATELY: NetInvestmentIncomeTaxBrackets.married_filing_separately_tax,
            SINGLE: NetInvestmentIncomeTaxBrackets.single_filer_tax,
        }
        
        if filing_status not in bracket_mapping:
            raise ValueError(f"Unsupported filing status: {filing_status}")
        
        year_brackets = bracket_mapping[filing_status]
        if tax_year not in year_brackets:
            raise ValueError(f"Unsupported tax year: {tax_year}")
        
        return year_brackets[tax_year]

