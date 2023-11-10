#include <iostream>
#include <cmath>
#include <chrono>
#include <cstdlib>

using namespace std;

void insertionSort(int list[], int listLength)
{
	for(int i = 1; i < listLength; i++)
	{
		int j = i - 1;
		while(j >= 0 && list[j] > list[j + 1])
		{
			swap(list[j], list[j + 1]);
			j--;
		}
	}
    /*O(n^2) if while close soon -> O(n)*/
}

int main()
{
	int listL = 10;
	int list[listL] = {3, 19, 8, 0, 48, -59, -89, 54, 142, 10};
	int listSorted[listL] = {-15, -10 , 2, 5, 18, 45, 100, 101, 108, 450};

    auto start1 = chrono::steady_clock::now();
 	insertionSort(list, listL);
    auto end1 = chrono::steady_clock::now();

    auto start2 = chrono::steady_clock::now();
 	insertionSort(listSorted, listL);
    auto end2 = chrono::steady_clock::now();
    
    auto diff1 = end1 - start1;
    auto diff2 = end2 - start2;

	for (int i = 0; i < listL; i++)
	{
	   cout<<list[i]<<"\t";
	}
    cout << chrono::duration<double>(diff1).count();
    cout << endl;
	for (int i = 0; i < listL; i++)
	{
	   cout<<listSorted[i]<<"\t";
	}
    cout << chrono::duration<double>(diff2).count();;
	return 0;
}