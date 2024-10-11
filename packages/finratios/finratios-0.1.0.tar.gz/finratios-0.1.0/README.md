# finratios

`finratios` is a Python package that calculates various financial ratios for a 
given company symbol using data from Yahoo Finance and exports the results to an Excel file.

In Mexico, we have the Financial Reporting Standards Council (CINIF). In NIF A-3, 
we have a list of financial ratios. 
It is freely available under the name "finratios," you can download including
income statement, balance sheet, and cash flow of publicly traded companies in the U.S., 
and it automatically calculates the most important financial ratios.

You can use it to research purposes, or investment analysis

Ratios of NIF A-3 in spanish

Deuda a capital contable \
Deuda a activos totales \
Cobertura de Interés \
Cobertura de Flujo \
Cobertura de Deuda \
Prueba de Liquidez \
Prueba de Acido \
Liquidez Inmediata \
Margen de Seguridad \
Intervalo Defensivo \
Margen de Utilidad Bruta \
Margen de Utilidad Operativa \
Margen de Utilidad Antes de Financiamientos e Impuestos \
Margen de Utilidad antes Financiamientos, Impuestos, Depreciación y Amortización \
Margen de Utilidad Neta \
Contribución Marginal \
Retorno de Activos \
Retorno de Capital Contribuido \
Retorno de Capital Total\
##########

Here you can check all symbols : https://stockanalysis.com/stocks/

Google colab example: https://colab.research.google.com/drive/1_oNjt7u_8sbbLpWJmuW5htvQ37_2eWyz?usp=sharing

Youtube Video spanish:

Youtube Video english:

## Author

jcepedaobregon@gmail.com

https://josuecepeda.weebly.com/

## Installation

Install the package via pip:

```bash
pip install git+https://github.com/josuecepeda94/finratios
```

## Example of usage
```bash
from finratios import generate_financial_ratios
```
Generate financial ratios for NVIDIA and save the Excel file in the current directory
```bash
generate_financial_ratios('NVDA', output_path='.')
```
## Parameters
symbol (str): The stock ticker symbol of the company (e.g., 'AAPL' for Apple Inc.). \
output_path (str, optional): The directory where the Excel file will be saved. Defaults to the current directory.
