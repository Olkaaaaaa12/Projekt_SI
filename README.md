# lokalizacja

Kod napisany przeze mnie w ramach projektu z przedmiotu Sztuczna Inteligencja znajduje się w pliku agents/prob.py.

Do obliczenia prawdopodobieństwa wykorzystałam macierz 42x42 z zadania z wcześniejszych zajęć, która przechowuje prawdopodobieństwo przejścia między lokacjami. Dodatkowo stworzyłam macierz 4x4, która przechowuje prawdopodobieństwo orientacji agenta po danej akcji. Macierz uwzględniająca odczyty z sensora o wymiarach 42x4 bierze pod uwagę każdą możliwą lokalizację oraz każdą możliwą orientację i dla nich oblicza zgodność z odczytami z sensora.

Macierz 42x42 przechowująca wartości prawdopodobieństwa lokacji agenta w przypadku, gdy poprzednią akcją był obrót wypełniana jest jedynkami na przekątnej, ponieważ obrót nie spowodował zmiany lokacji i agent został w tym samym polu. Jeżeli poprzednią akcją był ruch do przodu, a sensor nie zwrócił informacji o odbiciu się od ściany - 'bump', sprawdzam w ile lokacji agent mógł przejść. Orientacja agenta nie jest znana przez co nie można jednoznacznie określić, który kierunek oznaczał dla agenta 'forward'. Zostało to zrealizowane poprzez iterację po każdej możliwej lokacji agenta (42 możliwe lokacje). Dla każdej lokacji sprawdzam, ile ścian znajduje się wokół niej. Sprawdzam 4 możliwe orientacje w każdej lokacji i testuję czy akcja 'forward' mogłaby dojść do skutku w tej orientacji (czy lokacja przed agentem jest wolna, nie ma na niej ściany). Następnie zliczam w ile z tych lokacji agent mógł pójść, maksymalnie 4 (wokół agenta nie ma ścian), minimalnie 1 (wokół agenta są 3 ściany, nie 0, ponieważ wtedy sensor musiałby zwrócić 'bump). W przypadku 'forward' jest 5% szansy, że agent nie ruszył się, czyli 95%, że przeszedł do innej lokacji. Do każdej lokacji, do której agent mógł przejść wpisuję wartość 0.95 podzieloną przez ilość możliwych lokacji. Przykładowo, jeżeli wokół agenta jest 1 ściana, co oznacza, że agent mógł przejść w 3 pozostałe lokacje, to 0.95 dzielę przez 3. 5% prawdopodobieństwa, że agent został w miejscu i po 31.7%, że jest w jednej z tych 3 lokacji.

W przypadku macierzy 4x4 przechowującej prawdopodobieństwo orientacji agenta, jeżeli poprzednią akcją było 'forward', macierz wypełniana jest jedynkami na przekątnej, ponieważ orientacja agenta pozostała bez zmian. Jeżeli poprzednią akcją był skręt w lewo lub  w prawo to każdej potencjalnej poprzedniej orientacji przypisuje wartość 0.05, ponieważ takie jest prawdopodobieństwo, że agent się nie obrócił a następnie zgodnie z kierunkiem przypisuje następnej orientacji wartość 0.95. 

Dodatkowo korzystam z wartości 'bump'. Jeżeli zmienna percept zawiera 'bump' to całą macierz przejść między lokacjami wypełniam jedynkami na przekątnej, ponieważ na 100% agent nie zmienił lokacji - odbił się od ściany.

Wartości w macierzy sensora obliczane są poprzez mnożenie 1 z 0.9 w przypadku, gdy układ ścian zgadza się z odczytami sensora i z 0.1, gdy się nie zgadza. Dodatkowo wykorzystana jest również wartość 'bump'. Jeżeli w danej lokacji i orientacji w kierunku 'forward' znajduje się ściana i dodatkowo sensor zwrócił 'bump' to wartość wpisywana do macierzy mnożona jest z 100% (nie jest pomniejszana), ponieważ jeżeli sensor zwraca informacje, że w kierunku 'forward' znajduje się ściana oraz 'bump', czyli agent w tą ścianę uderzył to mamy 100% pewności, że sensor zwrócił poprawną informację. Dodatkowo, gdy sensor zwraca 'bump' to  wszystkie lokacje z orientacjami takimi, że w kierunku 'forward' nie ma ściany są mnożone z zerem, ponieważ jest 0% szansy, że ta kombinacja lokacji i orientacji jest tą, która jest szukana.   

Zasada poruszania się robota obejmuje kilka przypadków:
1) jeżeli sensor zwraca informację, o przeszkodzie z przodu i po prawej stronie ale po lewej nie oraz poprzednią akcją było przejście do przodu agent obróci się w lewo
2) analogicznie jeżeli przeszkoda jest z przodu i po lewej ale nie po prawej stronie to agent obróci się w prawo
3) jeżeli poprzednią akcją był ruch do przodu i przeszkoda jest na wprost ale nie ma ich po bokach bądź są po obu stronach to agent obróci się w lewo lub prawo, z dużo większym prawdopodobieństwem, że będzie to obrót w lewo
4) jeżeli poprzednią akcją był obrót i sensor zwraca informację o przeszkodzie na wprost to agent powtórzy obrót w tą samą stronę co w akcji poprzedniej
5) jeżeli sensor nie zwraca informacji o przeszkodzie przed agentem akcja jest losowana spośród wszystkich możliwych ale największe prawdopodobieństwo wylosowania ma ruch na wprost
