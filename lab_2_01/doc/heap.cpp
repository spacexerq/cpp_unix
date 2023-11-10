#include <iostream>
#include <cmath>
#include <chrono>
#include <cstdlib>

using namespace std;

void heapify(int list[], int listLength, int root)
{
	int largest = root;
	int l = 2*root + 1;
	int r = 2*root + 2;
	  
	if (l < listLength && list[l] > list[largest])
		largest = l;
	  
	if (r < listLength && list[r] > list[largest])
		largest = r;

	if (largest != root)
	{
		swap(list[root], list[largest]);
		heapify(list, listLength, largest);
	}
}
  
void heapSort(int list[], int listLength)
{
	for(int i = listLength / 2 - 1; i >= 0; i--){
		heapify(list, listLength, i);
		/*O(n)*/
	}
	for(int i = listLength - 1; i >= 0; i--)
	{
		swap(list[0], list[i]);
		heapify(list, i, 0);
		/*O(n log n)*/
	}
}
  
int main()
{
	int listL = 10;
	int list[listL] = {3,19,8,0,48,-59,-89,54,142,10};
	int listSorted[listL] = {-15, -10 , 2, 5, 18, 45, 100, 101, 108, 450};
	
	auto start1 = chrono::steady_clock::now();
 	heapSort(list, listL);
    auto end1 = chrono::steady_clock::now();
	auto diff1 = end1 - start1;
	
	auto start2 = chrono::steady_clock::now();
 	heapSort(listSorted, listL);
    auto end2 = chrono::steady_clock::now();
	auto diff2 = end2 - start2;

	for(int i = 0; i < listL; i++)
		cout << list[i] << '\t';
	cout << chrono::duration<double>(diff1).count();
	cout << endl;
	for(int i = 0; i < listL; i++)
		cout << listSorted[i] << '\t';
	cout << chrono::duration<double>(diff2).count();
}