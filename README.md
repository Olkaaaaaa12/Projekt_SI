# lokalizacja

Do obliczenia prawdopodobieństwa wykorzystałam macierz 42x42 z zadania z wcześniejszych zajęć, która przechowuje prawdopodobieństwo przejścia między lokacjami. Dodatkowo stworzyłam macierz 4x4, która przechowuje prawdopodobieństwo orientacji agenta po danej akcji. Macierz uwzględniająca odczyty z sensora o wymiarach 42x4 bierze pod uwagę każdą możliwą lokalizację oraz każdą możliwą orientację i dla nich oblicza zgodność z odczytami z sensora.
