import pandas as pd
import yfinance as yf
import datetime 
import os

def get_statements(symbol):
    ticker = yf.Ticker(symbol)
    # Retrieve statements (yearly)
    income_statement = ticker.financials.reset_index()
    balance_sheet = ticker.balance_sheet.reset_index()
    cashflow = ticker.cashflow.reset_index()

    # Retrieve statements (quarterly)
    income_statement_quarterly = ticker.quarterly_financials.reset_index()
    balance_sheet_quarterly = ticker.quarterly_balance_sheet.reset_index()
    cashflow_quarterly = ticker.quarterly_cashflow.reset_index()

    return (income_statement, balance_sheet, cashflow, 
            income_statement_quarterly, balance_sheet_quarterly, 
            cashflow_quarterly)

def get_statement_value(statement, key):
    if key in statement['index'].values:
        value = statement.loc[statement['index'] == key].iloc[0, 1:]
    else:
        # Return a Series of zeros with the appropriate columns
        value = pd.Series([0]* (statement.shape[1]-1), index=statement.columns[1:])
    return value

def return_razon(razon, columns, en_name, es_name):
    razon_df = pd.DataFrame([razon], columns=columns)
    razon_df['KPI'] = en_name
    columns = ['KPI'] + [col for col in razon_df.columns if col != 'KPI']
    razon_df = razon_df[columns]
    razon_df_es = razon_df.copy().reset_index(drop = True)
    razon_df_es.loc[0, 'KPI'] = es_name
    return razon_df.reset_index(drop = True), razon_df_es.reset_index(drop = True)

