import numpy as np
from astropy.io import fits
import os, sys
from os.path import dirname, abspath
import argparse
import yaml
import re
from pymgal.readsnapsgl import readsnap
from pymgal.SSP_models import SSP_models
from pymgal.filters import filters
from pymgal import dusts
from pymgal.load_data import load_data
from pymgal.projection import projection
from pymgal import __version__
from pymgal import utils
import numba
from multiprocessing import Pool

# Generate n random projection vectors
def random_projections(n_samples):
    points = []
    for _ in range(n_samples):
        # Generate random point on unit sphere using spherical coordinates
        theta = np.random.uniform(0, 2*np.pi)
        phi = np.random.uniform(0, np.pi)

        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)

        points.append([round(x, 2), round(y, 2), round(z, 2)])
    points = [np.array(element) for element in points]
    return points

def handle_input(config):
    # Handle some invalid inputs that aren't handled elsewhere
    if config["out_val"].lower() not in {"flux", "magnitude", "luminosity", "jy", "fv", "fl"}:
        raise ValueError(f"Invalid out_val: {config['out_val']} Expected 'flux', 'magnitude', 'luminosity', 'jy', 'fv', or 'fl'.") 

    if (config["mag_type"].lower() not in {"ab", "vega", "solar", "ab_app", "vega_app", "solar_app"}) and (config["out_val"]  == "magnitude"):
        raise ValueError(f"Invalid mag_type: {config['mag_type']}. Expected 'AB', 'vega', 'solar', 'AB_app', 'vega_app', or 'solar_app'.")



