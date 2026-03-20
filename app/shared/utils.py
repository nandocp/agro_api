import re
import unicodedata
from decimal import Decimal

from .enums import MaxSlopePercent, SlopeClass


def digits_only(value: str) -> str:
    return ''.join(filter(str.isdigit, value))


def slugify(value: str) -> str:
    value = unicodedata.normalize('NFKD', value)
    value = value.encode('ascii', 'ignore').decode('ascii')
    value = value.lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    value = re.sub(r'-+', '-', value)
    value = value.strip('-')
    return value


def classify_slope(slope_percent: Decimal) -> SlopeClass:
    if slope_percent <= MaxSlopePercent.FLAT:
        return SlopeClass.FLAT
    if slope_percent <= MaxSlopePercent.GENTLE:
        return SlopeClass.GENTLE
    if slope_percent <= MaxSlopePercent.MODERATE:
        return SlopeClass.MODERATE
    if slope_percent <= MaxSlopePercent.STRONG:
        return SlopeClass.STRONG
    if slope_percent <= MaxSlopePercent.STEEP:
        return SlopeClass.STEEP
    return SlopeClass.VERY_STEEP
