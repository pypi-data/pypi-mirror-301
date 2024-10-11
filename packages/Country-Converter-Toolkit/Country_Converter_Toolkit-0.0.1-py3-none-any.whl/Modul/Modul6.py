from datetime import datetime, timedelta

TIME_ZONES = {
    "WIB": 7,               # Western Indonesia Time
    "WITA": 8,              # Central Indonesia Time
    "WIT": 9,               # Eastern Indonesia Time
    "JST": 9,               # Japan Standard Time
    "KST": 9,               # Korea Standard Time
    "CST_China": 8,         # China Standard Time
    "EST_US": -5,           # Eastern Standard Time (US)
    "PST_US": -8,           # Pacific Standard Time (US)
    "CST_US": -6,           # Central Standard Time (US)
    "UTC": 0,               # Coordinated Universal Time
    "CET": 1,               # Central European Time
    "MSK": 3,               # Moscow Standard Time
    "GST_UAE": 4,           # Gulf Standard Time (UAE)
    "AEDT": 11,             # Australian Eastern Daylight Time
    "EET": 2,               # Eastern European Time
    "EAT": 3,               # East Africa Time
    "SAST": 2,              # South Africa Standard Time
    "ART": -3,              # Argentina Time
    "HKT": 8,               # Hong Kong Time
    "MYT": 8,               # Malaysia Time
    "IRST": 3.5,            # Iran Standard Time
    "AST_Saudi": 3,         # Arabia Standard Time (Saudi Arabia)
    "IST_Israel": 2,        # Israel Standard Time
    "WAT": 1,               # West Africa Time
    "WET": 0,               # Western European Time
    "NZDT": 13,             # New Zealand Daylight Time
    "PGT": 10,              # Papua New Guinea Time
    "FJT": 12,              # Fiji Time
    "PHT": 8,               # Philippine Time
    "PKT": 5,               # Pakistan Standard Time
    "IST_India": 5.5,       # Indian Standard Time
    "AFT": 4.5,             # Afghanistan Time
    "BST": 6,               # Bangladesh Standard Time
    "MMT": 6.5,             # Myanmar Time
    "MVT": 5,               # Maldives Time
    "AEST": 10,             # Australian Eastern Standard Time
    "ACST": 9.5,            # Australian Central Standard Time
    "AWST": 8,              # Australian Western Standard Time
    "HST": -10,             # Hawaii-Aleutian Standard Time
    "AKST": -9,             # Alaska Standard Time
    "GMT": 0,               # Greenwich Mean Time
    "ULAT": 8,              # Ulaanbaatar Time
    "ICT": 7,               # Indochina Time
    "BTT": 6,               # Bhutan Time
    "AST_Atlantic": -4,     # Atlantic Standard Time
    "PYT": -4,              # Paraguay Time
    "UYT": -3,              # Uruguay Time
    "BOT": -4,              # Bolivia Time
    "ECT": -5,              # Ecuador Time
    "VET": -4,              # Venezuela Time
    "TLT": 9,               # Timor-Leste Time
    "PET": -5,              # Peru Time
    "GYT": -4,              # Guyana Time
    "SRT": -3,              # Suriname Time
    "CAT": 2,               # Central Africa Time
    "GET": 4,               # Georgia Standard Time
    "AMT_Armenia": 4,       # Armenia Time
    "AZT": 4,               # Azerbaijan Time
    "ALMT": 6,              # Alma-Ata Time
    "KGT": 6,               # Kyrgyzstan Time
    "PETT": 12,             # Kamchatka Time
    "VLAT": 10,             # Vladivostok Time
    "YEKT": 5,              # Yekaterinburg Time
    "NOVT": 7,              # Novosibirsk Time
    "KRAT": 7,              # Krasnoyarsk Time
    "IRKT": 8,              # Irkutsk Time
    "KAL": 2,               # Kaliningrad Time
    "ChST": 10,             # Chamorro Standard Time
    "NST": -3.5,            # Newfoundland Standard Time
    "MHT": 12,              # Marshall Islands Time
    "PONT": 11,             # Pohnpei Standard Time
    "VUT": 11,              # Vanuatu Time
    "TOT": 13,              # Tonga Time
    "GILT": 12,             # Gilbert Island Time
    "BRT": -3,              # Brasilia Time
    "SGT": 8,               # Singapore Time
}

