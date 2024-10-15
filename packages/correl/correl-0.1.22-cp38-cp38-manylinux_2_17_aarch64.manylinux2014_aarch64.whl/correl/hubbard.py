#!/usr/bin/python
"""
Python module for calculating the Green's function and susceptibilities
for two approximations of the Hubbard model:
    - the atomic limit (atom class)
    - the meanfield AF solution (meanfield class)
Original functions for the atomic limit class have been created by
Dominik Robert Fus and later adapted by Matthias Reitner.
"""
__author__='Dominik Robert Fus, Matthias Reitner'

import numpy as np
import scipy.optimize as opt
from functools import partial
import itertools


class atom(object):
    """
    class to calculate the atomic limit for a given set of parameters

    attributes:
        U (float): value of Hubbard interaction.
        beta (float): inverse temperature.
        mu (float): chemical potential.
        h (float, optional): magnetic field.
        Niwf (int, optional): number of positive Matsubara frequencies

    """
    def __init__(self, U, beta, mu, h=0, Niwf=100) -> None:
        self.U = U
        self.beta = beta
        self.mu = mu
        self.h = h
        self.Niwf = int(Niwf)

    def Z(self):
        """
        returns:
            the partition function
        """
        return (1 + np.exp((self.mu+self.h)*self.beta)\
                + np.exp((self.mu-self.h)*self.beta)\
                + np.exp((2*self.mu-self.U)*self.beta))

    def n(self, h=None):
        """
        args:
            h (float, optional): magnetic field, default is self.h
        returns:
            the electron density (for one spin)
        """
        U = self.U
        mu = self.mu
        beta = self.beta
        if h is None:
            h = self.h
        # overflow handling for extreme parameters
        N = np.where(
            #if 
            mu>9*U/2,
                #then * e^-2ßµ/e^-2ßµ
                (np.exp((-mu+h)*beta)+np.exp(-U*beta))\
                /(np.exp(-2*mu*beta)+np.exp((-mu+h)*beta)\
                  +np.exp((-mu-h)*beta)+np.exp(-U*beta))
                #elif
                ,np.where(mu<-9*U/2,
                    #then
                    (np.exp((mu+h)*beta)+np.exp((2*mu-U)*beta))\
                    /(1+np.exp((mu+h)*beta)+np.exp((mu-h)*beta)\
                      +np.exp((2*mu-U)*beta))
                    #else * e^-ßµ/e^-ßµ
                    ,(np.exp(h*beta)+np.exp((mu-U)*beta))\
                    /(np.exp(-mu*beta)+np.exp(h*beta)\
                      +np.exp(-h*beta)+np.exp((mu-U)*beta))
        ))
        return N
    
    def n_total(self):
        """
        returns:
            the total electron density for both spin
        """
        return self.n()+self.n(h=-self.h)

    def m(self):
        """
        returns:
            magnetization = n(up) - n(down)
        """
        if self.h == 0:
            return 0.
        else:
            return self.n() - self.n(h=-self.h)
        
    def susz_c(self, omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            physical charge response
        """
        if omega !=0:
            return 0.
        else:
            return self.beta/2 *(
                (np.exp((self.mu+self.h)*self.beta)\
                + np.exp((self.mu-self.h)*self.beta)\
                + 4*np.exp((2*self.mu-self.U)*self.beta))/self.Z() \
                - (self.n_total())**2)
        
    def susz_sz(self, omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            physical longitudinal spin response
        """
        if omega !=0:
            return 0
        else:
            return self.beta/2 *(
                (np.exp((self.mu+self.h)*self.beta)\
                + np.exp((self.mu-self.h)*self.beta))/self.Z() \
                - (self.m())**2)
    
    def susz_sx(self, omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            physical transversal spin response
        """
        if self.h == 0:
            if omega != 0:
                return 0
            else:
                return self.beta * np.exp(self.beta*self.mu)/self.Z()
        else:
            if omega != 0:
                O = np.pi/self.beta*2*omega
                return np.exp(self.beta*self.mu)/self.Z()\
                    *(np.exp(self.beta*self.h) - np.exp(-self.beta*self.h))\
                    *2*self.h/(4*self.h**2+O**2)
            else:
                return np.exp(self.beta*self.mu)/self.Z()\
                    *(np.exp(self.beta*self.h) - np.exp(-self.beta*self.h))\
                    *1/(2*self.h)



    def iw(self, omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            fermionic Matsubara frequencies i(w + omega)
        """
        n_odd = 2*np.arange(-self.Niwf + omega,self.Niwf + omega)+1
        return 1j*np.pi/self.beta*n_odd

    def g(self, omega=0, h=None):
        """
        args:
            omega (int, optional): bosonic index shift
            h (float, optional): magnetic field, default is self.h
        returns:
            Green's function
        """
        U = self.U
        mu = self.mu
        if h is None:
            h = self.h
        N = self.n(h=-h)
        iw = self.iw(omega)
        return N/(iw+mu+h-U) + (1-N)/(iw+mu+h)


    def dg_diw(self, omega=0,h=None):
        """
        args:
            omega (int, optional): bosonic index shift
            h (float, optional): magnetic field, default is self.h
        returns:
            derivative of the Green's function (dG/diw)
        """
        U = self.U
        mu = self.mu
        if h is None:
            h = self.h
        N = self.n(h=-h)
        iw = self.iw(omega)
        return -N/(iw+mu+h-U)**2 - (1-N)/(iw+mu+h)**2

    def sigma(self, omega=0,h=None):
        """
        args:
            omega (int, optional): bosonic index shift
            h (float, optional): magnetic field, default is self.h
        returns:
            Selfenergy
        """
        if h is None:
            h = self.h
        G = self.g(omega=omega,h=h)
        iw = self.iw(omega)
        g0_1 = iw + self.mu + h
        return g0_1 - 1/G

    def g2uu(self, omega=0, h=None):
        """
        args:
            omega (int, optional): bosonic index shift
            h (float, optional): magnetic field, default is self.h
        returns:
            iw, iw' matrix of connected two-particle Green's function
            in spin up up up up in ph-convention <c+ c c+ c>
            for bosonic frequency omega
        """
        U = self.U
        mu = self.mu
        if h is None:
            h = self.h
        beta = self.beta
        N = self.n(h=-h)

        iw = self.iw()
        iw_o = self.iw(omega)
        nu_o = iw_o[:,None]
        nup = iw[None,:]

        x1 = nu_o+mu+h
        x_1 = nu_o+mu+h-U
        x2 = nup+mu+h
        x_2 = nup+mu+h-U


        delta = np.eye(2*self.Niwf)
        if omega == 0.:
            return beta * U**2 * N*(1-N) * (1-delta)/(x1*x_1*x2*x_2)
        else:
            return - beta * U**2 * N*(1-N) *delta/(x1*x_1*x2*x_2)


    def g2du(self, omega=0, h=None):
        """
        args:
            omega (int, optional): bosonic index shift
            h (float, optional): magnetic field, default is self.h
        returns:
            iw, iw' matrix of connected two-particle Green's function
            in spin down down up up ph-convention <c+ c c+ c>
            for bosonic frequency omega
        """
        U = self.U
        mu = self.mu
        if h is None:
            h = self.h
        beta = self.beta
        Nu = self.n(h=h)
        Nd = self.n(h=-h)
        #  Z* e^-ßµ
        z=(np.exp(-mu*beta) + np.exp(h*beta)\
           +np.exp(-h*beta) + np.exp((mu-U)*beta))

        iw = self.iw()
        iw_o = self.iw(omega)
        nu = iw[:,None]
        nu_o = iw_o[:,None]
        nup = iw[None,:]
        nup_o = iw_o[None,:]

        x1_m = nu_o+mu-h
        x_1_m = nu_o+mu-h-U
        x2_p = nup+mu+h
        x_2_p = nup+mu+h-U
        x3_p = nup_o+mu+h
        x_3_p = nup_o+mu+h-U
        x4_m = nu+mu-h
        x_4_m = nu+mu-h-U

        # delta(nu = nu')
        delta = np.eye(2*self.Niwf)
        # delta(nu + omega = -nu')
        delta_12 = np.eye(2*self.Niwf,k=omega)[:,::-1]

        if mu == U/2:
            hf_term = beta*delta_12/(2+np.exp(beta*(mu+h)) \
                                     +np.exp(beta*(mu-h))) \
                    *(1/x_1_m+1/x_2_p)*(1/x_3_p+1/x_4_m)
        else:
            hf_term = (Nu+Nd-1)/(nu_o+nup+2*mu-U)\
                    *(1/x_1_m+1/x_2_p)*(1/x_3_p+1/x_4_m)
            
        if h == 0:
            h0_term = - beta*delta/z*(1/x1_m-1/x_3_p)*(1/x4_m-1/x_2_p)
        else:
            h0_term = (Nu-Nd)/(nu_o-nup_o-2*h)\
                *(1/x1_m-1/x_3_p)*(1/x4_m-1/x_2_p)

        if omega == 0:
            w0_term = beta*U**2 *(np.exp(-beta*U)-1)/z**2 \
                    * 1/(x1_m*x_1_m*x2_p*x_2_p)
        else:
            w0_term = 0. 

        diag = hf_term +h0_term + w0_term

        offdiag = (Nu-1)/(x1_m*x_3_p*x4_m)  + (1-Nu)/(x1_m*x_2_p*x_3_p) \
                + (1-Nd)/(x_1_m*x2_p*x_3_p) + (Nd-1)/(x2_p*x_3_p*x4_m)  \
                + (1-Nd)/(x1_m*x2_p*x4_m)   + (1-Nd)/(x1_m*x2_p*x3_p)   \
                + (1-Nd)/(x_1_m*x3_p*x_4_m) + (Nd-1)/(x_1_m*x2_p*x3_p)  \
                + (1-Nd)/(x_2_p*x3_p*x_4_m) + (Nd-1)/(x1_m*x_2_p*x3_p)  \
                -    Nu/(x_1_m*x_2_p*x_4_m) -  Nu/(x_1_m*x_2_p*x_3_p)
        
        return diag+offdiag
    
    def f_uu(self, omega=0, h=None):
        """
        args:
            omega (int, optional): bosonic index shift
            h (float, optional): magnetic field, default is self.h
        returns:
            iw, iw' matrix of the full vertex in spin up up up up
            ph-convention <c+ c c+ c> for bosonic frequency omega
        """
        if h is None:
            h = self.h
        return -self.g2uu(omega=omega,h=h)\
            /(self.g(h=h)[:,None]*self.g(omega=omega,h=h)[:,None] \
              * self.g(h=h)[None,:]*self.g(omega=omega,h=h)[None,:])
    
    def f_du(self, omega=0, h=None):
        """
        args:
            omega (int, optional): bosonic index shift
            h (float, optional): magnetic field, default is self.h
        returns:
            iw, iw' matrix of the full vertex in spin down down up up
            ph-convention <c+ c c+ c> for bosonic frequency omega
        """
        if h is None:
            h = self.h
        return -self.g2du(omega=omega,h=h)\
            /(self.g(h=h)[:,None]*self.g(omega=omega,h=h)[:,None] \
              * self.g(h=h)[None,:]*self.g(omega=omega,h=h)[None,:])

    def chi_0(self, omega=0, h=None):
        """
        args:
            omega (int, optional): bosonic index shift
            h (float, optional): magnetic field, default is self.h
        returns:
            iw, iw' diagonal matrix of the ph bubble 
        """
        if h is None:
            h = self.h
        return - self.beta *np.diag(self.g(h=h)*self.g(omega=omega,h=h))
    
    def chi_uu(self, omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' matrix of the generalized susceptibility in
            spin up up up up ph-convention <c+ c c+ c> for bosonic
            frequency omega
        """
        return self.chi_0(omega=omega) + self.g2uu(omega=omega)
    
    def chi_dd(self, omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' matrix of the generalized susceptibility in
            spin down down down down ph-convention <c+ c c+ c> 
            for bosonic frequency omega
        """
        h = self.h
        return self.chi_0(omega=omega,h=-h) + self.g2uu(omega=omega,h=-h)
    
    def chi_du(self, omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' matrix of the generalized susceptibility in
            spin down down up up ph-convention <c+ c c+ c> 
            for bosonic frequency omega
        """
        return self.g2du(omega=omega)
    
    def chi_ud(self, omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' matrix of the generalized susceptibility in
            spin up up down down ph-convention <c+ c c+ c> 
            for bosonic frequency omega
        """
        h = self.h
        return self.g2du(omega=omega,h=-h)
    
    def chi_c(self, omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' matrix of the generalized charge susceptibility
            for bosonic frequency omega
        """
        h = self.h
        if h == 0:
            return self.chi_0(omega=omega) + self.g2uu(omega=omega)\
                + self.g2du(omega=omega)
        else:
            return (self.chi_uu(omega=omega) + self.chi_dd(omega=omega)\
                + self.chi_ud(omega=omega) + self.chi_du(omega=omega))/2


    def chi_s(self, omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' matrix of the generalized spin susceptibility
            for bosonic frequency omega
        """
        h = self.h
        if h == 0:
            return self.chi_0(omega=omega) + self.g2uu(omega=omega)\
                - self.g2du(omega=omega)
        else:
            return (self.chi_uu(omega=omega) + self.chi_dd(omega=omega)\
                - self.chi_ud(omega=omega) - self.chi_du(omega=omega))/2

        
    def chi_sc(self,omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' matrix of spin-charge component of the 
            generalized susceptibility (nonzero for h!=0)
            for bosonic frequency omega
        """
        return (self.chi_uu(omega=omega) - self.chi_dd(omega=omega)\
                + self.chi_ud(omega=omega) - self.chi_du(omega=omega))/2

    
    def chi_cs(self,omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' matrix of charge-spin component of the 
            generalized susceptibility (nonzero for h!=0)
            for bosonic frequency omega
        """
        return (self.chi_uu(omega=omega) - self.chi_dd(omega=omega)\
                - self.chi_ud(omega=omega) + self.chi_du(omega=omega))/2
    
    def X_sc(self,omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' matrix of the longitudinal generalized
            susceptibility in [[spin,   spin-charge]
                              ,[charge-spin, charge]]
            notation for bosonic frequency omega
        """
        return np.vstack((np.hstack((self.chi_s(omega=omega),
                                     self.chi_sc(omega=omega))),
                          np.hstack((self.chi_cs(omega=omega), 
                                     self.chi_c(omega=omega)))))
    
    def X0_sc(self,omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' diagonal matrix of the ph bubble
            in [[spin,   spin-charge]
               ,[charge-spin, charge]] notation
            for bosonic frequency omega
        """
        h = self.h
        x0u = self.chi_0(omega=omega) 
        x0d = self.chi_0(omega=omega,h=-h)
        return np.vstack((np.hstack(((x0u+x0d)/2,(x0u-x0d)/2)),
                          np.hstack(((x0u-x0d)/2,(x0u+x0d)/2))))
    
    def gamma(self,omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' matrix of the two-particle irreducible vertex
            in [[spin,   spin-charge]
               ,[charge-spin, charge]] notation
            for bosonic frequency omega
        """
        x = self.X_sc(omega=omega) 
        x0 = self.X0_sc(omega=omega)
        return np.linalg.inv(x) \
             - np.linalg.inv(x0)

    def gamma_c(self,omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' matrix of the two-particle irreducible vertex
            in the charge channel for bosonic frequency omega
        """
        assert self.h == 0, ("gamma_c only for h=0, "
                             "use self.gamma() for h!=0")
        return np.linalg.inv(self.chi_c(omega=omega)) \
             - np.linalg.inv(self.chi_0(omega=omega))
    
    def gamma_s(self,omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            iw, iw' matrix of the two-particle irreducible vertex
            in the spin channel for bosonic frequency omega
        """
        assert self.h == 0, ("gamma_c only for h=0, "
                             "use self.gamma() for h!=0")
        return np.linalg.inv(self.chi_s(omega=omega)) \
             - np.linalg.inv(self.chi_0(omega=omega))
    
    def sde_sigma(self):
        """
        calculates the self energy for given
        1 particle Green's function G,
        connected 2 particle Green's function G2_ud,
        inverse temperature beta,
        and Hubbard interaction U
        """
        beta = self.beta
        U = self.U 
        niwf = self.Niwf

        G = self.g()
        iO = np.arange(-niwf, niwf)
        G2_ud = np.moveaxis(np.array([self.g2du(omega=io) for io in iO]), 0 , -1)

        # dimensions
        Niv, Nivp, Niw = G2_ud.shape
        niv, = G.shape
        if Niv!=Nivp:
            raise ValueError("Fermionic frequencies nu, nu' must be same length")
        mid = niv//2
        iv_slice = slice(mid-Niv//2,mid+Niv//2)
        iv = 1j*(2*np.arange(-niv//2,niv//2)+1)*np.pi/beta

        # hartree term
        n = np.sum(G-1/iv)/beta + 0.5
        Σ = np.zeros((Niv),dtype='complex')
        Σ += U*n
        
        # vertex part of SDE
        temp = np.einsum('ijw, i -> i', G2_ud, 1/G[iv_slice])
        Σ += U/beta**2 * temp

        return Σ
    

    def skolimowskiDelta(self):
        """
        returns:
            violation of Luttinger count
        To Do:
            add magnetic field
        """
        assert self.h == 0, "currently only for h=0 implemented"
        def fermi(z):
            return 1/(np.exp(z)+1)
        N = self.n()
        return - fermi(-self.beta*self.mu)*N \
               + fermi(-self.beta*(self.mu-self.U))*(N-1) \
               + fermi(-self.beta*(self.mu+(N-1)*self.U))


class meanfield:
    """
    class to calculate the (antiferromagnetic) meanfield solution of
    the Hubbard model

    attributes:
        U (float): value of Hubbard interaction.
        beta (float): inverse temperature.
        mu (float): chemical potential (minus Hartree nU/2)
        t (float, optional): nearest neighbor hopping
        tpr (float, optional): next-nearest neighbor hopping
        tsec (float, optional): next-next-nearest neighbor hopping
        kpoints (int, optional): number of k-points in one dimension
        Niwf (int, optional): number of positive Matsubara frequencies
        deltino (float, optional): imaginary offset for real frequency
        D (float, optional): bandwith for real frequency
        vpoints (int, optional): number of real frequency points
        reduced_bz (bool, optional): reduced Brillouin zone
        para (bool, optional): enforce paramagnetic solution
        para_threshold (float, optional): set magnetization to zero
                                           for mag < thresh hold
        maxit (int, optional): maximum iterations for self-consistency

    """
    def __init__(self, U, beta, mu, t=1, tpr=0., tsec=0., 
                 kpoints: int=100, Niwf: int=100, 
                 deltino=1e-2, D=4, vpoints: int=401,
                 reduced_bz=True, para=False, para_threshold=1e-4,
                 maxit: int=3000) -> None:
        self.U = U
        self.beta = beta
        self.mu = mu
        self.t = t
        self.tpr = tpr
        self.tsec = tsec
        self.kpoints = kpoints
        self.Niwf =  Niwf
        self.deltino = deltino
        self.D = D
        self.vpoints = vpoints
        self.maxit = maxit
        k_end = np.pi/2 if reduced_bz else np.pi
        self.k = np.linspace(-k_end, k_end, kpoints, endpoint=False)
        if reduced_bz:
            self.kx = self.k[:,None]+self.k[None,:]
            self.ky = self.k[:,None]-self.k[None,:]
        else:
            self.kx = self.k[:,None]
            self.ky = self.k[None,:]
        if para:
            self.mag = 0.
        else:
            magnetization = self.m()
            if abs(magnetization) < para_threshold:
                self.mag = 0.
            else:
                self.mag = magnetization
    
    def iw(self, omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            fermionic Matsubara frequencies i(w + omega)
        """
        n_odd = 2*np.arange(-self.Niwf + omega,self.Niwf + omega)+1
        return 1j*np.pi/self.beta*n_odd
    
    def w(self, omega=0):
        """
        args:
            omega (float, optional): bosonic frequency shift
        returns:
            real frequencies: w + omega + i deltino
        """
        return np.linspace(-self.D+omega, self.D+omega, self.vpoints) \
            + 1j*self.deltino

    def ek(self,kx,ky):
        """
        args:
            kx (array): k-vector in x direction
            ky (array): k-vector in y direction
        returns:
            dispersion relation of 2D square lattice for 2 atomic basis
            for hopping between atoms (a) and atoms (b)
        """
        #kx = q[0]+self.k
        #ky = q[1]+self.k
        return  - 2*self.t*np.exp(1.j*kx)*(np.cos(kx)+np.cos(ky))
        
    def ek_pr(self,kx,ky):
        """
        args:
            kx (array): k-vector in x direction
            ky (array): k-vector in y direction
        returns:
            dispersion relation of 2D square lattice for 2 atomic basis
            for hopping between atoms (a) and atoms (a)
        """
        return  - 4*self.tpr*np.cos(kx)*np.cos(ky) \
                - 2*self.tsec*(np.cos(2*kx)+np.cos(2*ky))
        
    def m(self):
        """
        returns:
            magnetization of mean field AF Hubbard model
        """
        ek  = self.ek(self.kx,self.ky)
        ek_pr  = self.ek_pr(self.kx,self.ky)

        def eq_m(m):
            """
            returns:
                self consistent equation with 
                mean field magnetization at m_loop(m)=0
            """
            d = m*self.U/2
            E = np.sqrt(np.abs(ek)**2 + d*d)

            Gk_1 = 1/( np.exp(self.beta*(-E - self.mu + ek_pr))\
                       + np.ones(ek.shape) )
            Gk_2 = 1/( np.exp(self.beta*( E - self.mu + ek_pr))\
                       + np.ones(ek.shape) ) 
            return (np.sum((Gk_1 - Gk_2)*d/E,axis=(0,1)) / ek.size) - m
        
        try:
            M = opt.newton(eq_m,1,maxiter=self.maxit)
        except RuntimeError:
            print("Runtime Error, mean-field equation failed to converge:",
                  "set magnetization to zero")
            M = 0.
        return M
    
    def n(self):
        """
        returns:
            density of mean field AF Hubbard model
        """
        ek  = self.ek(self.kx,self.ky)
        ek_pr  = self.ek_pr(self.kx,self.ky)
        d = self.mag*self.U/2
        E = np.sqrt(np.abs(ek)**2 + d*d)

        Gk_1 = 1/( np.exp(self.beta*(-E - self.mu + ek_pr))\
                       + np.ones(ek.shape) )
        Gk_2 = 1/( np.exp(self.beta*( E - self.mu + ek_pr))\
                       + np.ones(ek.shape) ) 
        return (np.sum((Gk_1 + Gk_2),axis=(0,1)) / ek.size)

    def mu_hubbard(self):
        """
        returns:
            chemical potential of the mean field model
            (+ Hartree term)
        """
        return self.mu +self.U*self.n()/2

    def t_neel(self):
        """
        returns: 
            neal temperature of mean field AF Hubbard model 
        """
        ek  = self.ek(self.kx,self.ky)
        ek_pr  = self.ek_pr(self.kx,self.ky)

        def eq_beta(b):
            """returns 1/Tn = beta_c of mean field AF Hubbard model"""
            E = np.abs(ek)
            return (np.sum(
                        self.U/(2*E+1E-16) * (np.tanh(b*E)\
                        /(1+np.cosh(b*(self.mu - ek_pr))\
                           /np.cosh(b*E)))
                        ,axis=(0,1)) / ek.size) - 1
        return opt.newton(eq_beta,1,maxiter=self.maxit)

    def G(self,spin,q=[0,0],omega=0,mats=True):
        """
        args:
            spin (int): spin>0 up or spin<=0 down 
            q (array,optional): q shift in kx, ky
            omega (int, optional): bosonic index shift
            mats (bool, optional): Matsubara or real frequency
        returns: 
            Green's function of the AF Hubbard model
            in the 2 atomic basis a,b G[a,b,nu,kx,ky] 
            for int spin>0 up or spin<=0 down 
        """
        q = np.array(q)
        sigma = -1 if spin == 0 else np.sign(spin)
        ek  = self.ek(self.kx+q[0],self.ky+q[1])[None,:,:]
        ek_pr  = self.ek_pr(self.kx+q[0],self.ky+q[1])[None,:,:]

        mag = self.mag
        delta = mag*self.U/2
        mu = self.mu - ek_pr
        if mats:
            v = self.iw(omega=omega)[:,None,None]
        else :
            v = self.w(omega=omega)[:,None,None]
        z_p = np.array(v + mu + sigma*delta)
        z_m = np.array(v + mu - sigma*delta)

        denom = (z_m*z_p-np.abs(ek)**2)

        Gab = {
            "aa" : (z_m)/denom,
            "ab" : ek/denom,
            "ba" : np.conj(ek)/denom,
            "bb" : (z_p)/denom
        }
        return Gab

    def diagG(self,q=[0,0],omega=0,mats=True):
        """
        args:
            spin (int): spin>0 up or spin<=0 down 
            q (array,optional): q shift in kx, ky
            omega (int, optional): bosonic index shift
            mats (bool, optional): Matsubara (true) 
                                   or real frequency (false)
        returns:
            Green' function in the Nambu basis of the AF Hubbard model
            in the 2 atomic basis up,dn G[up,dn,nu,kx,ky] 
        """
        ek  = self.ek(self.kx+q[0],self.ky+q[1])[None,:,:]
        ek_pr  = self.ek_pr(self.kx+q[0],self.ky+q[1])[None,:,:]

        mag = self.mag
        delta = mag*self.U/2

        mu = self.mu  - ek_pr
        if mats:
            v = self.iw(omega=omega)[:,None,None]
        else :
            v = self.w(omega=omega)[:,None,None]
        E = np.sqrt(np.abs(ek)**2 + delta**2)
        Gud = {
            "up" : 1/(v + mu -E ),
            "dn" : 1/(v + mu +E ),
        }
        return Gud

    def diag_chi0_q(self,band):
        """
        args:
            band (int): 0/1
                        0 for Xc(q=0), Xs(q=Pi)
                        1 for Xc(q=Pi),Xs(q=0)
        returns:
            generalized static bubble susceptibility for 
            bosonic transfer momentum q from RPA in 
            Bogoliubov  basis
            [[upup,  0],
             [0, upup]]
            axis: (c/s, Matsubara frq, q points)
        """
        assert band in [0,1], "band index must be either 0 or 1"
        if band == 0:
            diagG = self.diagG()
        elif band == 1:
            diagG = self.diagG(q=[np.pi,np.pi])
        else:
            raise ValueError
        gu = diagG["up"]
        gd = diagG["dn"]
        gu_r = np.fft.fftn(gu,axes=(1,2))
        gd_r = np.fft.fftn(gd,axes=(1,2))

        Chi0_uu = -self.beta *  np.fft.ifftn(gu_r*gu_r,axes=(1,2))/self.kpoints**2
        Chi0_ud = -self.beta *  np.fft.ifftn(gu_r*gd_r,axes=(1,2))/self.kpoints**2
        Chi0_dd = -self.beta *  np.fft.ifftn(gd_r*gd_r,axes=(1,2))/self.kpoints**2
        Chi0_du = Chi0_ud
        zero = np.zeros(Chi0_uu.shape,dtype='complex')
        Chi0 = np.array([[Chi0_uu, Chi0_ud ],
                         [Chi0_du, Chi0_dd]])

        return Chi0

    def chi0_q(self,band):
        """
        args:
            band (int): for longitudinal component 0/1
                        0 for Xc(q=0), Xs(q=Pi)
                        1 for Xc(q=Pi),Xs(q=0)
        returns:
            generalized static bubble susceptibility for 
            bosonic transfer momentum q from RPA
            [[spin,        spin_charge],
             [charge_spin,      charge]]
            axis: (charge/spin, Matsubara frq, q points)
        """
        assert band in [0,1], "band index must be either 0 or 1"
        #calculate bubble
        g = self.G(1)
        # Fourier transform g(k) to g(r)
        gaa_r = np.fft.fftn(g["aa"],axes=(1,2))
        gbb_r = np.fft.fftn(g["bb"],axes=(1,2))
        gab_r = np.fft.fftn(g["ab"],axes=(1,2))
        gba_r = np.fft.fftn(g["ba"],axes=(1,2))

        # inverse Fourier transform  sum_r e^(iqr)g(-r)g(r) to X(q) = Sum_k g(k)g(k+q) 
        Chi0_AA_u = -self.beta *  np.fft.ifftn(gaa_r*gaa_r,axes=(1,2))/self.kpoints**2
        Chi0_AA_d = -self.beta *  np.fft.ifftn(gbb_r*gbb_r,axes=(1,2))/self.kpoints**2
        Chi0_AB_u = -self.beta *  np.fft.ifftn(gab_r*gab_r,axes=(1,2))/self.kpoints**2
        Chi0_AB_d = -self.beta *  np.fft.ifftn(gba_r*gba_r,axes=(1,2))/self.kpoints**2

        Chi0AA_s = 0.5*(Chi0_AA_u + Chi0_AA_d)
        Chi0AA_a = 0.5*(Chi0_AA_u - Chi0_AA_d)

        Chi0AB_s = (-1)**band*0.5*(Chi0_AB_u + Chi0_AB_d)
        Chi0AB_a = (-1)**band*0.5*(Chi0_AB_u - Chi0_AB_d)

        Chi0 = np.array([[Chi0AA_s + Chi0AB_s, Chi0AA_a - Chi0AB_a ],
                         [Chi0AA_a + Chi0AB_a, Chi0AA_s - Chi0AB_s]])

        return Chi0

    def chi_q(self,band, component):
        """
        args:
            band (int): for longitudinal component 0/1
                        0 for Xc(q=0), Xs(q=Pi)
                        1 for Xc(q=Pi),Xs(q=0)
            component (str): 's','c','sc',or 'cs'
                             's'  for spin
                             'c'  for charge
                             'sc' for spin-charge
                             'cs' for charge-spin
        returns:
            generalized static susceptibility for bosonic 
            transfer momentum q from RPA with the component
            s for spin, sc for spin_charge
        """
        assert band in [0,1], "band index must be either 0 or 1"
        assert component in ['s','c','sc','cs'], "component mus be 's','c','sc', or 'cs'"

        chi0 = np.moveaxis(self.chi0_q(band),[0,1,2,3,4],[3,4,2,0,1])
        chi0_1 = np.linalg.inv(chi0)

        Nmats = 2*self.Niwf
        qpoints = self.kpoints
        diag = np.arange(Nmats)

        gamma_11 =  self.U*np.ones((qpoints,qpoints,Nmats,Nmats),dtype='complex')/self.beta**2
        gamma_00 = -1*gamma_11[:]
        gamma_00[:,:,diag,diag] += chi0_1[:,:,:,0,0]
        gamma_11[:,:,diag,diag] += chi0_1[:,:,:,1,1]
        gamma_01 = chi0_1[:,:,:,0,1]
        gamma_10 = chi0_1[:,:,:,1,0]

        if component in ["s","cs"]:
            G_00 = np.linalg.inv(gamma_00\
                -gamma_01[:,:,:,None]*np.linalg.inv(gamma_11)\
                    *gamma_10[:,:,None,:])
            if component =="s":
                chiq = G_00
            else:
                chiq = - np.einsum('ijkl,ijlm->ijkm',np.linalg.inv(gamma_11),
                        gamma_10[:,:,:,None]*G_00)
        elif component in ["c","sc"]:
            G_11 = np.linalg.inv(gamma_11\
                -gamma_10[:,:,:,None]*np.linalg.inv(gamma_00)\
                    *gamma_01[:,:,None,:])
            if component =="c":
                chiq = G_11
            else:
                chiq = -np.einsum('ijkl,ijlm->ijkm',np.linalg.inv(gamma_00),
                        gamma_01[:,:,:,None]*G_11)

        return chiq

    def chi0_loc(self):
        """
        returns:
            local generalized static susceptibility bubble 
            [[spin,        spin_charge],
             [charge_spin,      charge]]
        """
        g = self.G(1)

        Chi0_AA_u = -self.beta * (np.sum(g["aa"] ,axis=(1,2))/self.kpoints**2)**2
        Chi0_AA_d = -self.beta * (np.sum(g["bb"] ,axis=(1,2))/self.kpoints**2)**2

        Chi0AA_s = 0.5*(Chi0_AA_u + Chi0_AA_d)
        Chi0AA_a = 0.5*(Chi0_AA_u - Chi0_AA_d)

        Nmats = 2*self.Niwf
        up_diag = np.arange(Nmats)
        dn_diag = np.arange(Nmats,2*Nmats)

        Chi0 = np.zeros((2*Nmats,2*Nmats),dtype='complex')
        Chi0[up_diag,up_diag] = Chi0AA_s
        Chi0[up_diag,dn_diag] = Chi0AA_a
        Chi0[dn_diag,up_diag] = Chi0AA_a
        Chi0[dn_diag,dn_diag] = Chi0AA_s
        
        return Chi0


    def chi_smpl_loc(self):
        """
        returns:
            calculate local susceptibility from DMFT like BSE
            (not the correct quantity)
        """
        g = self.G(1)
        Gu_AA = np.sum(g["aa"],axis=(1,2))/self.kpoints**2
        Gd_AA = np.sum(g["bb"],axis=(1,2))/self.kpoints**2
        Gu_AB = np.sum(g["ab"],axis=(1,2))/self.kpoints**2
        Gu_BA = np.sum(g["ba"],axis=(1,2))/self.kpoints**2
        Gd_AB = Gu_BA
        Gd_BA = Gu_AB


        Chi0_AA_u = -self.beta * Gu_AA *Gu_AA
        Chi0_AA_d = -self.beta * Gd_AA *Gd_AA
        Chi0_AB_u = -self.beta * Gu_AB *Gu_BA
        Chi0_AB_d = -self.beta * Gd_AB *Gd_BA

        Chi0AA_s = 0.5*(Chi0_AA_u + Chi0_AA_d)
        Chi0AA_a = 0.5*(Chi0_AA_u - Chi0_AA_d)


        Nmats = 2*self.Niwf
        up_diag = np.arange(Nmats)
        dn_diag = np.arange(Nmats,2*Nmats)

        Chi0AB_s = 0.5*(Chi0_AB_u + Chi0_AB_d)
        Chi0AB_a = 0.5*(Chi0_AB_u - Chi0_AB_d)

        Chi0_p = np.zeros((2*Nmats,2*Nmats),dtype='complex')
        Chi0_p[up_diag,up_diag] = Chi0AA_s + Chi0AB_s
        Chi0_p[up_diag,dn_diag] = Chi0AA_a - Chi0AB_a  
        Chi0_p[dn_diag,up_diag] = Chi0AA_a + Chi0AB_a
        Chi0_p[dn_diag,dn_diag] = Chi0AA_s - Chi0AB_s

        Chi0_m = np.zeros((2*Nmats,2*Nmats),dtype='complex')
        Chi0_m[up_diag,up_diag] = Chi0AA_s - Chi0AB_s
        Chi0_m[up_diag,dn_diag] = Chi0AA_a + Chi0AB_a  
        Chi0_m[dn_diag,up_diag] = Chi0AA_a - Chi0AB_a
        Chi0_m[dn_diag,dn_diag] = Chi0AA_s + Chi0AB_s

        Gamma = np.zeros((2*Nmats,2*Nmats),dtype='complex')
        Gamma[:Nmats,:Nmats] = -self.U/self.beta**2
        Gamma[Nmats:,Nmats:] = self.U/self.beta**2

        chi_p = np.linalg.inv(Gamma + np.linalg.inv(Chi0_p))
        chi_m = np.linalg.inv(Gamma + np.linalg.inv(Chi0_m))
        return (chi_p + chi_m)/2

    def chi_loc(self):
        """
        returns:
            local susceptibility from sum over chi_q
        """
        Xs_0 =  np.sum(self.chi_q(0,"s") ,axis=(0,1))/self.kpoints**2
        Xsc_0 = np.sum(self.chi_q(0,"sc"),axis=(0,1))/self.kpoints**2
        Xcs_0 = np.sum(self.chi_q(0,"cs"),axis=(0,1))/self.kpoints**2
        Xc_0 =  np.sum(self.chi_q(0,"c") ,axis=(0,1))/self.kpoints**2
        Xs_1 =  np.sum(self.chi_q(1,"s") ,axis=(0,1))/self.kpoints**2
        Xsc_1 = np.sum(self.chi_q(1,"sc"),axis=(0,1))/self.kpoints**2
        Xcs_1 = np.sum(self.chi_q(1,"cs"),axis=(0,1))/self.kpoints**2
        Xc_1 =  np.sum(self.chi_q(1,"c") ,axis=(0,1))/self.kpoints**2
        X = np.vstack((np.hstack(((Xs_0+Xs_1)/2,(Xsc_0+Xsc_1)/2)),
                       np.hstack(((Xcs_0+Xcs_1)/2,(Xc_0+Xc_1)/2))))
        return X

    def phys_bubble(self, spin, omega, q, transv=False, dynamic = False):
        """
        args:
            spin (int): spin>0 up or spin<=0 down 
            omega (float): bosonic frequency
            q (array): q bosonic transfer momentum [qx, qy]
            transv (bool, optional): transversal (True) 
                                     or longitudinal (False)
        returns:
           physical bubble(q,omega) suszeptibility in real frequency
           in the 2 atomic basis a,b 
           [[aa,ab],
            [ba,bb]] 
        """
        q = np.array(q)
        def fermi(E):
            return 1./(np.exp(self.beta*E) + 1)    
        sigma = -1 if spin == 0 else np.sign(spin)
        sigmap = -sigma if transv else sigma   
        ek  = self.ek(self.kx,self.ky)[:,:]
        ek_pr  = self.ek_pr(self.kx,self.ky)[:,:]
        ekq  = self.ek(self.kx+q[0],self.ky+q[1])[:,:]
        ek_prq  = self.ek_pr(self.kx+q[0],self.ky+q[1])[:,:]
        mag = self.mag
        Delta = mag*self.U/2
        mu = self.mu-ek_pr
        muq = self.mu-ek_prq
        Ek = np.sqrt(np.abs(ek)**2 + Delta**2)
        Ekq = np.sqrt(np.abs(ekq)**2 + Delta**2) 

        if Delta == 0:
            V_AA_a = 0.5
            V_AA_b = 0.5
            Vq_AA_a = 0.5
            Vq_AA_b = 0.5

            V_BB_a = 0.5
            V_BB_b = 0.5
            Vq_BB_a = 0.5
            Vq_BB_b = 0.5

            V_AB_a = -0.5
            V_AB_b = 0.5
            V_BA_a = -0.5
            V_BA_b = 0.5
            Vq_AB_a = -0.5
            Vq_AB_b = 0.5
            Vq_BA_a = -0.5
            Vq_BA_b = 0.5

        else:
            V_AA_a = 0.5*(1-sigma*Delta/Ek)
            V_AA_b = 0.5*(1+sigma*Delta/Ek)
            Vq_AA_a = 0.5*(1-sigmap*Delta/Ekq)
            Vq_AA_b = 0.5*(1+sigmap*Delta/Ekq)

            V_BB_a = 0.5*(1+sigma*Delta/Ek)
            V_BB_b = 0.5*(1-sigma*Delta/Ek)
            Vq_BB_a = 0.5*(1+sigmap*Delta/Ekq)
            Vq_BB_b = 0.5*(1-sigmap*Delta/Ekq)

            V_AB_a = -0.5*(np.conj(ek)/Ek)
            V_AB_b = 0.5*(np.conj(ek)/Ek)
            V_BA_a = -0.5*(ek/Ek)
            V_BA_b = 0.5*(ek/Ek)
            Vq_AB_a = -0.5*(np.conj(ekq)/Ekq)
            Vq_AB_b = 0.5*(np.conj(ekq)/Ekq)
            Vq_BA_a = -0.5*(ekq/Ekq)
            Vq_BA_b = 0.5*(ekq/Ekq)

        if np.array_equal(Ek-mu, Ekq-muq) and omega ==0 and dynamic:
            x_aa = np.zeros(Ek.shape,dtype='complex')
            x_bb = np.zeros(Ek.shape,dtype='complex')
        elif  np.array_equal(Ek-mu, Ekq-muq) and omega ==0:
            x_aa = -self.beta/(2+np.exp(self.beta*(Ek-mu))+np.exp(-self.beta*(Ekq-muq)))
            x_bb = -self.beta/(2+np.exp(self.beta*(-Ek-mu))+np.exp(-self.beta*(-Ekq-muq)))
        else:
            x_aa =(fermi(Ek-mu) - fermi(Ekq-muq))/(omega+1.j*self.deltino + Ek - Ekq)
            x_bb =(fermi(-Ek-mu) - fermi(-Ekq-muq))/(omega+1.j*self.deltino - Ek + Ekq) 
        x_ab =(fermi(Ek-mu) - fermi(-Ekq-muq))/(omega+1.j*self.deltino + Ek + Ekq)
        x_ba =(fermi(-Ek-mu) - fermi(Ekq-muq))/(omega+1.j*self.deltino - Ek - Ekq)

        chi0 = - np.array([
                 [np.sum(V_AA_a*(Vq_AA_a*x_aa + Vq_AA_b*x_ab) + V_AA_b*(Vq_AA_a*x_ba + Vq_AA_b * x_bb))/self.kpoints**2,
                  np.sum(V_AB_a*(Vq_BA_a*x_aa + Vq_BA_b*x_ab) + V_AB_b*(Vq_BA_a*x_ba + Vq_BA_b * x_bb))/self.kpoints**2]
                ,[np.sum(V_BA_a*(Vq_AB_a*x_aa + Vq_AB_b*x_ab) + V_BA_b*(Vq_AB_a*x_ba + Vq_AB_b * x_bb))/self.kpoints**2,
                  np.sum(V_BB_a*(Vq_BB_a*x_aa + Vq_BB_b*x_ab) + V_BB_b*(Vq_BB_a*x_ba + Vq_BB_b * x_bb))/self.kpoints**2]
                        ])
        return chi0

    def phys_chi0(self,band, omega, q, transv=False):
        """
        args:
            band (int): for longitudinal component 0/1
                        0 for Xc(q=0), Xs(q=Pi)
                        1 for Xc(q=Pi),Xs(q=0)
            omega (float): bosonic frequency
            q (array): q bosonic transfer momentum [qx, qy]
            transv (bool, optional): transversal (True) 
                                     or longitudinal (False)
        returns:
           physical bubble(q,omega) suszeptibility in real frequency
           transv=False:
           in the charge (c), spin (s) basis
           [[ss,sc],
            [cs,cc]]

           trasnv=True:
           in the two band spin basis 
           s->Sx(q=[0,0])
           S->Sx(q=[pi,pi])
           [[ss,sS],
            [Ss,SS]] 
        """
        assert band in [0,1], "band index must be either 0 or 1"
        x0 = self.phys_bubble(1, omega, q, transv=transv)
        if transv:
            xs = (x0[0,0] + x0[1,1])/2
            xa = (x0[0,0] - x0[1,1])/2
            x_s = (x0[0,1] + x0[1,0])/2
            x_a = (x0[0,1] - x0[1,0])/2
            x0l = np.zeros(x0.shape,dtype='complex')
            x0l[0,0]=xs-x_s
            x0l[0,1]=xa+x_a
            x0l[1,0]=xa-x_a
            x0l[1,1]=xs+x_s
        else:
            xs = (x0[0,0] + x0[1,1])/2
            xa = (x0[0,0] - x0[1,1])/2
            x_s = (-1)**band*(x0[0,1] + x0[1,0])/2
            x_a = (-1)**band*(x0[0,1] - x0[1,0])/2
            x0l = np.zeros(x0.shape,dtype='complex')
            x0l[0,0]=xs+x_s
            x0l[0,1]=xa-x_a
            x0l[1,0]=xa+x_a
            x0l[1,1]=xs-x_s
        return x0l

    def phys_chi(self, band, omega, q, transv=False):
        """
        args:
            band (int): for longitudinal component 0/1
                        0 for Xc(q=0), Xs(q=Pi)
                        1 for Xc(q=Pi),Xs(q=0)
            omega (float): bosonic frequency
            q (array): q bosonic transfer momentum [qx, qy]
            transv (bool, optional): transversal (True) 
                                     or longitudinal (False)
        returns:
           physical chi(q,omega) suszeptibility in real frequency
           transv=False:
           in the charge (c), spin (s) basis
           [[ss,sc],
            [cs,cc]]

           trasnv=True:
           in the two band spin basis 
           s->Sx(q=[0,0])
           S->Sx(q=[pi,pi])
           [[ss,sS],
            [Ss,SS]]
        """
        assert band in [0,1], "band index must be either 0 or 1"
        u = self.U
        x0 = self.phys_chi0(band, omega, q, transv=transv)
        if transv:
            gamma = [[-u, 0],
                     [0, -u]]
        else:
            gamma = [[-u, 0],
                     [0, u]]
        return np.linalg.inv(gamma + np.linalg.inv(x0))

    def phys_chi_loc(self, omega, transv=False):
        def sum_bands(Q):
            return (self.phys_chi(0,omega,[Q[0]+Q[1],Q[0]-Q[1]],transv=transv)\
                 + self.phys_chi(1,omega,[Q[0]+Q[1],Q[0]-Q[1]],transv=transv))/2
        Qlist = list(itertools.product(self.k,self.k))
        phys_loc = sum([sum_bands(Q) for Q in Qlist])
        return phys_loc/self.kpoints**2


class rpa:
    """
    class to calculate the paramagnetic random phase
    approximation of the Hubbard model

    attributes:
        U (float): value of Hubbard interaction.
        beta (float): inverse temperature.
        mu (float): chemical potential (minus Hartree nU/2)
        t (float, optional): nearest neighbor hopping
        tpr (float, optional): next-nearest neighbor hopping
        tsec (float, optional): next-next-nearest neighbor hopping
        kpoints (int, optional): number of k-points in one dimension
        Niwf (int, optional): number of positive Matsubara frequencies
        deltino (float, optional): imaginary offset for real frequency
        D (float, optional): bandwith for real frequency
        vpoints (int, optional): number of real frequency points
    """
    def __init__(self, U, beta, mu, t=1, tpr=0., tsec=0., 
                 kpoints: int=100, Niwf: int=100, 
                 deltino=1e-2, D=4, vpoints: int=401) -> None:
        self.U = U
        self.beta = beta
        self.mu = mu
        self.t = t
        self.tpr = tpr
        self.tsec = tsec
        self.kpoints = kpoints
        self.Niwf =  Niwf
        self.deltino = deltino
        self.D = D
        self.vpoints = vpoints
        self.k = np.linspace(-np.pi, np.pi, kpoints, endpoint=False)
        self.kx = self.k[:,None]
        self.ky = self.k[None,:]
    
    def iw(self, omega=0):
        """
        args:
            omega (int, optional): bosonic index shift
        returns:
            fermionic Matsubara frequencies i(w + omega)
        """
        n_odd = 2*np.arange(-self.Niwf + omega,self.Niwf + omega)+1
        return 1j*np.pi/self.beta*n_odd
    
    def w(self, omega=0):
        """
        args:
            omega (float, optional): bosonic frequency shift
        returns:
            real frequencies: w + omega + i deltino
        """
        return np.linspace(-self.D+omega, self.D+omega, self.vpoints) \
            + 1j*self.deltino

    def ek(self,kx,ky):
        """
        args:
            kx (array): k-vector in x direction
            ky (array): k-vector in y direction
        returns:
            dispersion relation of 2D square lattice 
        """
        return  - 2*self.t*(np.cos(kx)+np.cos(ky))

    def ek_pr(self,kx,ky):
        """
        args:
            kx (array): k-vector in x direction
            ky (array): k-vector in y direction
        returns:
            dispersion relation of 2D square lattice
        """
        return  - 4*self.tpr*np.cos(kx)*np.cos(ky) \
                - 2*self.tsec*(np.cos(2*kx)+np.cos(2*ky))

    def G(self,q=[0,0],omega=0,mats=True):
        """
        args:
            q (array,optional): q shift in kx, ky
            omega (int, optional): bosonic index shift
            mats (bool, optional): Matsubara or real frequency
        returns: 
            non interacting Green's function of the Hubbard model 
        """
        q = np.array(q)
        ek  = self.ek(self.kx+q[0],self.ky+q[1])[None,:,:]
        ek_pr  = self.ek_pr(self.kx+q[0],self.ky+q[1])[None,:,:]

        mu = self.mu 
        if mats:
            v = self.iw(omega=omega)[:,None,None]
        else :
            v = self.w(omega=omega)[:,None,None]
        return 1/(v + mu -ek -ek_pr)
    
    def chi0_q(self):
        """
        returns:
            generalized static bubble susceptibility for 
            bosonic transfer momentum q from RPA
        """
        g = self.G()
        # Fourier transform g(k) to g(r)
        g_r = np.fft.fftn(g,axes=(1,2))
        chi0 = -self.beta *  np.fft.ifftn(g_r*g_r,axes=(1,2))/self.kpoints**2
        return chi0

    def chi_q(self, component):
        """
        args:
            component (str): 's', or 'c'
                             's'  for spin
                             'c'  for charge
        returns:
            generalized static susceptibility for 
            bosonic transfer momentum q from RPA
            BSE equation
        """
        assert component in ['s','c'], "component mus be 's' or 'c'"
        Nmats = 2*self.Niwf
        qpoints = self.kpoints
        diag = np.arange(Nmats)

        chi0 = np.moveaxis(self.chi0_q(),[0,1,2],[2,0,1])
        chi0_1 = 1/chi0

        gamma =  self.U*np.ones((qpoints,qpoints,Nmats,Nmats),dtype='complex')/self.beta**2

        if component == "s":
            gamma = -1*gamma
            gamma[:,:,diag,diag] += chi0_1[:,:,:]
            chiq = np.linalg.inv(gamma)
        elif component == "c":
            gamma[:,:,diag,diag] += chi0_1[:,:,:]
            chiq = np.linalg.inv(gamma)
        return chiq

    def chi_loc(self, component):
        """
        args:
            component (str): 's', or 'c'
                             's'  for spin
                             'c'  for charge
        returns:
            local susceptibility from sum over chi_q
        """
        assert component in ['s','c'], "component mus be 's' or 'c'"

        return np.sum(self.chi_q(component) ,axis=(0,1))/self.kpoints**2