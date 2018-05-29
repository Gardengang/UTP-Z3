
import timeit
# modified version
#N= 3 43s
from csp import *
# the interface between a philosopher and a folk
def PFI(i):
    return [CE(pickup,i,i), CE(putdown,i,i)]

# the behaviour of a philosopher
def PHILs(i):
    body = Seq(Seq(Seq(SP(CE(pickup,i,i)), SP(CE(pickup,i,(i+1)%N))), SP(CE(putdown,i,(i+1)%N))), SP(CE(putdown,i,i)))
    return RecP(body,0)

# the behaviour of a fork
def FORKs(i):
    body = EC(Seq(SP(CE(pickup,i,i)), SP(CE(putdown,i,i))), Seq(SP(CE(pickup,(i-1)%N,i)), SP(CE(putdown,(i-1)%N,i))))
    return RecP(body,1)

# the behaviour of a pair of a philosopher and a adjacent folk
def PFs(i):
    return Par(PFI(i), PHILs(i), FORKs(i))

# the interface of two pairs
def PFPI(i):
    if i==N-2:
        return [CE(pickup,i,(i+1)%N), CE(putdown,i,(i+1)%N), CE(pickup,N-1,0), CE(putdown,N-1,0)]
    else:
        return [CE(pickup,i,(i+1)%N), CE(putdown,i,(i+1)%N)]

# the interaction of all philosophers and folks
def PAR(n):

    # the behavour of the 0 and 1 pairs
    TP = Par(PFPI(0), PFs(0), PFs(1))

    # combine with other pairs
    for i in range(n-2):
        TP = Par( PFPI(i+1), TP, PFs(i+2))
    return TP

start = timeit.default_timer()
DLF(PAR(N))
stop = timeit.default_timer()
print(stop - start)


### a solution for deadlock
### one philosopher has a different order to pick up forks.
def MPHILs(i):
    body = Seq(Seq(Seq(SP(CE(pickup, i, (i+1)%N)), SP(CE(pickup, i, i))), SP(CE(putdown, i, i))),
               SP(CE(putdown, i, (i+1)%N)))
    return RecP(body, 0)


P = Par(PFPI(N-2), PAR(N-1), Par(PFI(N-1), MPHILs(N-1), FORKs(N-1)))

start = timeit.default_timer()
DLF(P)
stop = timeit.default_timer()
print(stop - start)
