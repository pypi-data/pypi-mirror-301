
import numpy as np
from scipy.optimize import fsolve



# This function will calculate and plot P-wave velocity and effective bulk modulus for a given porosity.



# Voight-Ruess-Hill mixing model


def VRH_model(f=[0.35, 0.25, 0.2, 0.125, 0.075],
              K=[55.4, 36.6, 75.6, 46.7, 50.4],
              G=[28.1, 45, 25.6, 23.65, 27.4],
              rho=[2560, 2650, 2630, 2540, 3050]):
    """
    Implements the Voigt-Reuss-Hill (VRH) mixing model to estimate the effective bulk modulus (Km),
    shear modulus (Gm), and density (rho_b) of a composite material made from various minerals.

    Parameters:
    f (list): Fraction of each mineral in the composite (must sum to 1).
    K (list): Bulk modulus of each mineral (GPa).
    G (list): Shear modulus of each mineral (GPa).
    rho (list): Density of each mineral (kg/m^3).

    Returns:
    Km (float): Effective bulk modulus of the composite material (GPa).
    Gm (float): Effective shear modulus of the composite material (GPa).
    rho_b (float): Effective density of the composite material (kg/m^3).
    """
    # Convert input lists to numpy arrays for vectorized operations
    f = np.array(f)
    K = np.array(K)
    G = np.array(G)
    rho = np.array(rho)

    # Calculate effective bulk modulus (Km) using the VRH model
    # Voigt average for bulk modulus is the weighted sum of the moduli
    # Reuss average for bulk modulus is the harmonic mean of the moduli
    # VRH average is the arithmetic mean of Voigt and Reuss averages
    Km = 1 / 2 * (np.sum(f * K) + (np.sum(f / K)) ** (-1))

    # Calculate effective shear modulus (Gm) using the VRH model
    # Similar to bulk modulus but for shear moduli
    Gm = 1 / 2 * (np.sum(f * G) + (np.sum(f / G)) ** (-1))

    # Calculate effective density (rho_b) as the weighted sum of the densities
    rho_b = np.sum(f * rho)

    return Km, Gm, rho_b


def satK(Keff, Km, phi, Sat):
    """
    Calculate the saturated bulk modulus (K_sat) based on Brie's equation.

    Parameters:
    Keff (float): Effective bulk modulus of the dry rock (GPa).
    Km (float): Bulk modulus of the matrix (GPa).
    phi (float): Porosity of the rock.
    Sat (float): Saturation level of the fluid in the pores.

    Returns:
    float: Saturated bulk modulus (GPa).
    """
    Kw = 2  # Bulk modulus of water (GPa)
    Ka = 0.01  # Bulk modulus of air (GPa)
    Kfl = (Kw - Ka) * Sat ** 3 + Ka  # Effective fluid bulk modulus
    K_sat = (Keff / (Km - Keff) + Kfl / (phi * (Km - Kfl))) * Km / (1 + (Keff / (Km - Keff) + Kfl / (phi * (Km - Kfl))))
    return K_sat