CITY_TIME_ZONES = {
    "Jakarta": "WIB", "Surabaya": "WIB", "Bandung": "WIB",         # Indonesia (Western Indonesia Time)
    "Bali": "WITA", "Makassar": "WITA", "Manado": "WITA",          # Indonesia (Central Indonesia Time)
    "Jayapura": "WIT",                                             # Indonesia (Eastern Indonesia Time)
    "Tokyo": "JST", "Osaka": "JST", "Nagoya": "JST",               # Japan
    "Seoul": "KST", "Busan": "KST",                                # South Korea
    "Shanghai": "CST_China", "Beijing": "CST_China",               # China (China Standard Time)
    "New York": "EST_US", "Los Angeles": "PST_US", 
    "Chicago": "CST_US", "Houston": "CST_US",                      # US
    "London": "UTC", "Manchester": "UTC",                          # UK (Coordinated Universal Time)
    "Berlin": "CET", "Munich": "CET", "Frankfurt": "CET",          # Germany (Central European Time)
    "Moscow": "MSK", "Saint Petersburg": "MSK",                    # Russia (Moscow Standard Time)
    "Dubai": "GST_UAE",                                            # UAE (Gulf Standard Time)
    "Sydney": "AEDT", "Melbourne": "AEDT",                         # Australia (Australian Eastern Daylight Time)
    "Cairo": "EET", "Alexandria": "EET",                           # Egypt (Eastern European Time)
    "Nairobi": "EAT", "Mombasa": "EAT",                            # Kenya (East Africa Time)
    "Cape Town": "SAST", "Johannesburg": "SAST",                   # South Africa (South Africa Standard Time)
    "Buenos Aires": "ART",                                         # Argentina (Argentina Time)
    "Paris": "CET", "Nice": "CET",                                 # France
    "Madrid": "CET", "Barcelona": "CET",                           # Spain
    "Toronto": "EST_US", "Vancouver": "PST_US",                    # Canada
    "Mexico City": "CST_US", "Guadalajara": "CST_US",              # Mexico
    "Rio de Janeiro": "BRT", "São Paulo": "BRT",                   # Brazil (Brasilia Time)
    "Bangkok": "ICT",                                              # Thailand (Indochina Time)
    "Hanoi": "ICT",                                                # Vietnam
    "Singapore": "SGT",                                            # Singapore (Singapore Time)
    "Hong Kong": "HKT",                                            # Hong Kong
    "Kuala Lumpur": "MYT",                                         # Malaysia
    "Tehran": "IRST",                                              # Iran (Iran Standard Time)
    "Riyadh": "AST_Saudi",                                         # Saudi Arabia (Arabia Standard Time)
    "Jerusalem": "IST_Israel",                                     # Israel (Israel Standard Time)
    "Lagos": "WAT",                                                # Nigeria (West Africa Time)
    "Casablanca": "WET",                                           # Morocco (Western European Time)
    "Algiers": "CET",                                              # Algeria
    "Auckland": "NZDT",                                            # New Zealand (New Zealand Daylight Time)
    "Port Moresby": "PGT",                                         # Papua New Guinea
    "Suva": "FJT",                                                 # Fiji
    "Manila": "PHT",                                               # Philippines (Philippine Time)
    "Karachi": "PKT",                                              # Pakistan
    "Colombo": "IST_India",                                        # Sri Lanka (Indian Standard Time)
    "Rome": "CET",                                                 # Italy
    "Athens": "EET",                                               # Greece
    "Lisbon": "WET",                                               # Portugal
    "Miami": "EST_US",                                             # US
    "Denver": "MST",                                               # US
    "Lima": "PET",                                                 # Peru (Peru Time)
    "Tashkent": "ALMT",                                            # Uzbekistan
    "Astana": "ALMT",                                              # Kazakhstan
    "Bishkek": "KGT",                                              # Kyrgyzstan
    "Kuwait City": "AST_Saudi",                                    # Kuwait
    "Doha": "AST_Saudi",                                           # Qatar
    "Muscat": "GST_UAE",                                           # Oman
    "Kabul": "AFT",                                                # Afghanistan (Afghanistan Time)
    "Islamabad": "PKT",                                             # Pakistan
    "Kathmandu": "NPT",                                            # Nepal (Nepal Time)
    "Dhaka": "BST",                                                # Bangladesh (Bangladesh Standard Time)
    "Yangon": "MMT",                                               # Myanmar (Myanmar Time)
    "Male": "MVT",                                                 # Maldives
    "Brisbane": "AEST",                                            # Australia (Australian Eastern Standard Time)
    "Adelaide": "ACST",                                            # Australia (Australian Central Standard Time)
    "Perth": "AWST",                                               # Australia (Australian Western Standard Time)
    "Honolulu": "HST",                                             # Hawaii (US)
    "Anchorage": "AKST",                                           # Alaska (US)
    "Reykjavik": "GMT",                                            # Iceland
    "Dublin": "GMT",                                               # Ireland
    "Oslo": "CET",                                                 # Norway
    "Stockholm": "CET",                                            # Sweden
    "Helsinki": "EET",                                             # Finland
    "Bucharest": "EET",                                            # Romania
    "Sofia": "EET",                                                # Bulgaria
    "Tbilisi": "GET",                                              # Georgia
    "Yerevan": "AMT_Armenia",                                      # Armenia
    "Baku": "AZT",                                                 # Azerbaijan
    "Tirana": "CET",                                               # Albania
    "Dili": "TLT",                                                 # Timor-Leste
    "Apia": "TOT",                                                 # Samoa (Tonga Time)
    "Port Louis": "MUT",                                           # Mauritius
    "Victoria": "SCT",                                             # Seychelles
    "Antananarivo": "EAT",                                         # Madagascar
    "Nuuk": "WGT",                                                 # Greenland (Western Greenland Time)
    "San Juan": "AST_Atlantic",                                    # Puerto Rico
    "Hagåtña": "ChST",                                             # Guam (Chamorro Standard Time)
    "Nassau": "EST_US",                                            # Bahamas
    "Asunción": "PYT",                                             # Paraguay (Paraguay Time)
    "Montevideo": "UYT",                                           # Uruguay (Uruguay Time)
    "La Paz": "BOT",                                               # Bolivia (Bolivia Time)
    "Quito": "ECT",                                                # Ecuador (Ecuador Time)
    "Caracas": "VET",                                              # Venezuela (Venezuela Time)
    "San José": "CST_US",                                          # Costa Rica
    "Dili": "TLT",                                                 # East Timor (Timor-Leste Time)
    "Halifax": "AST_Atlantic",                                     # Canada (Atlantic Standard Time)
    "St. John's": "NST",                                           # Canada (Newfoundland Standard Time)
    "Guatemala City": "CST_US",                                    # Guatemala
    "Panama City": "EST_US"
}

