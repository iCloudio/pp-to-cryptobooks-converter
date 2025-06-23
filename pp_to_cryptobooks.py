#!/usr/bin/env python3
"""
Portfolio Performance to CryptoBooks Converter
==============================================

Converts cryptocurrency transaction CSV exports from Portfolio Performance
to CryptoBooks-compatible format for Italian tax declaration (730).

Author: [Your Name]
License: MIT
Version: 1.0.0
"""

import csv
import sys
import os
from datetime import datetime
from typing import Dict, Optional, Union

__version__ = "1.0.0"

# Comprehensive cryptocurrency symbol mapping
CRYPTO_SYMBOLS = {
    # Major cryptocurrencies
    'Bitcoin': 'BTC',
    'Ethereum': 'ETH',
    'Cardano': 'ADA',
    'Solana': 'SOL',
    'Dogecoin': 'DOGE',
    'Litecoin': 'LTC',
    'Polkadot': 'DOT',
    'Chainlink': 'LINK',
    'Polygon': 'MATIC',
    
    # Exchange tokens
    'Cronos': 'CRO',
    'Binance Coin': 'BNB',
    
    # DeFi tokens
    'Cosmos': 'ATOM',
    'Injective': 'INJ',
    'NEAR': 'NEAR',
    'Ondo': 'ONDO',
    'Nexera': 'NXRA',
    'Clearpool': 'CPOOL',
    'Bittensor': 'TAO',
    'Manta Network': 'MANTA',
    'Dymension': 'DYM',
    
    # Fan tokens
    'AC Milan Fan Token': 'ACM',
    'Juventus Fan Token': 'JUV',
    'Paris Saint-Germain Fan Token': 'PSG',
    
    # Add lowercase variants for case-insensitive matching
    **{k.lower(): v for k, v in {
        'Bitcoin': 'BTC', 'Ethereum': 'ETH', 'Cardano': 'ADA',
        'Solana': 'SOL', 'Dogecoin': 'DOGE', 'Litecoin': 'LTC',
        'Polkadot': 'DOT', 'Chainlink': 'LINK', 'Polygon': 'MATIC',
        'Cronos': 'CRO', 'Binance Coin': 'BNB', 'Cosmos': 'ATOM',
        'Injective': 'INJ', 'NEAR': 'NEAR', 'Ondo': 'ONDO',
        'Nexera': 'NXRA', 'Clearpool': 'CPOOL', 'Bittensor': 'TAO',
        'Manta Network': 'MANTA', 'Dymension': 'DYM',
        'AC Milan Fan Token': 'ACM', 'Juventus Fan Token': 'JUV',
        'Paris Saint-Germain Fan Token': 'PSG'
    }.items()}
}

# Expected input columns from Portfolio Performance
PP_COLUMNS = [
    'Data', 'Tipo', 'Titolo', 'Azioni', 'Quotazione', 'Importo',
    'Commissioni', 'Tasse', 'Valore operazione netto', 'Conto di cassa',
    'Conto di compensazione', 'Note', 'Origine'
]

# Output columns for CryptoBooks
CB_COLUMNS = [
    'TYPE', 'CATEGORY', 'TRANSACTION DATE', 'FROM CURRENCY', 'FROM AMOUNT',
    'TO CURRENCY', 'TO AMOUNT', 'FEE CURRENCY', 'FEE AMOUNT', 'NOTES', 'ORIGINAL ID'
]