## Differential effective medium model
def velDEM(phi, Km, Gm, rho_b, Sat, alpha):
    """
    Calculate effective bulk modulus (Keff), shear modulus (Geff), and P-wave velocity (Vp)
    for a rock with varying porosity (phi) based on the DEM model, taking into account
    the saturation (Sat) and the crack aspect ratio (alpha).

    Parameters:
    phi (np.array): Array of porosities.
    Km (float): Initial bulk modulus of the material (GPa).
    Gm (float): Initial shear modulus of the material (GPa).
    rho_b (float): Density of the solid phase (kg/m^3).
    Sat (float): Saturation level of the fluid in the cracks (0 to 1, where 1 is fully saturated).
    alpha (float): Crack aspect ratio.

    Returns:
    Keff1 (np.array): Effective bulk modulus for each porosity value (GPa).
    Geff1 (np.array): Effective shear modulus for each porosity value (GPa).
    Vp (np.array): P-wave velocity for each porosity value (m/s).
    """

    # Initialize arrays for the calculated values
    Keff1 = np.zeros(len(phi))
    Geff1 = np.zeros(len(phi))
    Vp = np.zeros(len(phi))

    # Constants for fluid moduli
    Kw = 2  # Bulk modulus of water (GPa)
    Ka = 0.01  # Bulk modulus of air (GPa)
    Kf = (Kw - Ka) * Sat ** 3 + Ka  # Effective fluid bulk modulus based on saturation Brie’s equation [Brie et al., 1995]

    for ii in range(len(phi)):
        # Calculate Poisson's ratio for the rock
        v = (3 * Km - 2 * Gm) / (2 * (3 * Km + Gm))

        # Parameters b, c, and d for equations
        b = 3 * np.pi * alpha * (1 - 2 * v) / (4 * (1 - v ** 2))
        c = 1 / (5 * (3 + 8 * (1 - v) / (np.pi * alpha * (2 - v))))
        d = 1 / (5 * (1 + 8 * (1 - v) * (5 - v) / (3 * np.pi * alpha * (2 - v))))

        # Solve for effective bulk modulus
        def equation_Keff(Keff):
            return (Keff - Kf) - (Km - Kf) * (1 - phi[ii]) ** (1 / b)
        Keff1[ii] = fsolve(equation_Keff, Km)[0]

        # Solve for effective shear modulus
        def equation_Geff(Geff):
            return Geff - Gm * (1 - phi[ii]) ** (1 / d)
        Geff1[ii] = fsolve(equation_Geff, Gm)[0]

        # Total density calculation considering porosity and saturation
        rho_a = 1.225  # Density of air (kg/m^3)
        rho_w = 1000  # Density of water (kg/m^3)
        rhototal = rho_b * (1 - phi[ii]) + (Sat * rho_w + (1 - Sat) * rho_a) * phi[ii]

        # P-wave velocity calculation
        Vp[ii] = np.sqrt((Keff1[ii] + 4 / 3 * Geff1[ii]) / rhototal) * 1000  # in m/s

    return Keff1, Geff1, Vp



def vel_porous(phi, Km, Gm, rho_b, Sat,depth = 1):
    """
    Calculate P-wave velocity (Vp) for a rock with varying porosity (phi) based on the Hertz-Mindlin model and Hashin-Shtrikman bounds, taking into account the saturation (Sat).

    Parameters:
    phi (np.array): Array of porosities.
    Km (float): Bulk modulus of the solid phase (GPa).
    Gm (float): Shear modulus of the solid phase (GPa).
    rho_b (float): Density of the solid phase (kg/m^3).
    Sat (float): Saturation level of the fluid in the pores (0 to 1, where 1 is fully saturated).
    depth (float): depth for pressure estimation (m)

    Returns:
    Vp_h (np.array): P-wave velocity for each porosity value (upper Hashin-Shtrikman bound) (m/s).
    Vp_l (np.array): P-wave velocity for each porosity value (lower Hashin-Shtrikman bound) (m/s).
    """

    # Hertz-Mindlin model in critical porosity

    C = 4  # The number of contacts
    phi_c = 0.4  # The critical porosity
    v = (3 * Km - 2 * Gm) / (2 * (3 * Km + Gm))  # Poisson's ratio
    P = (rho_b - 1000) * 9.8 * depth / (1e9)
    K_HM = (C ** 2 * (1 - phi_c) ** 2 * Gm ** 2 / (18 * np.pi ** 2 * (1 - v) ** 2) * P) ** (1 / 3)
    G_HM = (5 - 4 * v) / (10 - 2 * v) * ((3 * C ** 2 * (1 - phi_c) ** 2 * Gm ** 2) * P / (2 * np.pi ** 2 * (1 - v) ** 2)) ** (1 / 3)

    Vp_h = []
    Vp_l = []

    for ii in range(len(phi)):
        if phi[ii] < phi_c:
            Keff_L = (phi[ii] / phi_c / (K_HM + 4 / 3 * G_HM) + (1 - phi[ii] / phi_c) / (Km + 4 / 3 * G_HM)) ** (-1) - 4 / 3 * G_HM
            onede = G_HM / 6 * (9 * K_HM + 8 * G_HM) / (K_HM + 2 * G_HM)
            Geff_L = (phi[ii] / phi_c / (G_HM + onede) + (1 - phi[ii] / phi_c) / (Gm + onede)) ** (-1) - onede

            Keff_H = (phi[ii] / phi_c / (K_HM + 4 / 3 * Gm) + (1 - phi[ii] / phi_c) / (Km + 4 / 3 * Gm)) ** (-1) - 4 / 3 * Gm
            onede = Gm / 6 * (9 * Km + 8 * Gm) / (Km + 2 * Gm)
            Geff_H = (phi[ii] / phi_c / (G_HM + onede) + (1 - phi[ii] / phi_c) / (Gm + onede)) ** (-1) - onede

            Sh = satK(Keff_H, Km, phi[ii], Sat)
            Sl = satK(Keff_L, Km, phi[ii], Sat)
        else:
            Keff = ((1 - phi[ii]) / (1 - phi_c) / (K_HM + 4 / 3 * G_HM) + (phi[ii] - phi_c) / (1 - phi_c) / (4 / 3 * G_HM)) ** (-1) - 4 / 3 * G_HM
            onede = G_HM / 6 * (9 * K_HM + 8 * G_HM) / (K_HM + 2 * G_HM)
            Geff = ((1 - phi[ii]) / (1 - phi_c) / (G_HM + onede) + (phi[ii] - phi_c) / (1 - phi_c) / (onede)) ** (-1) - onede

            Sh = satK(Keff, Km, phi[ii], Sat)
            Sl = satK(Keff, Km, phi[ii], Sat)
            Geff_L = Geff
            Geff_H = Geff

        rho_a = 1.225
        rho_w = 1000
        rhototal = rho_b * (1 - phi[ii]) + (Sat * rho_w + (1 - Sat) * rho_a) * phi[ii]
        Vp_h.append(np.sqrt((Sh + 4 / 3 * Geff_H) * 1e9 / rhototal) / 1000)
        Vp_l.append(np.sqrt((Sl + 4 / 3 * Geff_L) * 1e9 / rhototal) / 1000)

    return np.array(Vp_h), np.array(Vp_l)


