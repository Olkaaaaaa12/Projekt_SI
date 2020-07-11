# lokalizacja

Do obliczenia prawdopodobieństwa wykorzystałam macierz 42x42 z zadania z wcześniejszych zajęć, która przechowuje prawdopodobieństwo przejścia między lokacjami. Dodatkowo stworzyłam macierz 4x4, która przechowuje prawdopodobieństwo orientacji agenta po danej akcji. Macierz uwzględniająca odczyty z sensora o wymiarach 42x4 bierze pod uwagę każdą możliwą lokalizację oraz każdą możliwą orientację i dla nich oblicza zgodność z odczytami z sensora.

Dodatkowo korzystam z wartości 'bump'. Jeżeli zmienna percept zawiera 'bump' to całą macierz przejść między lokacjami wypełniam jedynkami na przekątnej, ponieważ na 100% agent nie zmienił lokacji - odbił się od ściany.

Zasada poruszania się robota obejmuje kilka przypadków:
1) jeżeli sensor zwraca informację, o przeszkodzie z przodu i po prawej stronie ale po lewej nie oraz poprzednią akcją było przejście do przodu agent obróci się w lewo
2) analogicznie jeżeli przeszkoda jest z przodu i po lewej ale nie po prawej stronie to agent obróci się w prawo
3) jeżeli poprzednią akcją był ruch do przodu i przeszkoda jest na wprost ale nie ma ich po bokach bądź są po obu stronach to agent obróci się w lewo lub prawo, z dużo większym prawdopodobieństwem, że będzie to obrót w lewo
4) jeżeli poprzednią akcją był obrót i sensor zwraca informację o przeszkodzie na wprost to agent powtórzy obrót w tą samą stronę co w akcji poprzedniej
5) jeżeli sensor nie zwraca informacji o przeszkodzie przed agentem akcja jest losowana spośród wszystkich możliwych ale największe prawdopodobieństwo wylosowania ma ruch na wprost