DST_RULES = {

    "EST_US": {
        'start': (3, 2),  
        'end': (11, 1),   
        'dst_offset': 1,  
    },
    "PST_US": {
        'start': (3, 2),  
        'end': (11, 1),   
        'dst_offset': 1,
    },
    "CST_US": {
        'start': (3, 2),
        'end': (11, 1),
        'dst_offset': 1,
    },
    "AKST": {
        'start': (3, 2),
        'end': (11, 1),
        'dst_offset': 1,
    },
    "HST": {
        'start': (3, 2),
        'end': (11, 1),
        'dst_offset': 1,
    },
   
    "AEDT": {
        'start': (10, 1),  
        'end': (4, 1),     
        'dst_offset': 1,
    },
    "AEST": {
        'start': (10, 1),  
        'end': (4, 1),     
        'dst_offset': 1,
    },
    "ACST": {
        'start': (10, 1),
        'end': (4, 1),
        'dst_offset': 1,
    },
    
    "CET": {
        'start': (3, 5),   
        'end': (10, 5),    
        'dst_offset': 1,
    },
    "EET": {
        'start': (3, 5),
        'end': (10, 5),
        'dst_offset': 1,
    },
    "IST_Israel": {
        'start': (3, 5),
        'end': (10, 5),
        'dst_offset': 1,
    },
    
    "NZDT": {
        'start': (9, 5),  
        'end': (4, 1),    
        'dst_offset': 1,
    },
    
    "NST": {
        'start': (3, 2),
        'end': (11, 1),
        'dst_offset': 1,
    },
    
    "PYT": {
        'start': (10, 1),  
        'end': (3, 4),     
        'dst_offset': 1,
    },
    
    "ChST": {
        'start': (3, 2),
        'end': (11, 1),
        'dst_offset': 1,
    },
    "TOT": {
        'start': (9, 4),  
        'end': (4, 1),    
        'dst_offset': 1,
    }
}