def calculate_resistivity_archie(fluid_conductivity, m=2, porosity=0.2, S_w=1, n=2):
    """
    Calculate the formation resistivity using a modified Archie's Law,
    with fluid conductivity as an input.

    Args:
        fluid_conductivity (float): Conductivity of the formation fluid (S/m).
        S_w (float): Water saturation of the formation. Default is 1 (100% saturated).
        n (float): Saturation exponent. Reflects the effect of water saturation on resistivity. Default is 2.
        m (float): Cementation exponent. Reflects the effect of porosity on resistivity. Default is 2.
        porosity (float): Porosity of the formation. Default is 0.2.

    Returns:
        float: The calculated resistivity of the formation (ohm-m).
    """
    # Convert fluid conductivity to resistivity
    R_w = 1 / fluid_conductivity

    # Calculate the Formation Resistivity Factor (F)
    F = porosity ** (-m)

    # Calculate the resistivity of the formation when fully saturated with water
    R_o = F * R_w

    # Calculate the adjusted resistivity for water saturation
    resistivity = R_o / S_w ** n

    return resistivity


def waxman_smits_resistivity(S_w=1, rho_s=100, n=2, sigma_sur=0):
    """
    Calculate the formation resistivity using the Waxman-Smits model, accounting for the conductivity due to clay content.

    Args:
        S_w (float): Water saturation of the formation. Default is 1 (100% saturated).
        rho_s (float): Resistivity of the formation fully saturated with water (ohm-m). Default is 100 ohm-m.
        n (float): Saturation exponent. Reflects the effect of water saturation on resistivity. Default is 2.
        sigma_sur (float): Surface conductivity due to clay content (mS/m). Default is 0.

    Returns:
        float: The calculated resistivity of the formation (ohm-m), considering both water and clay conductivity.
    """
    # Calculate the conductivity of the formation when fully saturated with water
    sigma_sat = 1 / rho_s  # Convert resistivity to conductivity

    # Adjust the conductivity for water saturation and surface conductivity due to clay
    sigma = sigma_sat * S_w ** n + sigma_sur * S_w ** (n - 1)

    # Calculate the resistivity from the adjusted conductivity
    resistivity = 1 / sigma

    return resistivity


def estimate_saturation_from_resistivity_Ro(rho, R_o, n=2):
    """
    Estimate water saturation from resistivity using a modified Archie's Law,
    with the resistivity at full saturation as an input.

    Args:
        rho (float): Measured resistivity of the formation (ohm-m).
        R_o (float): Resistivity of the formation fully saturated with water (ohm-m).
        n (float): Saturation exponent. Reflects the effect of water saturation on resistivity. Default is 2.


    Returns:
        float: Estimated water saturation of the formation.
    """
    # Calculate the Formation Resistivity Factor (F) based on porosity and cementation exponent


    # Inverse Archie's Law to estimate water saturation from resistivity
    S_w = ((rho / R_o) ** (1/n))
    return S_w


