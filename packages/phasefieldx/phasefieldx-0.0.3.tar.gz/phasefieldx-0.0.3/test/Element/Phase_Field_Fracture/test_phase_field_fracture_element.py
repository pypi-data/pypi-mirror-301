import pytest
import numpy as np
import pyvista as pv
import os
import dolfinx
import mpi4py
import petsc4py

from phasefieldx.Element.Phase_Field_Fracture.Input import Input
from phasefieldx.Element.Phase_Field_Fracture.solver.solver import solve
from phasefieldx.Boundary.boundary_conditions import bc_xy, bc_y, get_ds_bound_from_marker
from phasefieldx.PostProcessing.ReferenceResult import AllResults

r"""
.. _ref_1700:

One Element tension Isotropic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

   #          u /\        /\  
   #            ||        ||      
   #     (0, 1) *----------* (1, 1)
   #            |          | 
   #            |          |
   #            |          |
   #            |          |
   #            |          | 
   #     (0, 0) *----------* (0, 1)
   #            /_\       /_\       
   #     |Y    ////       ///
   #     |                
   #     *---X           


.. _table_properties_label:

.. table:: Properties

   +----+---------+--------+
   |    | VALUE   | UNITS  |
   +====+=========+========+
   | E  | 210     | kN/mm2 |
   +----+---------+--------+
   | nu | 0.3     | [-]    |
   +----+---------+--------+
   | Gc | 0.005   | kN/mm2 |
   +----+---------+--------+
   | l  | 0.1     | mm     |
   +----+---------+--------+

In this example, we study a simple model formed by a single element with four nodes and dimensions of 1x1 mm. The bottom nodes are constrained in both directions, and the top nodes can slide vertically.

The Young's modulus, Poisson's ratio, and the critical energy release rate are given in the table :ref:`Properties <table_properties_label>`. Young's modulus $E$ and Poisson's ratio $\nu$ can be represented with the Lamé parameters as: $\lambda=\frac{E\nu}{(1+\nu)(1-2\nu)}$; $\mu=\frac{E}{2(1+\nu)}$.

In this case, due to the discretization, it is possible to obtain an analytical solution for the isotropic model by solving $\phi$ from the given equations. The term $|\nabla \phi|^2$ vanishes due to the discretization as explained by Molnar \cite{MOLNAR201727} and Miehe \cite{Miehe1} in the appendix.

.. math::
   \phi = \frac{2 \psi_a}{\frac{G_c}{l}+2\psi_a}=\frac{2 H}{\frac{G_c}{l}+2H} 
   
.. math:: 
    \sigma_y = \sigma_{a}(1-\phi)^2 + \sigma_{b}
    
"""

###############################################################################
# Import necessary libraries
# --------------------------
import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
import dolfinx
import mpi4py 
import petsc4py
import os


###############################################################################
# Import from phasefieldx package
# -------------------------------
from phasefieldx.Element.Phase_Field_Fracture.Input import Input
from phasefieldx.Element.Phase_Field_Fracture.solver.solver import solve
from phasefieldx.Boundary.boundary_conditions import bc_xy, bc_y, get_ds_bound_from_marker
from phasefieldx.PostProcessing.ReferenceResult import AllResults


# @pytest.mark.parametrize("dimension", ["1d", "2d", "3d"])
def test_phase_field_simulation():
    """
    Test phase-field simulation for 1D, 2D, and 3D cases and compare results with theoretical values.
    """
    Data = Input(E=210.0,   # young modulus
                nu=0.3,    # poisson
                Gc=0.005,  # critical energy release rate
                l=0.1,     # lenght scale parameter
                degradation="isotropic", # "isotropic" "anisotropic"
                split_energy="no",       # "spectral" "deviatoric"
                degradation_function="quadratic",
                irreversibility="no", # "miehe"
                fatigue=False,
                fatigue_degradation_function="asymptotic",
                fatigue_val=0.05625,
                k=0.0,
                min_stagger_iter=2,
                max_stagger_iter=500,
                stagger_error_tol=1e-8,
                save_solution_xdmf=False,
                save_solution_vtu=True,
                results_folder_name="1700_One_element_isotropic_tension_test")


    ###############################################################################
    # Mesh Definition
    # ---------------
    # We create a 1x1 mm quadrilateral mesh with a single element using Dolfinx.
    msh = dolfinx.mesh.create_rectangle(mpi4py.MPI.COMM_WORLD,
                                        [np.array([0, 0]),
                                        np.array([1, 1])],
                                        [1, 1],
                                        cell_type=dolfinx.mesh.CellType.quadrilateral)

    def bottom(x):
        return np.isclose(x[1], 0)

    def top(x):
        return np.isclose(x[1], 1)

    fdim = msh.topology.dim - 1

    bottom_facet_marker = dolfinx.mesh.locate_entities_boundary(msh, fdim, bottom) 
    top_facet_marker = dolfinx.mesh.locate_entities_boundary(msh, fdim, top)         

    ds_bottom = get_ds_bound_from_marker(top_facet_marker, msh , fdim)
    ds_top = get_ds_bound_from_marker(top_facet_marker, msh , fdim)

    ds_list = np.array([
                    [ds_bottom, "bottom"],
                    [ds_top,    "top"]
                    ])


    ###############################################################################
    # Function Space Definition
    # -------------------------
    # Define function spaces for displacement and phase-field using Lagrange elements.
    V_u = dolfinx.fem.functionspace(msh, ("Lagrange", 1, (msh.geometry.dim, )))
    V_phi = dolfinx.fem.functionspace(msh, ("Lagrange", 1))


    ###############################################################################
    # Boundary Conditions
    # -------------------
    # Apply boundary conditions: bottom nodes fixed in both directions, top nodes can slide vertically.
    bc_bottom = bc_xy(bottom_facet_marker, V_u, fdim)
    bc_top    = bc_xy(top_facet_marker,    V_u, fdim)
    bcs_list_u = [bc_top, bc_bottom]

    def update_boundary_conditions(bcs, time):
        if time <= 50:
            val =   0.0003*time 
        elif time <= 100:
            val =  -0.0003*(time-50) + 0.015
        else:
            val =  0.0003*(time-100)
        bcs[0].g.value[1] = petsc4py.PETSc.ScalarType(val)
        return 0, val, 0

    bcs_list_phi=[]
    T_list_u = None 
    update_loading = None
    f = None


    ###############################################################################
    # Call the Solver
    # ---------------
    # The problem is solved for a final time of 200. The solver will handle the mesh, boundary conditions,
    # and the given parameters to compute the solution.

    dt = 1.0
    final_time = 200.0

    solve(Data,
        msh, 
        final_time,
        V_u,
        V_phi,
        bcs_list_u,
        bcs_list_phi,
        update_boundary_conditions,
        f, 
        T_list_u,
        update_loading, 
        ds_list,
        dt,
        path = None)



    S = AllResults(Data.results_folder_name)
    displacement = S.dof_files["top.dof"]["Uy"]
    psi_t = 0.5*displacement**2 * (Data.lambda_+2*Data.mu)
    phi_t = 2*psi_t/(Data.Gc/Data.l + 2*psi_t)
    sigma_t = displacement*(Data.lambda_+2*Data.mu)*(1-phi_t)**2

    assert np.allclose(S.reaction_files['top.reaction']["Ry"],sigma_t, atol=1e-8), f"Computed reaction force {S.reaction_files['top.reaction']["Ry"]} does not match theoretical reaction {sigma_t}"
    
    # Clean up: Remove generated files
    if os.path.exists(Data.results_folder_name):
        import shutil
        shutil.rmtree(Data.results_folder_name)
        
