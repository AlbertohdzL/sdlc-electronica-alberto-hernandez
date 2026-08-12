def celsius_to_fahrenheit(c: float) -> float:
    """
    Convert Celsius to Fahrenheit.

    Parameters
    ----------
    c : float
        Temperature in degrees Celsius.

    Returns
    -------
    float
        Temperature in degrees Fahrenheit, rounded to 2 decimals.

    Raises
    ------
    ValueError
        If `c` is below absolute zero (-273.15 °C).
    """
    if c < -273.15:
        raise ValueError("Temperature below absolute zero (-273.15 °C)")
    return round(c * 9 / 5 + 32, 2)