def is_dst_active(tz: str, naive_time: datetime):
    """
    Check if DST is active for a given time zone and date.
    """
    if tz not in DST_RULES:
        return False
    
    dst_start_month, dst_start_week = DST_RULES[tz]['start']
    dst_end_month, dst_end_week = DST_RULES[tz]['end']

    dst_start = datetime(naive_time.year, dst_start_month, 1)
    dst_start += timedelta(days=(6 - dst_start.weekday()) + (dst_start_week - 1) * 7)

    dst_end = datetime(naive_time.year, dst_end_month, 1)
    dst_end += timedelta(days=(6 - dst_end.weekday()) + (dst_end_week - 1) * 7)

    return dst_start <= naive_time <= dst_end

def convert_time_by_code(from_tz: str, to_tz: str, time_str: str):
    """
    Convert time from time code to another, handling time zones and DST.
    """
    if from_tz not in TIME_ZONES or to_tz not in TIME_ZONES:
        return "Invalid time zone."

    naive_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

    from_offset = TIME_ZONES[from_tz]
    to_offset = TIME_ZONES[to_tz]

    if from_tz in DST_RULES:
        if is_dst_active(from_tz, naive_time):
            from_offset += DST_RULES[from_tz]['dst_offset']

    if to_tz in DST_RULES:
        if is_dst_active(to_tz, naive_time):
            to_offset += DST_RULES[to_tz]['dst_offset']

    time_difference = to_offset - from_offset
    converted_time = naive_time + timedelta(hours=int(time_difference), minutes=(time_difference % 1) * 60)

    return converted_time.strftime('%Y-%m-%d %H:%M:%S')

def convert_city_time(city_from: str, city_to: str, time_str: str):
    """
    Convert time from one city to another, handling time zones and DST.
    """
    city_from = city_from.title()
    city_to = city_to.title()
    
    city_from_tz = CITY_TIME_ZONES.get(city_from)
    city_to_tz = CITY_TIME_ZONES.get(city_to)
    
    if not city_from_tz or not city_to_tz:
        return "City not found."
    
    from_offset = TIME_ZONES.get(city_from_tz)
    to_offset = TIME_ZONES.get(city_to_tz)
    
    if from_offset is None or to_offset is None:
        return "Invalid time zone."
    
    naive_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    
    if city_from_tz in DST_RULES:
        if is_dst_active(city_from_tz, naive_time):
            from_offset += DST_RULES[city_from_tz]['dst_offset']
    
    if city_to_tz in DST_RULES:
        if is_dst_active(city_to_tz, naive_time):
            to_offset += DST_RULES[city_to_tz]['dst_offset']
    
    time_difference = to_offset - from_offset
    converted_time = naive_time + timedelta(hours=int(time_difference), minutes=(time_difference % 1) * 60)

    return converted_time.strftime('%Y-%m-%d %H:%M:%S')
