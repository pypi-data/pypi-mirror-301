
<h1 align="center">Country Converter Toolkit</h1>

## Feature

- **Country Code**
  - find out the country code from the country name
- **Country Info**
  - find out country information about capital city and currency from country name
- **Country Languange**
  - find out the language of a country based on the country name
- **Continent of countries**
  - find out continent from country name or country code
- **Currency Conversion**
  - convert money from one country to another
- **Time Zone**
  - convert time from one country to another
 
## Installation

To install the Country Converter Toolkit package, use pip:

```bash
pip install Country-Converter-Toolkit
```

## how to use

Here are some examples of how to use the Country-Converter-Toolkit package:

### Country Code

```python
from Country.CountryCode import search_country_code
print(search_country_code("Indonesia"))
```

### Country Info

```python
from Country.CountryInfo import get_country_info
print(get_country_info("indonesia"))
```

### Country Languange

```python
from Country.CountryLanguange import get_country_language
print(get_country_language("Indonesia"))
```

### Continent of countries

```python
from Country.ContinentOfCountries import get_info_by_country_code
print(get_info_by_country_code("ID"))
```

### Currency Conversion

```python
from Country.MoneyConversion import currency_conversion
print(currency_conversion(10, 'USD', 'IDR'))
```

### Time Zone

```python
from Country.TimeZone import convert_time_by_code
print(convert_time_by_code("WITA", "JST", "2024-10-09 14:30:00"))
```

```python
from Country.TimeZone import convert_city_time
print(convert_city_time("Makassar", "New York", "2024-10-09 00:30:00"))
```

## About The Module
This package consists of the following modules:

### `Module_1`
#### `search_country_code(country_name) : str`
This function contains the country name and country code

**usage example:**
```python
from Country.CountryCode import search_country_code
print(search_country_code('Indonesia'))
```

**output:**
```
ID
```
### Module_1 Notes:
  
- If the country name entered does not exist or the user enters something other than the country name, "country not found" will appear.

### `Modul_2`

This function is used to get a country's info based on the country name entered

**Usage Example:**
```python
from Country.CountryInfo import get_country_info
print(get_country_info("Indonesia"))
```

**Output:**
```
Capital City : Jakarta, Currency : RUPIAH (IDR)
```

**Module 3 Notes:**
- Ensure you input the correct country name to obtain accurate result
- Make sure to use the correct capitalization for the country


### `Modul_3`

This function is used to get a country's language  based on the country name entered

#### `search_country_language(country_name) : str`

**Usage Example:**
```python
from Country.CountryLanguange import get_country_language
print(get_country_language("Indonesia"))
```

**Output:**
```
Indonesian
```

**Module 3 Notes:**
- Ensure you input the correct country name to obtain accurate result
- Make sure to use the correct capitalization for the codes
- If the country listed are not a part of the list, the function will return a "Code not Found" message

### `module_4`

#### data_country
This function is designed for programmers who want to categorize countries by continent.

#### get_info_by_country_code(country_code)
This function uses the get() method to retrieve information about a country based on the provided country code.

*Parameter:*
- country_code: The expected input is a country code (example: "AF").

*Example Usage:*
```python
from Country.ContinentOfCountries import get_info_by_country_code
print(get_info_by_country_code('JP'))
```

**Output:**
Japan, Asia

#### `get_info_by_country_code(country_code)`
This function uses the `get()` method to retrieve information about a country based on the provided country name.

**Parameter:**
- `country_name`: The expected input is a country name (example: "Afghanistan").

**Example Usage:**
```python
from Country.ContinentOfCountries import get_info_by_country_code
print(get_info_by_country_code('ID'))
``` 

*Output:*
Indonesia, Asia

### Module 4 notes
- An example of its use is that the programmer will import this library, then if the programmer calls the function by entering the country code and it will be converted to the continent of that country.
- To search for country information based on the given country_code. This function will return the names of countries and continents as tuples. Otherwise, it will return a message that the country code is not found.
- For the country name function, this function iterates through all the values ​​in data_country. For each value, it checks whether the country name (in lowercase) matches the given country_name (also in lowercase).
If found, this function will return the country and continent names as tuples. If not found, it will return a message that the country name was not found.

### `module_5`


#### `currency_conversion(amount, from_currency, to_currency)`
This function is used to convert a number of currencies from one country to another.

**Parameter:**
- `amount`: The amount of money you want to convert.
- `from_currency`: The origin of the currency you want to convert.
- `to_currency`: Destination currency to be converted.

**Example Usage:**
```python
from Country.MoneyConversion import currency_conversion
print(currency_conversion(10, 'USD', 'IDR'))
```

**Output:**
```
142.450.00
```
If the currency is not recognized, the output is:
'''
Currency not recognized
'''

### Catatan modul 1
- Make sure to use capital letters for the country's currency

### `module_6`

#### `convert_time_by_code(from_tz: str, to_tz: str, time_str: str)`

This function is used to convert time from one time zone code to another.

**Parameters:**
- `from_tz`: The time zone code to convert from.
- `to_tz`: The time zone code to convert to.
- `time_str`: The time to be converted (format: YYYY-MM-DD HH:MM:SS).

**Example Usage:**
```python
from Country.TimeZone import convert_time_by_code
print(convert_time_by_code("WITA", "JST", "2024-10-09 14:30:00"))
```

**Output:**
```
2024-10-09 15:30:00
```


#### `convert_city_time(city_from: str, city_to: str, time_str: str)`
This function is used to convert time from one city to another city with a different time zone.

**Example Usage:**
```python
from Country.TimeZone import convert_city_time
print(convert_city_time("Makassar", "New York", "2024-10-09 00:30:00"))
```

**Output:**
```
2024-10-08 12:30:00
```

### Module 6 Notes
- Ensure you input the correct time zone and city to obtain accurate conversion results.
- When using the `convert_time_by_code()` function, make sure to use the correct capitalization for time zone codes.
- For `convert_time_by_code()`, if there are time zones with the same name, use the format `CODE_country`, `for example, convert_time_by_code("WITA", "AST_Atlantic", "2024-10-09 12:00:00")`.
- Not all cities can be converted; make sure to input major cities or capitals. If unavailable, use the `convert_time_by_code()` function instead.
- If the time zone or city is not found, the function will return an error message.

## contact
For further questions, please contact
  - aal3it@gmail.com
  - arielmufaddhal1@gmail.com
  - diditikbalalfarauzy3943@gmail.com
  - andisophieamri@gmail.com
  - anisaandi1980@gmail.com
  - azzahrasyam49@gmail.com
