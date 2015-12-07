###############################################################################
#   MN3ExponentialDiskPotential.py: class that implements the three Miyamoto-
#                                   Nagai approximation to a radially 
#                                   exponential disk potential of Smith et al.
#                                   2015
###############################################################################
import numpy
import warnings
from galpy.util import galpyWarning
from galpy.potential_src.Potential import Potential, kms_to_kpcGyrDecorator
from galpy.potential_src.MiyamotoNagaiPotential import MiyamotoNagaiPotential
class MN3ExponentialDiskPotential(Potential):
    """class that implements the three Miyamoto-Nagai approximation to a radially-exponential disk potential of `Smith et al. 2015 <http://adsabs.harvard.edu/abs/2015arXiv150200627S>`_

    .. math::

        \\rho(R,z) = \\mathrm{amp}\\,\\exp\\left(-R/h_R-|z|/h_z\\right)

    or 

    .. math::

        \\rho(R,z) = \\mathrm{amp}\\,\\exp\\left(-R/h_R\\right)\\mathrm{sech}^2\\left(-|z|/h_z\\right)

    depending on whether sech=True or not. This density is approximated using three Miyamoto-Nagai disks

    """
    def __init__(self,amp=1.,hr=1./3.,hz=1./16.,
                 sech=False,posdens=False,
                 normalize=False):
        """
        NAME:

           __init__

        PURPOSE:

           initialize a 3MN approximation to an exponential disk potential

        INPUT:

           amp - amplitude to be applied to the potential (default: 1)

           hr - disk scale-length

           hz - scale-height

           sech= (False) if True, hz is the scale height of a sech vertical profile (default is exponential vertical profile)

           posdens= (False) if True, allow only positive density solutions (Table 2 in Smith et al. rather than Table 1)

           normalize - if True, normalize such that vc(1.,0.)=1., or, if given as a number, such that the force is this fraction of the force necessary to make vc(1.,0.)=1.

        OUTPUT:

           MN3ExponentialDiskPotential object

        HISTORY:

           2015-02-07 - Written - Bovy (IAS)

        """
        self._hr= hr
        self._hz= hz
        self._scale= self._hr
        Potential.__init__(self,amp=amp*4.*numpy.pi*self._hr**2.*self._hz)
        # First determine b/rd
        if sech:
            self._brd= _b_sechhz(self._hz/self._hr)
        else:
            self._brd= _b_exphz(self._hz/self._hr)
        if self._brd < 0.:
            raise IOError("MN3ExponentialDiskPotential's b/Rd is negative for the given hz")
        # Check range
        if (not posdens and self._brd > 3.) \
                or (posdens and self._brd > 1.35):
            warnings.warn("MN3ExponentialDiskPotential's b/Rd = %g is outside of the interpolation range of Smith et al. (2015)" % self._brd,
                          galpyWarning)
        self._b= self._brd*self._hr
        # Now setup the various MN disks
        if posdens:
            self._mn3= [MiyamotoNagaiPotential(amp=_mass1_tab2(self._brd),
                                               a=_a1_tab2(self._brd)*self._hr,
                                               b=self._b),
                        MiyamotoNagaiPotential(amp=_mass2_tab2(self._brd),
                                               a=_a2_tab2(self._brd)*self._hr,
                                               b=self._b),
                        MiyamotoNagaiPotential(amp=_mass3_tab2(self._brd),
                                               a=_a3_tab2(self._brd)*self._hr,
                                               b=self._b)]
        else:
            self._mn3= [MiyamotoNagaiPotential(amp=_mass1_tab1(self._brd),
                                               a=_a1_tab1(self._brd)*self._hr,
                                               b=self._b),
                        MiyamotoNagaiPotential(amp=_mass2_tab1(self._brd),
                                               a=_a2_tab1(self._brd)*self._hr,
                                               b=self._b),
                        MiyamotoNagaiPotential(amp=_mass3_tab1(self._brd),
                                               a=_a3_tab1(self._brd)*self._hr,
                                               b=self._b)]
        if normalize or \
                (isinstance(normalize,(int,float)) \
                     and not isinstance(normalize,bool)):
            self.normalize(normalize)
        self.hasC= True
        self.hasC_dxdv= True
        self._nemo_accname= 'MiyamotoNagai+MiyamotoNagai+MiyamotoNagai'
        return None

    def _evaluate(self,R,z,**kwargs):
        """
        NAME:
           _evaluate
        PURPOSE:
           evaluate the potential at R,z
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
        OUTPUT:
           Phi(R,z)
        HISTORY:
           2015-02-07 - Written - Bovy (IAS)
        """
        return self._mn3[0](R,z)+self._mn3[1](R,z)\
            +self._mn3[2](R,z)

    def _Rforce(self,R,z,**kwargs):
        """
        NAME:
           _Rforce
        PURPOSE:
           evaluate the radial force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
        OUTPUT:
           the radial force
        HISTORY:
           2015-02-07 - Written - Bovy (IAS)
        """
        return self._mn3[0].Rforce(R,z)+self._mn3[1].Rforce(R,z)\
            +self._mn3[2].Rforce(R,z)

    def _zforce(self,R,z,**kwargs):
        """
        NAME:
           _zforce
        PURPOSE:
           evaluate the vertical force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
        OUTPUT:
           the vertical force
        HISTORY:
           2015-02-07 - Written - Bovy (IAS)
        """
        return self._mn3[0].zforce(R,z)+self._mn3[1].zforce(R,z)\
            +self._mn3[2].zforce(R,z)

    def _dens(self,R,z,**kwargs):
        """
        NAME:
           _dens
        PURPOSE:
           evaluate the density for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
        OUTPUT:
           the density
        HISTORY:
           2015-02-07 - Written - Bovy (IAS)
        """
        return self._mn3[0].dens(R,z)+self._mn3[1].dens(R,z)\
            +self._mn3[2].dens(R,z)

    def _R2deriv(self,R,z,**kwargs):
        """
        NAME:
           _R2deriv
        PURPOSE:
           evaluate the second radial derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
        OUTPUT:
           the second radial derivative
        HISTORY:
           2015-02-07 - Written - Bovy (IAS)
        """
        return self._mn3[0].R2deriv(R,z)+self._mn3[1].R2deriv(R,z)\
            +self._mn3[2].R2deriv(R,z)

    def _z2deriv(self,R,z,**kwargs):
        """
        NAME:
           _z2deriv
        PURPOSE:
           evaluate the second vertical derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
        OUTPUT:
           the second vertical derivative
        HISTORY:
           2015-02-07 - Written - Bovy (IAS)
        """
        return self._mn3[0].z2deriv(R,z)+self._mn3[1].z2deriv(R,z)\
            +self._mn3[2].z2deriv(R,z)

    def _Rzderiv(self,R,z,**kwargs):
        """
        NAME:
           _Rzderiv
        PURPOSE:
           evaluate the mixed R,z derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
        OUTPUT:
           d2phi/dR/dz
        HISTORY:
           2015-02-07 - Written - Bovy (IAS)
        """
        return self._mn3[0].Rzderiv(R,z)+self._mn3[1].Rzderiv(R,z)\
            +self._mn3[2].Rzderiv(R,z)

    @kms_to_kpcGyrDecorator
    def _nemo_accpars(self,vo,ro):
        """
        NAME:

           _nemo_accpars

        PURPOSE:

           return the accpars potential parameters for use of this potential with NEMO

        INPUT:

           vo - velocity unit in km/s

           ro - length unit in kpc

        OUTPUT:

           accpars string

        HISTORY:

           2015-02-09 - Written - Bovy (IAS)

        """
        out= ""
        # Loop through the self._mn3 MN potentials
        for ii in range(3):
            if ii > 0: out+= '#'
            ampl= self._amp*self._mn3[ii]._amp*vo**2.*ro
            out+= "0,%s,%s,%s" % (ampl,self._mn3[ii]._a*ro,self._mn3[ii]._b*ro)
        return out

