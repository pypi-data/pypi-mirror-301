import numpy as np
from pymgal import utils
from numba import njit
import time



# Speed up dust attenuation with numba since charlot_fall can be slow otherwise
@njit(parallel=True)
def charlot_fall_numba(ts1, ls1, tau1, tau2, tbreak):
    ls1 = np.reshape(ls1, (ls1.size, 1))
    ts1 = np.reshape(ts1, (1, ts1.size))

    taus = np.full(ts1.size, tau1)
    m = ts1.ravel() > tbreak
    if m.any():
        taus[m] = tau2
    return np.exp(-1.0 * taus * (ls1 / 5500.0) ** -0.7)


class charlot_fall(object):
    """ callable-object implementation of the Charlot and Fall (2000) dust law """
    tau1 = 0.0
    tau2 = 0.0
    tbreak = 0.0

    def __init__(self, tau1=1.0, tau2=0.5, tbreak=0.01):
        """ dust_obj = charlot_fall(tau1=1.0, tau2=0.3, tbreak=0.01)
        Return a callable object for returning the dimming factor as a function of age
        for a Charlot and Fall (2000) dust law.  The dimming is:

        np.exp(-1*Tau(t)(lambda/5500angstroms))

        Where Tau(t) = `tau1` for t < `tbreak` (in gyrs) and `tau2` otherwise. """

        self.tau1 = tau1
        self.tau2 = tau2
        self.tbreak = tbreak


    def __call__(self, ts, ls):
        ts1 = np.copy(ts)
        ls1 = np.copy(ls) 
        dust = charlot_fall_numba(ts1, ls1, self.tau1, self.tau2, self.tbreak)        
        return dust



# Calzetti seems to run faster without numba, but here is the implementation just in case
@njit(parallel=True)
def numba_calzetti(ls, esbv, rv):
    ks = np.zeros(ls.size)
    s = ls < .63
    if s.any():
        ks[s] = 2.659 * (-2.156 + 1.509 / ls[s] - 0.198 / ls[s]**2.0 +
                         0.011 / ls[s]**3.0) + rv
    l = ~s
    if l.any(): ks[l] = 2.659 * (-1.857 + 1.040 / ls[l]) + rv

    # calculate dimming factor as a function of lambda
    factors = 10.0**(-0.4 * esbv * ks)
    return factors



class calzetti(object):
    """ callable-object implementation of the Calzetti et al. (2000) dust law """
    av = 0.0
    rv = 0.0
    ebv = 0.0
    esbv = 0.0

    def __init__(self, av=1.0, rv=4.05):
        """ dust_obj = calzetti( av=1.0, rv=4.05 )
		Return a callable object for returning the dimming factor as a function of age
		for a Calzetti et al. (2000) dust law.  The dimming is:

		 """

        self.av = av
        self.rv = rv
        self.ebv = self.av / self.rv
        self.esbv = self.ebv * 0.44

    def __call__(self, ts, ls):

        # calzetti was fit in microns...
        ls = utils.convert_length(np.asarray(ls), incoming='a', outgoing='um')
        
        ks = np.zeros(ls.size)
        s = ls < .63
        if s.any():
            ks[s] = 2.659 * (-2.156 + 1.509 / ls[s] - 0.198 / ls[s]**2.0 +
                             0.011 / ls[s]**3.0) + self.rv
        l = ~s
        if l.any(): ks[l] = 2.659 * (-1.857 + 1.040 / ls[l]) + self.rv

        # calculate dimming factor as a function of lambda
        factors = 10.0**(-0.4 * self.esbv * ks)     #numba_calzetti(ls, self.esbv, self.rv)  # for numba use

        # need to return an array of shape (nls,nts).  Therefore, repeat
        return factors.reshape((ls.size, 1)).repeat(len(ts), axis=1)



