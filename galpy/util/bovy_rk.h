/*
  C implementations of Runge-Kutta integrators
 */
/*
Copyright (c) 2011, Jo Bovy
All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

   Redistributions of source code must retain the above copyright notice, 
      this list of conditions and the following disclaimer.
   Redistributions in binary form must reproduce the above copyright notice, 
      this list of conditions and the following disclaimer in the 
      documentation and/or other materials provided with the distribution.
   The name of the author may not be used to endorse or promote products 
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
*/
#ifndef __BOVY_RK_H__
#define __BOVY_RK_H__
/*
  include
*/
#include <bovy_symplecticode.h>
/*
  Function declarations
*/
void bovy_rk4(void (*func)(double, double *, double *,
			   int, struct leapFuncArg *),
	      int,
	      double *,
	      int, double *,
	      int, struct leapFuncArg *,
	      double, double,
	      double *);
inline void bovy_rk4_onestep(void (*func)(double, double *, double *,
					  int, struct leapFuncArg *),
			     int,
			     double *,double *,
			     double, double,
			     int, struct leapFuncArg *,
			     double *,double *);
inline void save_rk(int, double *, double *);
double rk_estimate_step(void (*func)(double , double *, double *,int, struct leapFuncArg *),
			 int, double *,
			 double, double *,
			 int,struct leapFuncArg *,
			 double,double,double);
#endif /* bovy_rk.h */