def calculate_ratio(numerator_key, denominator_key, numerator_statement, denominator_statement, en_name, es_name):
    numerator = get_statement_value(numerator_statement, numerator_key)
    denominator = get_statement_value(denominator_statement, denominator_key)
    denominator = denominator.replace(0, pd.NA)  # Avoid division by zero
    ratio = numerator / denominator
    ratio_df_en, ratio_df_es = return_razon(ratio, numerator_statement.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def debt_to_equity_f(balance_sheet):
    en_name = 'Debt to Equity'
    es_name = 'Deuda a capital contable'
    return calculate_ratio('Total Debt', 'Total Capitalization', balance_sheet, balance_sheet, en_name, es_name)

def debt_to_total_assets_ratio_f(balance_sheet):
    en_name = 'Debt to Total Assets Ratio'
    es_name = 'Deuda a activos totales'
    return calculate_ratio('Total Debt', 'Total Assets', balance_sheet, balance_sheet, en_name, es_name)

def interest_coverage_ratio_f(income_statement):
    en_name = 'Interest Coverage Ratio'
    es_name = 'Cobertura de Interés'
    return calculate_ratio('EBIT', 'Interest Expense', income_statement, income_statement, en_name, es_name)

def cfcr_f(cashflow):
    free_cash = get_statement_value(cashflow, 'Free Cash Flow')
    rep_debt = get_statement_value(cashflow, 'Repayment Of Debt').abs()
    ratio = free_cash / rep_debt.replace(0, pd.NA)
    en_name = 'Flow Coverage Ratio'
    es_name = 'Cobertura de Flujo'
    ratio_df_en, ratio_df_es = return_razon(ratio, cashflow.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def dcr_f(cashflow, balance_sheet):
    op_cf = get_statement_value(cashflow, 'Operating Cash Flow')
    total_debt = get_statement_value(balance_sheet, 'Total Debt')
    ratio = op_cf / total_debt.replace(0, pd.NA)
    en_name = 'Debt Coverage Ratio'
    es_name = 'Cobertura de Deuda'
    ratio_df_en, ratio_df_es = return_razon(ratio, cashflow.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def quick_ratio_f(balance_sheet):
    en_name = 'Quick Ratio'
    es_name = 'Prueba de Liquidez'
    return calculate_ratio('Current Assets', 'Current Liabilities', balance_sheet, balance_sheet, en_name, es_name)

def acid_ratio_f(balance_sheet):
    if 'Inventory' not in balance_sheet['index'].values:
        # Inventory not found, skip this ratio
        return None, None
    current_assets = get_statement_value(balance_sheet, 'Current Assets')
    inventory = get_statement_value(balance_sheet, 'Inventory')
    current_liabilities = get_statement_value(balance_sheet, 'Current Liabilities').replace(0, pd.NA)
    acid_ratio = (current_assets - inventory) / current_liabilities
    en_name = 'Acid Ratio'
    es_name = 'Prueba del Ácido'
    ratio_df_en, ratio_df_es = return_razon(acid_ratio, balance_sheet.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def immediate_liquidity_ratio_f(cashflow, balance_sheet):
    end_cash_position = get_statement_value(cashflow, 'End Cash Position')
    current_liabilities = get_statement_value(balance_sheet, 'Current Liabilities').replace(0, pd.NA)
    ilr = end_cash_position / current_liabilities
    en_name = 'Immediate Liquidity Ratio'
    es_name = 'Liquidez Inmediata'
    ratio_df_en, ratio_df_es = return_razon(ilr, cashflow.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def margin_of_safety_f(balance_sheet):
    working_capital = get_statement_value(balance_sheet, 'Working Capital')
    current_liabilities = get_statement_value(balance_sheet, 'Current Liabilities').replace(0, pd.NA)
    maosa = working_capital / current_liabilities
    en_name = 'Margin of Safety Ratio'
    es_name = 'Margen de Seguridad'
    ratio_df_en, ratio_df_es = return_razon(maosa, balance_sheet.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def defensive_interval_ratio_f(cashflow, income_statement, balance_sheet):
    end_cash_position = get_statement_value(cashflow, 'End Cash Position')
    investments_and_advances = get_statement_value(balance_sheet, 'Investments And Advances')
    if investments_and_advances.sum() == 0:
        investments_and_advances = get_statement_value(balance_sheet, 'Other Non Current Assets')
    accounts_receivable = get_statement_value(balance_sheet, 'Accounts Receivable')
    numerator = end_cash_position + investments_and_advances + accounts_receivable

    # Get Operating Expenses
    cost_of_revenue = get_statement_value(income_statement, 'Cost Of Revenue')
    if cost_of_revenue.sum() == 0:
        cost_of_revenue = get_statement_value(income_statement, 'Operating Expense')
    selling_general_admin = get_statement_value(income_statement, 'Selling General And Administration')
    research_and_dev = get_statement_value(income_statement, 'Research And Development')
    depreciation = get_statement_value(income_statement, 'Reconciled Depreciation')
    denominator = cost_of_revenue + selling_general_admin + research_and_dev - depreciation
    denominator = denominator.replace(0, pd.NA)
    dein = (numerator / denominator) * 365
    en_name = 'Defensive Interval Ratio'
    es_name = 'Intervalo Defensivo'
    ratio_df_en, ratio_df_es = return_razon(dein, cashflow.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def gross_profit_margin_f(income_statement):
    gross_profit = get_statement_value(income_statement, 'Gross Profit')
    if gross_profit.sum() == 0:
        gross_profit = get_statement_value(income_statement, 'Operating Income')
    operating_revenue = get_statement_value(income_statement, 'Operating Revenue').replace(0, pd.NA)
    gpm = gross_profit / operating_revenue
    en_name = 'Gross Profit Margin'
    es_name = 'Margen de Utilidad Bruta'
    ratio_df_en, ratio_df_es = return_razon(gpm, income_statement.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def operating_profit_margin_f(income_statement):
    operating_income = get_statement_value(income_statement, 'Operating Income')
    operating_revenue = get_statement_value(income_statement, 'Operating Revenue').replace(0, pd.NA)
    opm = operating_income / operating_revenue
    en_name = 'Operating Profit Margin'
    es_name = 'Margen de Utilidad Operativa'
    ratio_df_en, ratio_df_es = return_razon(opm, income_statement.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def muafi_f(income_statement):
    ebit = get_statement_value(income_statement, 'EBIT')
    operating_revenue = get_statement_value(income_statement, 'Operating Revenue').replace(0, pd.NA)
    muafi = ebit / operating_revenue
    en_name = 'Profit Margin Before Financing and Taxes'
    es_name = 'Margen de Utilidad Antes de Financiamientos e Impuestos'
    ratio_df_en, ratio_df_es = return_razon(muafi, income_statement.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def muafida_f(income_statement):
    ebitda = get_statement_value(income_statement, 'EBITDA')
    operating_revenue = get_statement_value(income_statement, 'Operating Revenue').replace(0, pd.NA)
    muafida = ebitda / operating_revenue
    en_name = 'Profit Margin Before Financing, Taxes, Depreciation and Amortization'
    es_name = 'Margen de Utilidad antes Financiamientos, Impuestos, Depreciación y Amortización'
    ratio_df_en, ratio_df_es = return_razon(muafida, income_statement.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def mun_f(income_statement):
    net_income = get_statement_value(income_statement, 'Net Income From Continuing Operation Net Minority Interest')
    operating_revenue = get_statement_value(income_statement, 'Operating Revenue').replace(0, pd.NA)
    mun = net_income / operating_revenue
    en_name = 'Net Profit Margin'
    es_name = 'Margen de Utilidad Neta'
    ratio_df_en, ratio_df_es = return_razon(mun, income_statement.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def cm_f(income_statement):
    operating_revenue = get_statement_value(income_statement, 'Operating Revenue').replace(0, pd.NA)
    cost_of_revenue = get_statement_value(income_statement, 'Cost Of Revenue')
    if cost_of_revenue.sum() == 0:
        cost_of_revenue = get_statement_value(income_statement, 'Operating Expense')
    cm = (operating_revenue - cost_of_revenue) / operating_revenue
    en_name = 'Marginal Contribution Ratio'
    es_name = 'Contribución Marginal'
    ratio_df_en, ratio_df_es = return_razon(cm, income_statement.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def rda_f(balance_sheet, income_statement):
    net_income = get_statement_value(income_statement, 'Net Income From Continuing Operation Net Minority Interest')
    total_assets = get_statement_value(balance_sheet, 'Total Assets').replace(0, pd.NA)
    rda = net_income / total_assets
    en_name = 'Return on Assets'
    es_name = 'Retorno de Activos'
    ratio_df_en, ratio_df_es = return_razon(rda, income_statement.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def rdcc_f(income_statement, balance_sheet):
    net_income = get_statement_value(income_statement, 'Net Income From Continuing Operation Net Minority Interest')
    invested_capital = get_statement_value(balance_sheet, 'Invested Capital').replace(0, pd.NA)
    rdcc = net_income / invested_capital
    en_name = 'Return on Contributed Capital Ratio'
    es_name = 'Retorno de Capital Contribuido'
    columns = income_statement.columns[1:]
    ratio_df_en, ratio_df_es = return_razon(rdcc, income_statement.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es

def rdct_f(income_statement, balance_sheet):
    net_income = get_statement_value(income_statement, 'Net Income From Continuing Operation Net Minority Interest')
    total_capital = get_statement_value(balance_sheet, 'Total Capitalization').replace(0, pd.NA)
    rdct = net_income / total_capital
    en_name = 'Total Return on Capital Ratio'
    es_name = 'Retorno de Capital Total'
    ratio_df_en, ratio_df_es = return_razon(rdct, income_statement.columns[1:], en_name, es_name)
    return ratio_df_en, ratio_df_es
def generate_financial_ratios(symbol, output_path='.'):
    import pandas as pd
    import yfinance as yf
    import datetime 
    import os
    # Main code
    
    income_statement, balance_sheet, cashflow, income_statement_quarterly, \
    balance_sheet_quarterly, cashflow_quarterly = get_statements(symbol)
    
    # List of dataframes
    dataframes = [income_statement, balance_sheet, cashflow, 
                  income_statement_quarterly, balance_sheet_quarterly, 
                  cashflow_quarterly]
    
    # Clean dataframes
    for df in dataframes:
        # Convert all columns except 'index' to numeric, replace NaN with 0
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce').fillna(0)
    
    en_dataframes = []
    es_dataframes = []
    # Compute ratios
    debt_to_equity, debt_to_equity_es = debt_to_equity_f(balance_sheet)
    en_dataframes.append(debt_to_equity)
    es_dataframes.append(debt_to_equity_es)
    
    debt_to_total_assets_ratio, debt_to_total_assets_ratio_es = debt_to_total_assets_ratio_f(balance_sheet)
    en_dataframes.append(debt_to_total_assets_ratio)
    es_dataframes.append(debt_to_total_assets_ratio_es)
    
    interest_coverage_ratio, interest_coverage_ratio_es = interest_coverage_ratio_f(income_statement)
    en_dataframes.append(interest_coverage_ratio)
    es_dataframes.append(interest_coverage_ratio_es)
    
    cfcr, cfcr_es = cfcr_f(cashflow)
    en_dataframes.append(cfcr)
    es_dataframes.append(cfcr_es)
    
    dcr, dcr_es = dcr_f(cashflow, balance_sheet)
    en_dataframes.append(dcr)
    es_dataframes.append(dcr_es)
    
    quick_ratio, quick_ratio_es = quick_ratio_f(balance_sheet)
    en_dataframes.append(quick_ratio)
    es_dataframes.append(quick_ratio_es)
    
    # Acid Ratio calculation with updated handling
    acid_ratio, acid_ratio_es = acid_ratio_f(balance_sheet)
    if acid_ratio is not None:
        # Proceed with acid_ratio if it's computed
        en_dataframes.append(acid_ratio)
        es_dataframes.append(acid_ratio_es)
        pass  # Replace with your code logic as needed
    else:
        print("Acid Ratio skipped due to missing 'Inventory' in balance sheet.")
    
    ilr, ilr_es = immediate_liquidity_ratio_f(cashflow, balance_sheet)
    en_dataframes.append(ilr)
    es_dataframes.append(ilr_es)
    
    maosa, maosa_es = margin_of_safety_f(balance_sheet)
    en_dataframes.append(maosa)
    es_dataframes.append(maosa_es)
    
    dein, dein_es = defensive_interval_ratio_f(cashflow, income_statement, balance_sheet)
    en_dataframes.append(dein)
    es_dataframes.append(dein_es)
    
    gpm, gpm_es = gross_profit_margin_f(income_statement)
    en_dataframes.append(gpm)
    es_dataframes.append(gpm_es)
    
    opm, opm_es = operating_profit_margin_f(income_statement)
    en_dataframes.append(opm)
    es_dataframes.append(opm_es)
    
    muafi, muafi_es = muafi_f(income_statement)
    en_dataframes.append(muafi)
    es_dataframes.append(muafi_es)
    
    muafida, muafida_es = muafida_f(income_statement)
    en_dataframes.append(muafida)
    es_dataframes.append(muafida_es)
    
    mun, mun_es = mun_f(income_statement)
    en_dataframes.append(mun)
    es_dataframes.append(mun_es)
    
    cm, cm_es = cm_f(income_statement)
    en_dataframes.append(cm)
    es_dataframes.append(cm_es)
    
    rda, rda_es = rda_f(balance_sheet, income_statement)
    en_dataframes.append(rda)
    es_dataframes.append(rda_es)
    
    rdcc, rdcc_es = rdcc_f(income_statement, balance_sheet)
    en_dataframes.append(rdcc)
    es_dataframes.append(rdcc_es)
    
    rdct, rdct_es = rdct_f(income_statement, balance_sheet)
    en_dataframes.append(rdct)
    es_dataframes.append(rdct_es)
    
    # Concatenate the dataframes
    # Concatenar los dataframes en un solo dataframe en inglés
    en_dataframe = pd.concat(en_dataframes, axis=0).reset_index(drop=True)
    
    # Concatenar los dataframes en un solo dataframe en español
    es_dataframe = pd.concat(es_dataframes, axis=0).reset_index(drop=True)
    
    # Reverse the order of financial statements
    income_statement = income_statement.iloc[::-1].reset_index(drop=True)
    income_statement_quarterly = income_statement_quarterly.iloc[::-1].reset_index(drop=True)
    balance_sheet = balance_sheet.iloc[::-1].reset_index(drop=True)
    balance_sheet_quarterly = balance_sheet_quarterly.iloc[::-1].reset_index(drop=True)
    cashflow = cashflow.iloc[::-1].reset_index(drop=True)
    cashflow_quarterly = cashflow_quarterly.iloc[::-1].reset_index(drop=True)
    
    # Define the Excel file path
    # Definir el nombre del archivo Excel
    excel_filename = f"{symbol}_financial_ratios_{str(datetime.datetime.now())[0:10]}.xlsx"
    excel_filepath = os.path.join(output_path, excel_filename)
    os.chdir(output_path)
    
    # Save to Excel
    # Guardar en un archivo Excel con diferentes hojas
    with pd.ExcelWriter(excel_filepath, engine='xlsxwriter') as writer:
        # Guardar el dataframe en inglés en la hoja 'Ratios EN'
        en_dataframe.to_excel(writer, sheet_name='Ratios EN', index=False)
        
        # Guardar el dataframe en español en la hoja 'Ratios ES'
        es_dataframe.to_excel(writer, sheet_name='Ratios ES', index=False)
        income_statement.to_excel(writer, sheet_name = 'Income Statement', index=False)
        income_statement_quarterly.to_excel(writer, sheet_name = 'Income statement QT', index=False)
        balance_sheet.to_excel(writer, sheet_name = 'Balance sheet', index=False)
        balance_sheet_quarterly.to_excel(writer, sheet_name = 'Balance sheet QT', index=False)
        cashflow.to_excel(writer, sheet_name = 'Cashflow', index=False)
        cashflow_quarterly.to_excel(writer, sheet_name = 'Cashflow QT', index=False)
        pass
    
    print(f"Financial ratios saved to {excel_filepath}")



