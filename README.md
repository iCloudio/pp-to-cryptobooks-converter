# Portfolio Performance to CryptoBooks Converter

🔄 **Convert cryptocurrency transactions from Portfolio Performance to CryptoBooks format for Italian tax declaration (730)**

## Overview

This tool simplifies the process of declaring cryptocurrency gains/losses in your Italian tax return by converting transaction data between two popular applications:

- **[Portfolio Performance](https://www.portfolio-performance.info/en/)** - Open source investment portfolio tracking software
- **[CryptoBooks](https://cryptobooks.tax/it)** - Italian cryptocurrency tax calculation platform

## Why This Tool?

Managing cryptocurrency taxes in Italy can be complex. This converter bridges the gap between:

1. **Portfolio Performance** - Where you track your crypto investments
2. **CryptoBooks** - Where you calculate taxes for your 730 declaration

Instead of manually re-entering hundreds of transactions, simply export from Portfolio Performance and import into CryptoBooks!

## Features

✅ **Complete Transaction Conversion**
- Handles buy/sell transactions correctly
- Preserves all transaction details (dates, amounts, fees)
- Maps cryptocurrency names to standard symbols

✅ **Italian Excel Compatibility**
- Uses semicolon delimiters
- European decimal format (comma-separated)
- Ready to open in Italian Excel

✅ **Comprehensive Crypto Support**
- Major cryptocurrencies (BTC, ETH, ADA, SOL, etc.)
- DeFi tokens (ATOM, INJ, NEAR, TAO, etc.)
- Fan tokens (ACM, JUV, PSG)
- Easy to extend with new tokens

✅ **Professional Grade**
- Error handling and validation
- Detailed conversion reports
- Type hints and documentation

## Installation

### Prerequisites
- Python 3.7 or higher
- No additional dependencies required (uses only standard library)

### Download
```bash
git clone https://github.com/yourusername/pp-to-cryptobooks-converter.git
cd pp-to-cryptobooks-converter
```

## Usage

### Step 1: Export from Portfolio Performance
1. Open Portfolio Performance
2. Go to your cryptocurrency transactions
3. Export as CSV with these columns:
   - Data, Tipo, Titolo, Azioni, Quotazione, Importo, Commissioni, Tasse, Valore operazione netto, Conto di cassa, Conto di compensazione, Note, Origine

### Step 2: Convert
```bash
python pp_to_cryptobooks.py input_transactions.csv output_for_cryptobooks.csv
```

### Step 3: Import to CryptoBooks
1. Open [CryptoBooks](https://cryptobooks.tax/it)
2. Import the converted CSV file
3. Generate your tax report for 730 declaration

## Input/Output Format

### Input (Portfolio Performance)
```csv
Data;Tipo;Titolo;Azioni;Quotazione;Importo;Commissioni;Tasse;Valore operazione netto;Conto di cassa;Conto di compensazione;Note;Origine
20/02/2025 20:37;Compra;Bitcoin EUR;0,01064;93.774,44;997,76;;;997,76;Binance;EUR Binance;con le commissioni erano 1000 eur;
20/02/2025 19:28;Vendi;Ethereum EUR;0,5;2.400,00;1.200,00;;;1.200,00;Coinbase;EUR Coinbase;;
```

### Output (CryptoBooks)
```csv
TYPE;CATEGORY;TRANSACTION DATE;FROM CURRENCY;FROM AMOUNT;TO CURRENCY;TO AMOUNT;FEE CURRENCY;FEE AMOUNT;NOTES;ORIGINAL ID
Trade;Trading;20/02/2025 20:37;EUR;997,76;BTC;0,01064;;;con le commissioni erano 1000 eur;
Trade;Trading;20/02/2025 19:28;ETH;0,5;EUR;1200;;;EUR Coinbase;
```

## Supported Cryptocurrencies

The converter recognizes 25+ cryptocurrencies including:

| Cryptocurrency | Symbol | Cryptocurrency | Symbol |
|---------------|--------|---------------|--------|
| Bitcoin | BTC | Cosmos | ATOM |
| Ethereum | ETH | Injective | INJ |
| Cardano | ADA | NEAR Protocol | NEAR |
| Solana | SOL | Ondo | ONDO |
| Cronos | CRO | Bittensor | TAO |
| Polygon | MATIC | Manta Network | MANTA |

*...and many more!*

### Adding New Cryptocurrencies

To add support for new tokens, edit the `CRYPTO_SYMBOLS` dictionary in the code:

```python
CRYPTO_SYMBOLS = {
    'Your Token Name': 'SYMBOL',
    # ... existing mappings
}
```

## Example

```bash
$ python pp_to_cryptobooks.py my_transactions.csv cryptobooks_import.csv

====================================================================
🔄 Portfolio Performance to CryptoBooks Converter
   Version 1.0.0
   Convert crypto transactions for Italian tax declaration (730)
====================================================================
📁 Input:  my_transactions.csv
📁 Output: cryptobooks_import.csv
----------------------------------------------------------------------
📊 Columns found: ['Data', 'Tipo', 'Titolo', 'Azioni', 'Quotazione', 'Importo', 'Commissioni', 'Tasse', 'Valore operazione netto', 'Conto di cassa', 'Conto di compensazione', 'Note', 'Origine']
✅ Row 1: Compra Bitcoin EUR -> EUR → BTC
✅ Row 2: Vendi Ethereum EUR -> ETH → EUR

🎉 Conversion completed!
📈 Rows processed: 2
⚠️  Rows skipped: 0
💾 Output saved to: cryptobooks_import.csv

✅ Conversion completed successfully!

📋 Next steps:
   1. Open the output file to verify the conversion
   2. Import the file into CryptoBooks
   3. Use CryptoBooks to generate your tax report
```

## Contributing

Contributions are welcome! Please feel free to:

1. Report bugs
2. Suggest new features
3. Add support for new cryptocurrencies
4. Improve documentation

### Development Setup

```bash
git clone https://github.com/yourusername/pp-to-cryptobooks-converter.git
cd pp-to-cryptobooks-converter

# Run tests
python -m pytest tests/

# Check code style
python -m flake8 pp_to_cryptobooks.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

⚠️ **Important**: This tool is provided for convenience only. Always verify the converted data before submitting your tax declaration. The authors are not responsible for any tax-related issues arising from the use of this software.

## Links

- [Portfolio Performance](https://www.portfolio-performance.info/en/) - Open source portfolio tracking
- [CryptoBooks](https://cryptobooks.tax/it) - Italian crypto tax platform
- [Italian Tax Authority (Agenzia delle Entrate)](https://www.agenziaentrate.gov.it/)

## Support

If you find this tool helpful, please ⭐ star the repository!

For questions or issues, please open a GitHub issue.
