# Report. Lab1
Бабич Никита Станиславович 312400 Z33434 4 курс

## Цель
Познакомить студента с основами анализа алгоритмов на примере операций сортировки. 

## Methods
	Память	Худшее	Среднее	Лучшее	Устойчивость
    сортировка пузырьком	O(1)	O(n^2)	O(n^2)	O(n^2)	
    сортировка выбором	O(1)	O(n^2)	O(n^2)	O(n^2)	Нет
    сортировка вставкой	O(n) + O(1)	O(n^2)	O(n^2)	O(n)	
    цифровая сортировка (LSD, MSD)	O(w+n)	O(w*n)			да
    сортировка подсчетом	O(n+k)	O(n+k)		x \less len(x)	
    сортировка слиянием	O(1)+O(n)	O(n logn)	O(n logn)	O(n logn)
    шейкерная сортировка (сортировка перемешиванием) 	O(1)	O(n^2)	O(n^2)	O(n)	
    быстрая сортировка (сортировка Хоара)					
    сортировка кучей (пирамидальная	O(1)[+ O(n)]	O(n logn)	O(n logn)	O(n logn) [or O(n)]	нет
LSD – поразрядно
MSD - алфавитно

## Solve
Использованы 2 метода: сортировка вставками и сортировка пирамидльная (кучей)
Показано оптимальное время для заранее отсортированного набора данных
