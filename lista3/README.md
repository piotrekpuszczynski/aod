Piotr Puszczyński
Grudzień 10 2021

Folder zawiera plik z metodami tworzącymi graf i wyszukującymi w nim najkrótsze 
ścieżki algorytmem dijkstry i jego alternywami. Zawiera też plik 
obsługujący argumety, który czyta plik, tworzy graf, wykonuje odpowiedni 
algorytm i zapisuje wyniki do pliku.

Jak skompilować i użyc algorytmów:
1) 
    make
    

    kompiluje pliki
3) 
    ./main dijkstra/dial/radixheap -d plik.gr -ss plik.ss -oss plik.ss.res

    ./main dijkstra/dial/radixheap -d plik.gr -p2p plik.p2p -op2p plik.p2p.res


    używa wybranego algorytmu na podanych danych z odpowiednimi parametrami:
    -d - plik z danymi do grafu
    -ss - plik z danymi wierzchołkami do znaleźienie najktótszej ścieżki
    -oss - plik z czasem wykonywania się algorytmu na podanych wierzchołkah
    -p2p - plik z parami wierzchołków dla których program ma obliczyc najkrótsze ścieżki
    -op2p - plik z odlełością między podanymi parami wierzchołków
4) 
    make clean


    usuwa pliki wykonywalne

pliki -d, -ss, -p2p muszą być w katalogu /in (w parametrze wpisać tylko nazwę pliku, bez katalogu /in),
podobnie -oss i -op2p, które są zapisywane w katalogu /out