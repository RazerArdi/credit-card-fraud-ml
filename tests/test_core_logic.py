import pytest
import math
from datetime import datetime

# MOCK FUNCTIONS (Fungsi Simulasi)


def calculate_haversine(lat1, lon1, lat2, lon2):
    """Menghitung jarak spasial (kilometer) menggunakan formula Haversine."""
    if not (-90 <= lat1 <= 90 and -90 <= lat2 <= 90):
        raise ValueError("Latitude harus berada di rentang -90 hingga 90 derajat.")
    if not (-180 <= lon1 <= 180 and -180 <= lon2 <= 180):
        raise ValueError("Longitude harus berada di rentang -180 hingga 180 derajat.")

    R = 6371.0  # Radius ekuatorial bumi dalam km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def extract_transaction_hour(timestamp_str):
    """Mengekstrak fitur jam dari string timestamp mentah (Feature Engineering)."""
    dt_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return dt_obj.hour


# UNIT TESTS (Pytest Suite)


class TestSpatialFeatures:
    """Test suite untuk memvalidasi algoritma ekstraksi fitur geospasial."""

    @pytest.mark.parametrize(
        "coord, expected_distance",
        [
            (
                (-6.2088, 106.8456, -6.9175, 107.6191),
                116.24,
            ),  # Jakarta ke Bandung (~116.24 km)
            (
                (33.9659, -80.9355, 33.9863, -81.2007),
                24.6,
            ),  # Jarak aktual fraudTest.csv baris pertama
            (
                (-6.2088, 106.8456, -6.2088, 106.8456),
                0.0,
            ),  # Transaksi di koordinat yang persis sama
        ],
    )
    def test_haversine_distance_accuracy(self, coord, expected_distance):
        """Memvalidasi akurasi perhitungan jarak Haversine dengan margin error relasional 2%."""
        lat1, lon1, lat2, lon2 = coord
        distance = calculate_haversine(lat1, lon1, lat2, lon2)

        # Pengujian profesional pada float tidak menggunakan "==", melainkan math.isclose
        assert math.isclose(distance, expected_distance, rel_tol=0.02)

    def test_haversine_invalid_coordinates(self):
        """Memastikan sistem menolak data koordinat spasial yang korup/tidak valid."""
        with pytest.raises(ValueError, match="Latitude harus berada di rentang"):
            # Latitude 95.0 tidak masuk akal secara geografis
            calculate_haversine(95.0, 106.8456, -6.2088, 107.6191)


class TestTemporalFeatures:
    """Test suite untuk memvalidasi pemrosesan waktu transaksi."""

    @pytest.mark.parametrize(
        "timestamp, expected_hour",
        [
            ("2020-06-21 12:14:25", 12),  # Transaksi siang hari standar
            ("2019-04-22 00:02:01", 0),  # Transaksi tengah malam (potensi anomali)
            ("2026-12-31 23:59:59", 23),  # Transaksi batas akhir tahun
        ],
    )
    def test_transaction_hour_extraction(self, timestamp, expected_hour):
        """Memvalidasi isolasi variabel independen jam untuk deteksi penipuan temporal."""
        extracted_hour = extract_transaction_hour(timestamp)
        assert extracted_hour == expected_hour
        assert isinstance(extracted_hour, int)
