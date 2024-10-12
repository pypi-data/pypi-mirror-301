from datetime import datetime

from src.anemos.weather import AnemosObjectTypes, v2get


def test_get():
    assert len(v2get("100-0005")) > 0

def test_get_with_object_type():
    assert len(v2get("100-0005", AnemosObjectTypes.WeatherWarning)) > 0

