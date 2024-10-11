# Num2GeoText

A Python package for converting numbers and floats (up to 15 digits) into Georgian text, and for converting floats (up to 15 digits) into Georgian currency text representations. It supports a wide range of use cases, 
including converting numerical values for text-based reports, financial applications, 
educational tools, voice assistants, legal documents, data validation and more. 
This package can be utilized in generating invoices, converting currency amounts for receipts, 
enhancing accessibility through text-to-speech systems, and providing better readability for 
large numeric data.

## Overview

The package performs the following tasks:

### 1. Convert Numbers to Text
- Converts integers into readable Georgian text representations.

### 2. Convert Floats to Text
- Converts floats into Georgian text representations.

### 3. Convert Floats to Currency Text
- Converts floats into Georgian currency text representations.

### 4. Supports Multiple Use Cases
- Useful for financial applications, educational tools, and more.

## Requirements

Ensure you have the following Python packages installed:

- **setuptools**

You can install this package using pip if it is not already installed:

```bash
pip install setuptools
```

## Usage

Here is an example of how to use this package:

```python
from num2geotext import int_num_to_geo_text, float_num_to_geo_text, float_num_to_geo_currency

# Convert a number to Georgian text
int_text_representation = int_num_to_geo_text(30245)

# Convert a float to Georgian text
float_text_representation = float_num_to_geo_text(256.35)

# Convert a float to Georgian currency text
float_currency_text_representation = float_num_to_geo_currency(3578945.15)

print(int_text_representation)  # Output: "ოცდაათი ათას ორას ორმოცდახუთი"
print(float_text_representation)  # Output: "ორას ორმოცდათექვსმეტი მთელი, ოცდათხუთმეტი მეასედი"
print(float_currency_text_representation)  # Output: "სამი მილიონ ხუთას სამოცდათვრამეტი ათას ცხრაას ორმოცდახუთი ლარი და თხუთმეტი თეთრი"
```

## Function Descriptions
- int_num_to_geo_text(number: int) -> str:
  - Converts an integer into its corresponding Georgian text representation.
- float_num_to_geo_text(number: float) -> str:
  - Converts a float into its corresponding Georgian text representation (limited to two decimal places)
- float_num_to_geo_currency(number: float) -> str:
  - Converts a float into its corresponding Georgian currency text representation.

## Summary
This package provides simple yet effective functions to convert numerical values into their Georgian text equivalents, making it useful for various applications such as financial reporting and educational tools.