class TransactionConverter:
    """Handles conversion of Portfolio Performance transactions to CryptoBooks format."""
    
    def __init__(self):
        self.converted_count = 0
        self.skipped_count = 0
        
    def parse_european_decimal(self, value_str: str) -> float:
        """
        Convert European decimal format to float.
        
        Args:
            value_str: String with European format (e.g., "1.234,56")
            
        Returns:
            Float value or 0.0 if conversion fails
        """
        if not value_str or value_str.strip() == '':
            return 0.0
        try:
            # Remove thousands separator (.) and replace decimal comma with dot
            clean_value = value_str.replace('.', '').replace(',', '.')
            return float(clean_value)
        except (ValueError, AttributeError):
            return 0.0
    
    def extract_crypto_symbol(self, title: str) -> str:
        """
        Extract cryptocurrency symbol from transaction title.
        
        Args:
            title: Transaction title from Portfolio Performance
            
        Returns:
            Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        """
        title_lower = title.lower()
        
        # Check against known cryptocurrencies (case-insensitive)
        for crypto_name, symbol in CRYPTO_SYMBOLS.items():
            if crypto_name.lower() in title_lower:
                return symbol
        
        # Fallback: extract uppercase tokens (3-4 chars)
        words = title.replace('EUR', '').split()
        for word in words:
            word = word.strip()
            if len(word) >= 3 and word.isupper():
                return word[:4]
        
        # Last resort: use first word
        first_word = title.split()[0] if title.split() else 'UNKNOWN'
        return first_word.upper()[:4]
    
    def format_decimal_for_excel(self, value: Union[int, float, str]) -> str:
        """
        Format decimal values for Italian Excel compatibility.
        
        Args:
            value: Numeric value to format
            
        Returns:
            String with comma as decimal separator
        """
        if isinstance(value, (int, float)):
            if value == 0:
                return ''
            return str(value).replace('.', ',')
        return str(value)
    
    def convert_transaction(self, row: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
        Convert a single Portfolio Performance transaction row to CryptoBooks format.
        
        Args:
            row: Dictionary representing a CSV row from Portfolio Performance
            
        Returns:
            Converted transaction dictionary or None if conversion fails
        """
        try:
            # Extract and clean data
            date = row['Data'].strip()
            transaction_type = row['Tipo'].strip()
            title = row['Titolo'].strip()
            shares = self.parse_european_decimal(row['Azioni'])
            price = self.parse_european_decimal(row['Quotazione'])
            amount = self.parse_european_decimal(row['Importo'])
            fees = self.parse_european_decimal(row['Commissioni'])
            notes = row['Note'].strip()
            origin = row['Origine'].strip()
            
            # Extract cryptocurrency symbol
            crypto_symbol = self.extract_crypto_symbol(title)
            
            # Determine transaction direction and currencies
            if transaction_type.lower() == 'compra':
                # BUY: EUR -> CRYPTO
                from_currency = 'EUR'
                to_currency = crypto_symbol
                from_amount = amount  # EUR spent
                to_amount = shares    # Crypto received
            elif transaction_type.lower() == 'vendi':
                # SELL: CRYPTO -> EUR
                from_currency = crypto_symbol
                to_currency = 'EUR'
                from_amount = shares  # Crypto sold
                to_amount = amount    # EUR received
            else:
                # Unknown type - use default
                from_currency = 'EUR'
                to_currency = crypto_symbol
                from_amount = amount
                to_amount = shares
            
            # Combine notes and origin
            combined_notes = f"{notes} {origin}".strip()
            if not combined_notes:
                combined_notes = f"{transaction_type} {title} on {origin}".strip()
            
            # Create CryptoBooks format
            converted_row = {
                'TYPE': 'Trade',
                'CATEGORY': 'Trading',
                'TRANSACTION DATE': date,
                'FROM CURRENCY': from_currency,
                'FROM AMOUNT': self.format_decimal_for_excel(from_amount),
                'TO CURRENCY': to_currency,
                'TO AMOUNT': self.format_decimal_for_excel(to_amount),
                'FEE CURRENCY': from_currency if fees > 0 else '',
                'FEE AMOUNT': self.format_decimal_for_excel(fees) if fees > 0 else '',
                'NOTES': combined_notes,
                'ORIGINAL ID': ''
            }
            
            self.converted_count += 1
            return converted_row
            
        except Exception as e:
            print(f"❌ Error converting row: {e}")
            print(f"   Problematic row: {row}")
            self.skipped_count += 1
            return None
    
    def validate_input_file(self, file_path: str) -> bool:
        """
        Validate that the input file exists and has expected format.
        
        Args:
            file_path: Path to the input CSV file
            
        Returns:
            True if file is valid, False otherwise
        """
        if not os.path.exists(file_path):
            print(f"❌ Error: File {file_path} does not exist!")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                
            # Check if it looks like Portfolio Performance format
            if 'Data' in first_line and 'Tipo' in first_line and 'Titolo' in first_line:
                return True
            else:
                print("⚠️  Warning: File doesn't appear to be in Portfolio Performance format")
                print(f"   Expected columns containing: Data, Tipo, Titolo")
                print(f"   Found: {first_line}")
                return False
                
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False
    
    def convert_csv(self, input_file: str, output_file: str) -> bool:
        """
        Convert Portfolio Performance CSV to CryptoBooks format.
        
        Args:
            input_file: Path to Portfolio Performance CSV file
            output_file: Path for CryptoBooks output file
            
        Returns:
            True if conversion successful, False otherwise
        """
        if not self.validate_input_file(input_file):
            return False
        
        try:
            with open(input_file, 'r', encoding='utf-8') as infile:
                # Portfolio Performance uses semicolon delimiter
                reader = csv.DictReader(infile, delimiter=';')
                
                print(f"📊 Columns found: {list(reader.fieldnames)}")
                
                converted_rows = []
                
                for row_num, row in enumerate(reader, 1):
                    converted_row = self.convert_transaction(row)
                    if converted_row:
                        converted_rows.append(converted_row)
                        print(f"✅ Row {row_num}: {row['Tipo']} {row['Titolo']} -> "
                              f"{converted_row['FROM CURRENCY']} → {converted_row['TO CURRENCY']}")
                
                # Write output file with semicolon delimiter for Italian Excel
                with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.DictWriter(outfile, fieldnames=CB_COLUMNS, delimiter=';')
                    writer.writeheader()
                    writer.writerows(converted_rows)
                
                self._print_summary(output_file, converted_rows)
                return True
                
        except Exception as e:
            print(f"❌ Error during conversion: {e}")
            return False
    
    def _print_summary(self, output_file: str, converted_rows: list):
        """Print conversion summary."""
        print(f"\n🎉 Conversion completed!")
        print(f"📈 Rows processed: {self.converted_count}")
        print(f"⚠️  Rows skipped: {self.skipped_count}")
        print(f"💾 Output saved to: {output_file}")
        
        if converted_rows:
            print(f"\n📋 Preview of first converted transaction:")
            first_row = converted_rows[0]
            for key, value in first_row.items():
                print(f"   {key}: {value}")


def print_banner():
    """Print application banner."""
    print("=" * 70)
    print("🔄 Portfolio Performance to CryptoBooks Converter")
    print(f"   Version {__version__}")
    print("   Convert crypto transactions for Italian tax declaration (730)")
    print("=" * 70)


def print_usage():
    """Print usage instructions."""
    print("📖 Usage:")
    print("   python pp_to_cryptobooks.py <input_file.csv> <output_file.csv>")
    print("\n💡 Example:")
    print("   python pp_to_cryptobooks.py portfolio_transactions.csv cryptobooks_import.csv")
    print("\n📋 Input format: Portfolio Performance CSV export")
    print("📋 Output format: CryptoBooks import format")


def main():
    """Main application entry point."""
    print_banner()
    
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)
    
    input_file, output_file = sys.argv[1], sys.argv[2]
    
    print(f"📁 Input:  {input_file}")
    print(f"📁 Output: {output_file}")
    print("-" * 70)
    
    converter = TransactionConverter()
    success = converter.convert_csv(input_file, output_file)
    
    if success:
        print("\n✅ Conversion completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Open the output file to verify the conversion")
        print("   2. Import the file into CryptoBooks")
        print("   3. Use CryptoBooks to generate your tax report")
    else:
        print("\n❌ Conversion failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
