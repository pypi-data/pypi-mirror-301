//=============================================================
//(c) 2011 Distributed under MIT-style license. 
//(see LICENSE.txt or visit http://opensource.org/licenses/MIT)
//=============================================================


#include <math.h>
#include <numeric>
#include <stdio.h>
#include <iostream>
#include <algorithm>
#include <vector>
#include <iterator>
#include <limits>

extern "C"{
void mdl(int* in, int dsize, int* arity, int asize, int complexity, double* out)
{
	int64_t ri=arity[0];
	int *drepr = new int[dsize]; 
	int abasis[asize]; abasis[0]=0;
	int qi = 0.0;
	double penalty = 0.0;

	out[0] = 0.0;
	out[1] = 0.0;
	
	if (asize>1){
		abasis[1]=1;
		std::partial_sum(arity+1,arity+asize-1, abasis+2, std::multiplies<int>());
		qi = std::accumulate(arity+1, arity+asize, 1, std::multiplies<int>());
		penalty = (ri-1)*qi*(log(dsize)*0.5*complexity+1-complexity);
	}

	
	int row[asize];
	for(int i=0; i<dsize; i++){
		for( int j = 0; j<asize; ++j ) row[j] = in[i*asize + j] ;
		drepr[i] = std::inner_product( row, row + asize, abasis, 0 );
	}
	int64_t cpt_size = *std::max_element(drepr, drepr+dsize)+1;
	

	std::vector<int> N_ijk (cpt_size*ri,0);
	for (int i=0; i<dsize; i++){
		N_ijk[drepr[i]*ri+in[asize*i]]+=1;
	}

	//std::vector<double> Nij (cpt_size,0.0);
	int nijk=0, nij=0;
	double LL=0.0;

	for(int i=0; i<cpt_size; i++){
		nij=std::accumulate(N_ijk.begin()+ri*i, N_ijk.begin()+ri*(i+1), 0);
		if(nij > 0){
			for(int j=0; j<ri; j++){
				nijk=N_ijk[ri*i+j];
				if(nijk > 0){
					LL += nijk*log( (double)nijk/nij );
				}
			}
		}
	}

	//std::copy(Nijk.begin(), Nijk.end(), std::ostream_iterator<double>(std::cout, " "));
	//std::cout<<std::endl;

	//for(double n : Nijk){ if ( n>0 ){ H+=n*log(n);} };
	//for(double n : Nij){ if ( n>0 ){ H-=n*log(n);} };
	out[0] = -(LL - penalty)/dsize;

	delete[] drepr;
}


void mu(int* in, int dsize, int* arity, int asize,  double* out)
{
	int64_t ri=arity[0];
	//int *drepr = new int[dsize]; 
	int abasis[asize]; abasis[0]=0;
	
	if (asize>1){
		abasis[1]=1;
		std::partial_sum(arity+1,arity+asize-1, abasis+2, std::multiplies<int>());
	}
	//std::cout<<"basis"<<std::endl;
	//std::copy(abasis, abasis+asize, std::ostream_iterator<int>(std::cout," "));
	//std::cout<<std::endl;

	int row[asize];
	std::vector<int> drepr (dsize,0);
	for(int i=0; i<dsize; i++){
		for( int j = 0; j<asize; ++j ) row[j] = in[i*asize + j] ;
		drepr[i] = std::inner_product( row, row + asize, abasis, 0 );
	}

	//std::sort(drepr.begin(), drepr.end());
	//std::vector<int>::iterator it;
	//it = std::unique(drepr.begin(), drepr.end(), std::equal_to<int>());
	//int cpt_size = std::distance( drepr.begin(), it );
	int64_t cpt_size = *std::max_element(drepr.begin(), drepr.end())+1;
	
	std::vector<int> N_ijk (cpt_size*ri,0);
	for (int i=0; i<dsize; i++){
		N_ijk[drepr[i]*ri+in[asize*i]]+=1;
	}

	//std::vector<double> Nij (cpt_size,0.0);
	int nijk,nij;
	double mu = 0.0, LL = 0.0;
	const double PI = 3.141592653589793;
	const double XI = 2+PI*PI/24;

	for(int i=0; i<cpt_size; i++){
		//Nij[i]=std::accumulate(Nijk.begin()+ri*i, Nijk.begin()+ri*(i+1), 0);

		nij=std::accumulate(N_ijk.begin()+ri*i, N_ijk.begin()+ri*(i+1), 0);
		if (nij > 0){
			mu += log( (double)nij ) + XI;
			for (int j=0; j<ri; j++){
				nijk = N_ijk[ri*i+j];
				if (nijk > 0){
					LL += nijk * log( (double)nijk/nij );
				}
			}
		}
	}

	//for(double n : Nij){ if ( n>0 ){ H+=n*log(n);} };
	//for(double n : Nijk){ if ( n>0 ){ H-=n*log(n);} };


	out[0] = -LL/dsize;


	//for( double n : Nij ){ if ( n > 0 ){ mu += log(n) + XI; } };
	out[1] = mu/dsize;

	//std::copy(Nijk.begin(), Nijk.end(), std::ostream_iterator<double>(std::cout, " "));
	//std::cout<<std::endl;


	//delete[] drepr;

}






			
}