def estimate_saturation_fsolve_Ro(rho, R_o, sigma_sur, n=2):
    """
    Estimate water saturation from resistivity in the presence of surface conductivity,
    using the fsolve function from SciPy for numerical solving and R_o as an input.

    Args:
        rho (float or array-like): Measured resistivity of the formation (ohm-m).
        R_o (float): Resistivity of the formation fully saturated with water (ohm-m).
        sigma_sur (float or array-like): Surface conductivity due to clay content (mS/m).
        n (float): Saturation exponent. Default is 2.


    Returns:
        array: Estimated water saturation of the formation for each rho and sigma_sur pair.
    """
    # Ensure inputs are arrays for vectorized operations
    rho = np.asarray(rho)
    sigma_sur = np.asarray(sigma_sur)
    S_t = ((rho / R_o) ** (1/n))
    # Define the function to find the root, representing the equation to solve
    def equation_to_solve(S_w, rho, R_o, sigma_sur, n):
        return (R_o * S_w ** (-n)) + (sigma_sur * S_w ** (n - 1)) - 1 / rho

    # Solve for S_w for each rho and sigma_sur
    solution = [fsolve(equation_to_solve, x0=S_t, args=(rho_val, R_o, sigma_sur_val, n))[0] for rho_val, sigma_sur_val in zip(rho, sigma_sur)]

    return np.array(solution)


def estimate_saturation_from_resistivity(rho, fluid_conductivity, n=2, m=2, porosity=0.2):
    """
    Estimate water saturation from resistivity using a modified inverse Archie's formula.

    Args:
        rho (float): Measured resistivity of the formation (ohm-m).
        fluid_conductivity (float): Conductivity of the formation fluid (S/m).
        n (float): Saturation exponent. Default is 2.
        m (float): Cementation exponent. Reflects the effect of porosity on resistivity. Default is 2.
        porosity (float): Porosity of the formation. Default is 0.2.

    Returns:
        float: Estimated water saturation of the formation.
    """
    # Convert fluid conductivity to resistivity
    R_w = 1 / fluid_conductivity

    # Calculate the Formation Resistivity Factor (F)
    F = porosity ** (-m)

    # Calculate resistivity at full saturation
    R_o = F * R_w

    # Inverse Archie's formula to estimate water saturation
    S_w = ((rho / R_o) ** (1/n))
    return S_w

def estimate_saturation_fsolve(rho, fluid_conductivity, sigma_sur, n=2, m=2, porosity=0.2):
    """
    Estimate water saturation from resistivity in the presence of surface conductivity,
    using the fsolve function from SciPy for numerical solving.

    Args:
        rho (float or array-like): Measured resistivity of the formation (ohm-m).
        fluid_conductivity (float): Conductivity of the formation fluid (S/m).
        sigma_sur (float or array-like): Surface conductivity due to clay content (mS/m).
        n (float): Saturation exponent. Default is 2.
        m (float): Cementation exponent. Reflects the effect of porosity on resistivity. Default is 2.
        porosity (float): Porosity of the formation. Default is 0.2.

    Returns:
        array: Estimated water saturation of the formation for each rho and sigma_sur pair.
    """
    # Ensure inputs are arrays for vectorized operations
    rho = np.asarray(rho)
    sigma_sur = np.asarray(sigma_sur)

    # Convert fluid conductivity to resistivity
    R_w = 1 / fluid_conductivity

    # Calculate the Formation Resistivity Factor (F) and R_o
    F = porosity ** (-m)
    R_o = F * R_w

    S_t = ((rho / R_o) ** (1/n))
    # Define the function to find the root, representing the equation to solve
    def equation_to_solve(S_w, rho, R_o, sigma_sur, n):
        return (R_o * S_w ** (-n)) + (sigma_sur * S_w ** (n - 1)) - 1 / rho

    # Solve for S_w for each rho and sigma_sur
    solution = [fsolve(equation_to_solve, x0=S_t, args=(rho_val, R_o, sigma_sur_val, n))[0] for rho_val, sigma_sur_val in zip(rho, sigma_sur)]

    return np.array(solution)
