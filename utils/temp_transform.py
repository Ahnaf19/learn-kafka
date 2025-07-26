# utils/temp_transform.py

from loguru import logger


def i8n_weather(msg) -> dict:
    """Transform temperature data from Celsius to Fahrenheit and Kelvin.

    Args:
        msg (dict): The input message containing temperature data.

    Returns:
        dict: A dictionary with transformed temperature values.
    """
    celcius = msg['current']['temperature_2m']
    farenheit = (celcius * 9/5) + 32
    kelvin = celcius + 273.15
    
    logger.debug(f'Transformed temperature data: {celcius}°C to {farenheit}°F and {kelvin}K')
    
    return {
        'celcius': celcius,
        'farenheit': round(farenheit, 2),
        'kelvin': round(kelvin, 2)
    }
    