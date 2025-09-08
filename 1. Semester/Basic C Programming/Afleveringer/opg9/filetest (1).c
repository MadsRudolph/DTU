#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#define listsize 100   //defines array size
int listarray[listsize];   //an array of int

struct  Record  { 
    char  name[50];
    char  address[50]; 
    int  age;
    unsigned  int  phone;
};

struct Record  list[100];


int  binarySearch(int  x) ;
void  sortList();

int main() {
    printf("Hello Easy C project!");
}

int  binarySearch(int  x)  {	//  search  for  an  element  =  x int  low;	//  low	end  of  search  interval
int  high;	                    //  high  end  of  search  interval
int  mid=0;	                    //  middle  of  search  interval
int low  =  0;	                //  index  to  first  element
high  =  listsize  -  1;	    //  index  to  last  element
mid=(high-low)/2;
while  (low  <  high)  {	    //  continue  until  search  interval  is  zero  length mid  =  (low  +  high)  /  2;	
                                //  find  middle  point
if  (x  <=  listarray[mid])  {	    //  compare  middle  element
high  =  mid;	                //  new  interval  is  from  low  to  mid
}
else  {
low  =  mid  +  1;	            //  new  interval  is  from  mid+1  to  high
}
}
if  (listarray[low]  ==  x)  {	    //  did  we  find  the  value  we  were  looking  for? return  low;	
   return  1;                           //  yes.  return  index  to  where  the  value  was  found
}
else  {
return  -1;	                    //  value  was  not  found.  return  an  error  code
}
}

void  sortList()  {
bool  swapped  =  true;	       //  remember  if  we  have  swapped  elements
int  i=0;	                   //  index
int  j  =  0;	               //  counting  number  of  runs
int  temp=0;	               //  temporary  storage  during  swapping
while  (swapped)  {	           //  repeat  as  long  as  there  is  something  to  swap j++;	
                               //  count  number  of  runs
swapped  =  false;
for  (i  =  0;  i  <  listsize-j;  i++)  {  //  loop  through  list
 
if  (listarray[i]  >  listarray[i+1])  {  //  if  element  is  bigger  than  the  next temp  =  list[i];	
                                //  swap  list[i]  and  list[i+1]  list[i]  =  list[i+1];
temp= listarray[i];
listarray[i+1]  =  temp;
swapped  =  true;	            //  remember  that  we  swapped
}
}
}
}
 