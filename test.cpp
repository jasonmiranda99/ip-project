#include<iostream>
using namespace std;

int main()
{
	int m;
	cout<<"Enter semester: ";
	cin>>m;
	
	int credits[]={16,18,23,24,22,22,17,18};
	float cgpa,sgpa;
	
	cout<<"Enter previous cgpa:\n";
		cin>>cgpa;
	
	cout<<"Enter current sgpa:\n";
		cin>>sgpa;
	
	int totalcredits=0;
	for(int i=0;i<m-1;i++)
		totalcredits+=credits[i];
		
	float num=(cgpa*totalcredits)+(credits[m-1]*sgpa);
	totalcredits+=credits[m-1];
		
	cout<<(float)num/totalcredits;
}
