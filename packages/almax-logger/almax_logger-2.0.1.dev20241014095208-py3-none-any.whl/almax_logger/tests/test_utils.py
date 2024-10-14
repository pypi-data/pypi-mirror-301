import unittest
from datetime import datetime, timedelta
from tools.utils import now, CalculateTimePassed, TimeToString  # Sostituisci 'your_module' con il nome del modulo corretto.

class TestTimeFunctions(unittest.TestCase):
    
    # Test per la funzione now()
    def test_now(self):
        current_time = now()
        self.assertIsInstance(current_time, datetime, "Il risultato della funzione now() deve essere un'istanza di datetime.")
    
    # Test per la funzione CalculateTimePassed()
    def test_calculate_time_passed_with_start(self):
        start_time = datetime.now() - timedelta(seconds=10)
        time_passed = CalculateTimePassed(start=start_time)
        self.assertGreaterEqual(time_passed.total_seconds(), 10, "Il tempo passato dovrebbe essere maggiore o uguale a 10 secondi.")
    
    def test_calculate_time_passed_without_start(self):
        # Il test per verificare un comportamento anomalo nel codice
        with self.assertRaises(TypeError, msg="Deve sollevare un TypeError se il parametro start non è un oggetto datetime."):
            CalculateTimePassed()  # start è definito come 0 nel codice originale, ma dovrebbe sollevare TypeError.
    
    # Test per la funzione TimeToString()
    def test_time_to_string(self):
        test_duration = timedelta(days=2, hours=3, minutes=45, seconds=30)
        result = TimeToString(test_duration)
        self.assertEqual(result, "2 Days = 51 Hours = 3105 Minutes = 186330.0 Seconds", 
                         "La funzione TimeToString() dovrebbe formattare correttamente il tempo passato in giorni, ore, minuti e secondi.")

    def test_time_to_string_zero_duration(self):
        zero_duration = timedelta(seconds=0)
        result = TimeToString(zero_duration)
        self.assertEqual(result, "0 Days = 0 Hours = 0 Minutes = 0.0 Seconds", 
                         "La funzione TimeToString() dovrebbe gestire correttamente una durata di zero secondi.")
        
if __name__ == '__main__':
    unittest.main()