class MockObservation(object):
    r"""Create a mock observation of your snapshot with PyMGal
    Below, you can modify any of these parameters to change the nature of your projection

    Parameters
    ----------
    coords        : An array [x_c, y_c, z_c, r] representing the x,y,z centre of your simulation region and its radius
                        IMPORTANT: Make sure to modify this to fit the dimensions of your simulation box.
                        All simulations are different, so they may have different box sizes and particle positions.
                        If you're not sure how to get these coordinates, consider looking for catalogue data from your simulations. 
    model         : The simple stellar population model used. Default: "bc03". Full list can be found at pymgal/models.
    imf           : The initial mass function (IMF) assumed by the SSP model. Default: "chab"
                        Can be either "chab", "krou", or  "salp" (ie Chabrier, Kroupa, or Salpeter).
    dustf         : The function used for dust attenuation. Default: None
                        Can be either None, "charlot_fall" or "calzetti" (ie Charlot and Fall (2000)  or Calzetti et al (2000))
                        The user may also specify a custom dust function here by defining it beforehand and passing it to dustf
    filters       : The list of filters used in projections. Default: ["sdss_r"]
                        Can contain multiple filters. Full list can be found in the pymgal/filters directory
    custom_model  : If you select a custom SSP_model object, PyMGal will ignore the "model", and "imf" parameters above and will use the custom one instead. Default: None
                        If None, the model will be loaded based on it's model name and IMF
    out_val       : Do you want the output in luminosity, Lsun, flux, Fv, Fl, Jy, magnitude? Default: flux.
    mag_type      : If the user selected unit="magnitude", keep track of the type of magnitude (AB, vega, solar) in either apparent or absolute. Default: "AB".
                        If out_val != magnitude, this does nothing   
    proj_vecs     : A list of projection vectors. You can specify principal axes (i.e. “x”, “y”, or “z”) or provide custom vectors in Cartesian coordinates [x, y, z]. Default: "z"
    proj_angs     : A list of angles [alpha, beta, gamma] (in degrees) used to rotate around the x, y, and z axes, respectively. Default: None
                        This serves the same purpose as proj_vecs, so you can use either or both.
    proj_rand     :  The number of random projection directions you want for your simulations.
    rest_frame    : If set to True, the results will be in the rest frame. Otherwise, they will be in the observer’s frame.
    AR            : Angular resolution. Type: arcsec. Default: None 
                         If AR is None and npx is auto, we will force the npx to be 512
                         If AR is None, it will automatically recalculated in the code for output.
                         At z=0, no matter AR is set or not, AR is always assume at z = 0.05. 
    npx           : The pixel number of the grid for projection.
                        Type: int. Default: 512
                        A [npx, npx] image will be produced later.
                        It accept 'auto' parameter, which will automatically decide the pixel number to include all particles.
    z_obs         : The redshift of the object at. Default: None.
                        If None, redshift from simulation data will be used.
                        This will be moved to 0.05 if simulation redshift is used and equal to 0.
                        Note this redshift does not change anything of the simulation physical particle positions, only shift the object to this redshift for observing.
    p_thick     : The thickness in projection direction. Default: None.
                        If None, use all data from cutting region. Otherwise set a value in simulation
                        length unit (kpc/h normally), then a slice of data [center-p_thick, center+p_thick]
                        will be used to make the y-map.
    ksmooth        : An integer representing the k in kNN Gaussian smoothing. 1 sigma for the Gaussian is set to the distance to the kth neighbour in 3D space.
                        If k>0, you set the smoothing length of a particle to be the distance between the particle and its kth nearest neighbour.
                        If k=0, pymgal does not perform smoothing.
                        If k<0, throw an error.
    g_soft         : The gravitational softening length in kpc (physical), which is coverted into pixel values and used as the maximum number of pixels used for the gaussian kernel's 1 sigma.
    add_spec       : Do you want to include the spectrum of the particles? Default: False. If true, the spectrum of each particle will be added to the pixels in the observation.
    spec_res       : If add_spec is set to True, you can define the resolution of the output spectrum. Default: None
                     If None, the max resolution of the spectrum will be used. 
    ncpu           : The number of CPUs you want to use to parallelize the task
    noise          : The level of Gaussian noise you want in your output maps in AB mag / arcsec^2. Default: None
                        If given a float/int, the AB magnitude will be converted to the appropriate output unit and added as Gaussian noise
    outmas         : do you want to output stellar mass? Default: False.
                         If True, the stellar mass in each pixel are saved.
    outage         : do you want to out put stellar age (mass weighted)? Default: False.
                       If True, the stellar age in each pixel are saved.
    outmet         : do you want to out put stellar metallicity (mass weighted)? Default: False.
                       If True, the stellar metallicity in each pixel are saved.
    quiet:         : Do you want to silence output regarding progress? Default: True

    """

    def __init__(self, sim_file, coords, params=None):
        # Default parameter values
        defaults = {
            "model": SSP_models('bc03', IMF='chab', has_masses=True),
            "dustf": None,
            "filters": ["sdss_r"],
            "out_val": "flux",
            "mag_type": "AB",
            "proj_vecs": "z",
            "proj_angs": None,
            "proj_rand": 0,
            "rest_frame": True,
            "AR": 1.2,
            "npx": 512,
            "z_obs": 0.1,
            "ksmooth": 100,
            "g_soft": None,
            "add_spec": False,
            "spec_res": None,
            "p_thick": None,
            "ncpu": 16,
            "noise": None,
            "outmas": True,
            "outage": False,
            "outmet": False,
            "quiet": True
        }

        # If params is not provided, use the default values
        if params is None:
            params = {}

        # Merge provided params with default values
        self.params = {**defaults, **params}

        # Assign essential attributes
        self.sim_file = sim_file
        self.coords = coords
        self.snapname = os.path.basename(self.sim_file).replace('.hdf5', '') if ".hdf5" in os.path.basename(self.sim_file) else os.path.basename(self.sim_file)
        self.simd = load_data(self.sim_file, snapshot=True, center=self.coords[:3], radius=self.coords[-1])
        if not self.params["quiet"]:
            print("Snapshot file successfully read:", self.sim_file)
       
        # Initialize magnitudes as None since they have not yet been computed
        self.mag = None
        self.stored_params = None # For tracking changes in parameters


    def params_changed(self):
      
        # Check if any relevant parameters have changed since the last magnitude computation.
        if self.stored_params is None:
            return True
        
        relevant_keys = ["out_val", "mag_type", "filters", "dustf", "rest_frame", "noise"]

        # If observer's frame is chosen, we need to recompute magnitudes with the redshifted SEDs
        if not self.params["rest_frame"]:
            relevant_keys.append("z_obs")

        for key in relevant_keys:
            if self.params[key] != self.stored_params[key]:
                return True
        return False


    def get_mags(self):
        """
        Prepare the data needed for projections, based on the initialized parameters.
        """
        dustf = self.params["dustf"]
        z_obs = self.params["z_obs"]

        # Prepare the SSP model and filters
        self.params["model"].quiet = self.params["quiet"]   # Suppress print statements if the user wishes
        sspmod = self.params["model"] # Initialize
        filters_list = filters(f_name=self.params["filters"])

        # Compute magnitudes
        is_vega = self.params["mag_type"].lower().startswith('vega')
        mag = filters_list.calc_energy(sspmod, self.simd, dust_func=dustf, vega=is_vega, unit=self.params["out_val"], rest_frame=self.params["rest_frame"], noise=self.params["noise"], redshift=z_obs, outspec_res=self.params["spec_res"])

        # Store the precomputed attributes
        self.mag = mag
        self.sspmod = sspmod
        self.spectrum = filters_list.spectrum
        
        self.noise_dict = filters_list.noises
        self.stored_params = self.params.copy()  # Store the current configuration

    def project_worker(self, proj_direc, output_dir, lsmooth=None, spectrum=None):
        if not self.params["quiet"]:
            print("Projecting to:", proj_direc)
        pj = projection(self.mag, self.simd, npx=self.params["npx"], unit=self.params["out_val"], AR=self.params["AR"], redshift=self.params["z_obs"], p_thick=self.params["p_thick"],
                           axis=proj_direc, mag_type=self.params["mag_type"], ksmooth=self.params["ksmooth"], lsmooth=lsmooth, noise=self.noise_dict, spectrum=spectrum, outmas=self.params["outmas"], 
                           outage=self.params["outage"], outmet=self.params["outmet"])
 
        if isinstance(proj_direc, np.ndarray):
            proj_direc = f"({';'.join(map(str, proj_direc))})"
        if isinstance(proj_direc, list):
            proj_direc = f"({'°,'.join(map(str, proj_direc))}°)"

        output_path = os.path.join(output_dir, f"{self.snapname}-{proj_direc}.fits")
        pj.write_fits_image(output_path, overwrite=True)

    def project(self, output_dir):
        """
        Project the simulation data and save the output to the given directory.
        Before projecting, ensure the prep is done.
        """
        # Check if magnitudes need to be recomputed
        if self.mag is None or self.params_changed():
            self.get_mags()
        
        spectrum = self.spectrum if self.params["add_spec"] else None
        if (self.params["ksmooth"] > 0 and self.params["add_spec"]) or (self.params["noise"] is not None and self.params["add_spec"]):
            raise ValueError("Spectrum is not supported for projections with noise or with smoothing. Please change your settings and try again.")
  
        lsmooth=None
        # Optionally compute kNN distances for smoothing
        if self.params["ksmooth"] > 0:
            lsmooth = utils.knn_distance(np.copy(self.simd.S_pos), self.params["ksmooth"])
        else:
            lsmooth = None

        proj_rand = self.params["proj_rand"]
        proj_vecs = self.params["proj_vecs"] if isinstance(self.params["proj_vecs"], list) else [self.params["proj_vecs"]]
        # Get projection vectors and angles
        chosen_proj_vecs = [np.array(v) if isinstance(v, list) else v for v in proj_vecs] if proj_vecs else []
        random_proj_vecs = random_projections(proj_rand)
        
        # Set up projection list
        projections = chosen_proj_vecs + random_proj_vecs
 
        if not projections:
            raise ValueError("Please provide projection vectors or set num_random_proj.")
 
        worker_args = [(proj_direc, output_dir, lsmooth, spectrum) for proj_direc in proj_vecs]

        # Use multiprocessing to parallelize the project_worker calls
        with Pool(self.params["ncpu"]) as pool:
            pool.starmap(self.project_worker, worker_args)