# Equations from Table 1
def _mass1_tab1(brd):
    return -0.0090*brd**4.+0.0640*brd**3.-0.1653*brd**2.+0.1164*brd+1.9487
def _mass2_tab1(brd):
    return 0.0173*brd**4.-0.0903*brd**3.+0.0877*brd**2.+0.2029*brd-1.3077
def _mass3_tab1(brd):
    return -0.0051*brd**4.+0.0287*brd**3.-0.0361*brd**2.-0.0544*brd+0.2242
def _a1_tab1(brd):
    return -0.0358*brd**4.+0.2610*brd**3.-0.6987*brd**2.-0.1193*brd+2.0074
def _a2_tab1(brd):
    return -0.0830*brd**4.+0.4992*brd**3.-0.7967*brd**2.-1.2966*brd+4.4441
def _a3_tab1(brd):
    return -0.0247*brd**4.+0.1718*brd**3.-0.4124*brd**2.-0.5944*brd+0.7333
# Equations from Table 2
def _mass1_tab2(brd):
    return 0.0036*brd**4.-0.0330*brd**3.+0.1117*brd**2.-0.1335*brd+0.1749
def _mass2_tab2(brd):
    return -0.0131*brd**4.+0.1090*brd**3.-0.3035*brd**2.+0.2921*brd-5.7976
def _mass3_tab2(brd):
    return -0.0048*brd**4.+0.0454*brd**3.-0.1425*brd**2.+0.1012*brd+6.7120
def _a1_tab2(brd):
    return -0.0158*brd**4.+0.0993*brd**3.-0.2070*brd**2.-0.7089*brd+0.6445
def _a2_tab2(brd):
    return -0.0319*brd**4.+0.1514*brd**3.-0.1279*brd**2.-0.9325*brd+2.6836
def _a3_tab2(brd):
    return -0.0326*brd**4.+0.1816*brd**3.-0.2943*brd**2.-0.6329*brd+2.3193
# Equations to go from hz to b
def _b_exphz(hz):
    return -0.269*hz**3.+1.080*hz**2.+1.092*hz
def _b_sechhz(hz):
    return -0.033*hz**3.+0.262*hz**2.+0.659*hz
