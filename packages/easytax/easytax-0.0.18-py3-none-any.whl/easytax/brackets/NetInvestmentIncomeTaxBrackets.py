# Local Imports
from ..base import ProgressiveTax, ProgressiveTaxBracket

married_filing_jointly_tax = {
    # Source: https://www.irs.gov/taxtopics/tc559
    2022: ProgressiveTax.ProgressiveTax(
        ProgressiveTaxBracket.ProgressiveTaxBracket(
            tax_rates=[0, 0.038],
            income_thresholds=[250000])
        ),
    2023: ProgressiveTax.ProgressiveTax(
        ProgressiveTaxBracket.ProgressiveTaxBracket(
            tax_rates=[0, 0.038],
            income_thresholds=[250000])
        ),
    # Source: https://www.irs.gov/individuals/net-investment-income-tax
    2024: ProgressiveTax.ProgressiveTax(
        ProgressiveTaxBracket.ProgressiveTaxBracket(
            tax_rates=[0, 0.038],
            income_thresholds=[250000])
        ),
}

married_filing_separately_tax = {
    # Source: https://www.irs.gov/taxtopics/tc559
    2022: ProgressiveTax.ProgressiveTax(
        ProgressiveTaxBracket.ProgressiveTaxBracket(
            tax_rates=[0, 0.038],
            income_thresholds=[125000])
        ),
    # Source: https://www.irs.gov/taxtopics/tc559
    2023: ProgressiveTax.ProgressiveTax(
        ProgressiveTaxBracket.ProgressiveTaxBracket(
            tax_rates=[0, 0.038],
            income_thresholds=[125000])
        ),
    # Source: https://www.irs.gov/individuals/net-investment-income-tax
    2024: ProgressiveTax.ProgressiveTax(
        ProgressiveTaxBracket.ProgressiveTaxBracket(
            tax_rates=[0, 0.038],
            income_thresholds=[125000])
        ),
}

single_filer_tax = {
    # Source: https://www.irs.gov/taxtopics/tc559
    2022: ProgressiveTax.ProgressiveTax(
        ProgressiveTaxBracket.ProgressiveTaxBracket(
            tax_rates=[0, 0.038],
            income_thresholds=[200000])
        ),
    # Source: https://www.irs.gov/taxtopics/tc559
    2023: ProgressiveTax.ProgressiveTax(
        ProgressiveTaxBracket.ProgressiveTaxBracket(
            tax_rates=[0, 0.038],
            income_thresholds=[200000])
        ),
    # Source: https://www.irs.gov/individuals/net-investment-income-tax
    2024: ProgressiveTax.ProgressiveTax(
        ProgressiveTaxBracket.ProgressiveTaxBracket(
            tax_rates=[0, 0.038],
            income_thresholds=[200000])
        ),
}