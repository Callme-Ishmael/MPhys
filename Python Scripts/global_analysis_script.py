import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyarrow.parquet as pq
import os
import sys
import vector
import math
from functools import reduce
from scipy.integrate import quad
import mplhep as hep
plt.style.use(hep.style.ATLAS)
from numpy.lib.recfunctions import unstructured_to_structured
from scipy.stats import binned_statistic

def concatenate_vector_arrays(*arrays):
  keys = ["px", "py", "pz", "E"]
  return vector.array({key: np.concatenate([getattr(a, key) for a in arrays]) for key in keys })

# class Particle:
#     def __init__(self, pid, momentum_components):
#         self.pid = pid
#         self.mom = vector.obj(E=momentum_components[0], px=momentum_components[1], py=momentum_components[2], pz=momentum_components[3])

#     def __repr__(self):
#         return f"Particle(pid={self.pid}, mom={self.mom})"
		
# vector1 = vector.obj(x=1, y=2, z=3)
# vector2 = vector.obj(x=4, y=5, z=6)
# vector3 = vector.obj(x=7, y=8, z=9)

# vector_array_obj = vector.array([vector1, vector2, vector3])
# print(vector_array_obj)

# class Particles:
# 	def __init__(self, pid, momentum_components):
# 		self.pid = pid
# 		self.mom = vector.array({"E":momentum_components[:,0], "px":momentum_components[:,1], "py":momentum_components[:,2], "pz":momentum_components[:,3]})

# 	def __repr__(self):
# 		return f"Particles(pid={self.pid}, mom={self.mom})"
# 	def filter(self, id):
# 		try:
# 			mask = self.pid == id
# 			E= self.mom["E"][mask]
# 			px = self.mom["px"][mask]
# 			py = self.mom["py"][mask]
# 			pz = self.mom["pz"][mask]
# 			return Particles(self.pid[mask], (np.array([E,px,py,pz]).T)[mask])
# 		except:
# 			print("Error: Particle ID, " + str(id) + ", not found")
# 			print("Returning None")
# 			return None
# 	def filter_not(self, id):
# 		try:
# 			mask = self.pid != id
# 			E= self.mom["E"][mask]
# 			px = self.mom["px"][mask]
# 			py = self.mom["py"][mask]
# 			pz = self.mom["pz"][mask]
# 			return Particles(self.pid[mask], (np.array([E,px,py,pz]).T)[mask])
# 		except:
# 			print("Error: No Particle IDs other than " + str(id) + " were found")
# 			print("Returning None")
# 			return None

						 
		

#probably wrong this needs your attention
def binning(x, weights, bins):
	if len(weights) == 0:
		print("error: weights array is empty. Returning a dummy plot.")
		return np.ones(5), np.ones(5), np.ones(6), np.ones(5), np.ones(5)
	weights= weights / np.sum(weights)
	try:
		count, bin_edges, bin_number=binned_statistic(x=x, values=weights,statistic='sum', bins=bins)
	except:
		print("binning failed")
		if np.isnan(x).any():
			print("nan values in x")
			print("number of nan vals= ",np.shape(np.where(np.isnan(x))))
		if np.isinf(x).any():
			print("inf values in x")
			print("number of inf vals= ",np.shape(np.where(np.isinf(x))))
		return 4*np.ones(5), np.ones(5), np.ones(6), np.ones(5), np.ones(5)
	bin_width= bin_edges[1] - bin_edges[0]
	w2= weights**2
	bin_centres= (bin_edges[:-1] + bin_edges[1:]) / 2
	var= np.empty([0,1])
	for i in range(1,len(bin_edges)):
		var= np.append(var, np.sum(w2[np.argwhere(bin_number == i)]))
	return count / bin_width, bin_centres, bin_edges, weights / bin_width, np.sqrt(var) / bin_width


def intrajet_momenta(df):
	#float_cols = df.select_dtypes(include="float").columns
	#df[float_cols] = df[float_cols].astype("float32")
	# higgs= vector.array({"E": df['HiggsE'],
	# 											"px": df['Higgspx'], 
	# 											"py": df['Higgspy'],
	# 											"pz": df['Higgspz']})
	p1= vector.array({"E": df['P1E'],
												"px": df['P1px'],
												"py": df['P1py'],
												"pz": df['P1pz']})
	p2= vector.array({"E": df['P2E'],
												"px": df['P2px'],
												"py": df['P2py'],
												"pz": df['P2pz']})
	c1= vector.array({"E": df['C1E'],
												"px": df['C1px'],
												"py": df['C1py'],
												"pz": df['C1pz']})
	c2= vector.array({"E": df['C2E'],
												"px": df['C2px'],
												"py": df['C2py'],
												"pz": df['C2pz']})
	c3= vector.array({"E": df['C3E'],
												"px": df['C3px'],
												"py": df['C3py'],
												"pz": df['C3pz']})
	c4= vector.array({"E": df['C4E'],
												"px": df['C4px'],
												"py": df['C4py'],
												"pz": df['C4pz']})
	gc1= vector.array({"E": df['GC1E'],
												"px": df['GC1px'],
												"py": df['GC1py'],
												"pz": df['GC1pz']})
	gc2= vector.array({"E": df['GC2E'],
												"px": df['GC2px'],
												"py": df['GC2py'],
												"pz": df['GC2pz']})
	gc3= vector.array({"E": df['GC3E'],
												"px": df['GC3px'],
												"py": df['GC3py'],
												"pz": df['GC3pz']})
	gc4= vector.array({"E": df['GC4E'],
												"px": df['GC4px'],
												"py": df['GC4py'],
												"pz": df['GC4pz']})
	gc5= vector.array({"E": df['GC5E'],
												"px": df['GC5px'],
												"py": df['GC5py'],
												"pz": df['GC5pz']})
	gc6= vector.array({"E": df['GC6E'],
												"px": df['GC6px'],
												"py": df['GC6py'],
												"pz": df['GC6pz']})
	gc7= vector.array({"E": df['GC7E'],
												"px": df['GC7px'],
												"py": df['GC7py'],
												"pz": df['GC7pz']})
	gc8= vector.array({"E": df['GC8E'],
												"px": df['GC8px'],
												"py": df['GC8py'],
												"pz": df['GC8pz']})

	# higgs= df[['HiggsE', 'Higgspx', 'Higgspy', 'Higgspz']].to_numpy()
	# gc1= df[['GC1E', 'GC1px', 'GC1py', 'GC1pz']].to_numpy()
	# gc2= df[['GC2E', 'GC2px', 'GC2py', 'GC2pz']].to_numpy()
	# gc3= df[['GC3E', 'GC3px', 'GC3py', 'GC3pz']].to_numpy()
	# gc4= df[['GC4E', 'GC4px', 'GC4py', 'GC4pz']].to_numpy()
	# gc5= df[['GC5E', 'GC5px', 'GC5py', 'GC5pz']].to_numpy()
	# gc6= df[['GC6E', 'GC6px', 'GC6py', 'GC6pz']].to_numpy()
	# gc7= df[['GC7E', 'GC7px', 'GC7py', 'GC7pz']].to_numpy()
	# gc8= df[['GC8E', 'GC8px', 'GC8py', 'GC8pz']].to_numpy()

	return p1, p2, c1, c2, c3, c4, gc1, gc2, gc3, gc4, gc5, gc6, gc7, gc8
	#return Particles(higgs_pid, higgs), Particles(pid_1, gc1), Particles(pid_2, gc2), Particles(pid_3, gc3), Particles(pid_4, gc4), Particles(pid_5, gc5), Particles(pid_6, gc6), Particles(pid_7, gc7), Particles(pid_8, gc8)


def interjet_momenta(df):
	c1= vector.array({"E": df['C1E'],
												"px": df['C1px'],
												"py": df['C1py'],
												"pz": df['C1pz']})
	c2= vector.array({"E": df['C2E'],
												"px": df['C2px'],
												"py": df['C2py'],
												"pz": df['C2pz']})
	c3= vector.array({"E": df['C3E'],
												"px": df['C3px'],
												"py": df['C3py'],
												"pz": df['C3pz']})
	c4= vector.array({"E": df['C4E'],
												"px": df['C4px'],
												"py": df['C4py'],
												"pz": df['C4pz']})
	return c1, c2, c3, c4


def pids(df):
	#int_cols = df.select_dtypes(include="int").columns
	#df[int_cols] = df[int_cols].apply(pd.to_numeric, downcast="integer")
	P1_pid= df['P1PID'].to_numpy()
	P2_pid= df['P2PID'].to_numpy()
	C1_pid= df['C1PID'].to_numpy()
	C2_pid= df['C2PID'].to_numpy()
	C3_pid= df['C3PID'].to_numpy()
	C4_pid= df['C4PID'].to_numpy()
	GC1_pid= df['GC1PID'].to_numpy()
	GC2_pid= df['GC2PID'].to_numpy()
	GC3_pid= df['GC3PID'].to_numpy()
	GC4_pid= df['GC4PID'].to_numpy()
	GC5_pid= df['GC5PID'].to_numpy()
	GC6_pid= df['GC6PID'].to_numpy()
	GC7_pid= df['GC7PID'].to_numpy()
	GC8_pid= df['GC8PID'].to_numpy()

	return P1_pid, P2_pid, C1_pid, C2_pid, C3_pid, C4_pid, GC1_pid, GC2_pid, GC3_pid, GC4_pid, GC5_pid, GC6_pid, GC7_pid, GC8_pid


def richardson_interjet(c1, c2, c3, c4, event_weight, boost_bool, z_cut, tag):
	# tag should be used to calculate the theory prediction
	p1= c1 + c2
	p2 = c3 + c4
	higgs= p1 + p2
	#["bb_qgqg", "gg_qqqq", "gg_gggg", "gg_qqgg"]
	def rotate_to_z(v, pseudophi, pseudotheta):
		v_rotated_no_y = v.rotate_axis(angle= -1 * pseudophi, axis=vector.obj(x=0, y=0, z=1))
		v_rotated_no_pt = v_rotated_no_y.rotate_axis(angle= -1 * pseudotheta, axis=vector.obj(x=0, y=1, z=0))
		return v_rotated_no_pt

	if boost_bool == True:
		c1= c1.boostCM_of(higgs)
		c2= c2.boostCM_of(higgs)
		c3= c3.boostCM_of(higgs)
		c4= c4.boostCM_of(higgs)
		p1= p1.boostCM_of(higgs)
		p2= p2.boostCM_of(higgs)

	#mask_cuts= ((np.true_divide(c1["E"], p1["E"]) > z_cut) & (np.true_divide(c1["E"], p1["E"]) < 1-z_cut)) & ((np.true_divide(c3["E"], p2["E"]) > z_cut) & (np.true_divide(c3["E"], p2["E"]) < 1-z_cut))
	valid_mask = ~np.isnan(c1["E"]) & ~np.isnan(p1["E"]) & ~np.isnan(c3["E"]) & ~np.isnan(p2["E"]) & \
                 ~np.isinf(c1["E"]) & ~np.isinf(p1["E"]) & ~np.isinf(c3["E"]) & ~np.isinf(p2["E"])
	mask_cuts = valid_mask & ((np.true_divide(c1["E"], p1["E"]) > z_cut) & (np.true_divide(c1["E"], p1["E"]) < 1 - z_cut)) & \
                ((np.true_divide(c3["E"], p2["E"]) > z_cut) & (np.true_divide(c3["E"], p2["E"]) < 1 - z_cut))
	
	c1= c1[mask_cuts]
	c2= c2[mask_cuts]
	c3= c3[mask_cuts]
	c4= c4[mask_cuts]
	p1= p1[mask_cuts]
	p2= p2[mask_cuts]
	event_weight= event_weight[mask_cuts]

	principal_phi= p1.phi
	c1_rotated= rotate_to_z(c1, p1.phi, p1.theta)
	c2_rotated= rotate_to_z(c2, p2.phi, p2.theta)
	phi_1= c1_rotated.phi
	phi_2= c2_rotated.phi
	phi_1_prime= (2*principal_phi) + np.pi - phi_1
	delta_phi= phi_2 - phi_1_prime
	delta_phi_1= np.where((delta_phi >= -5* np.pi) & (delta_phi <= -3*np.pi), delta_phi + (4*np.pi), delta_phi)
	delta_phi_2= np.where((delta_phi_1 >= -3* np.pi) & (delta_phi_1 <= -1*np.pi), delta_phi_1 + (2*np.pi), delta_phi_1)
	delta_phi_3= np.where((delta_phi_2 <= 5*np.pi) & (delta_phi_2 >= 3*np.pi), delta_phi_2 - (4*np.pi) , delta_phi_2)
	delta_phi_4= np.where((delta_phi_3 >= 1*np.pi) & (delta_phi_3 <= 3*np.pi), delta_phi_3 - (2*np.pi) , delta_phi_3)
	# heights, bin_centres, bin_edges, weights_norm, uncert= binning(delta_phi_4, event_weight, 50)
	# fig, ax= plt.subplots()
	# ax.stairs(values= heights, edges= bin_edges, label="z_cut= "+str(z_cut),color='b')
	# ax.errorbar(x= bin_centres, y=heights, yerr= uncert, fmt='x', capsize=1, elinewidth=1, color='b', markersize=3)
	# ax.set_title("Richardson_interjet " + title)
	# ax.set_xlabel("Delta phi (rad)")
	# ax.set_ylabel("normalised diff cross section")
	# ax.legend()
	# fig.savefig("Richardson_interjet_" + title + ".png")
	return np.array([delta_phi_4, event_weight]).T


def panscales_no_nonsense_interjet(c1, c2, c3, c4, event_weight, boost_bool, z_cut, tag):
	p1= c1 + c2
	p2 = c3 + c4
	higgs= p1 + p2

	def boost_to_frame(v, p):
		v_boosted= v.boostCM_of(p)
		return v_boosted
	if boost_bool == True:
		c1= boost_to_frame(c1, higgs)
		c2= boost_to_frame(c2, higgs)
		c3= boost_to_frame(c3, higgs)
		c4= boost_to_frame(c4, higgs)
		p1= boost_to_frame(p1, higgs)
		p2= boost_to_frame(p2, higgs)

	#mask_cuts= ((c1["E"] / p1["E"] > z_cut) & (c1["E"] / p1["E"] < 1-z_cut)) & ((c3["E"] / p2["E"] > z_cut) & (c3["E"] / p2["E"] < 1-z_cut))
	valid_mask = ~np.isnan(c1["E"]) & ~np.isnan(p1["E"]) & ~np.isnan(c3["E"]) & ~np.isnan(p2["E"]) & \
                 ~np.isinf(c1["E"]) & ~np.isinf(p1["E"]) & ~np.isinf(c3["E"]) & ~np.isinf(p2["E"])


	mask_cuts = valid_mask & ((np.true_divide(c1["E"], p1["E"]) > z_cut) & (np.true_divide(c1["E"], p1["E"]) < 1 - z_cut)) & \
                ((np.true_divide(c3["E"], p2["E"]) > z_cut) & (np.true_divide(c3["E"], p2["E"]) < 1 - z_cut))
	
	
	
	c1= c1[mask_cuts]
	c2= c2[mask_cuts]
	c3= c3[mask_cuts]
	c4= c4[mask_cuts]
	p1= p1[mask_cuts]
	p2= p2[mask_cuts]
	event_weight= event_weight[mask_cuts]

	hard_child_1_mask = c1["E"] >= c2["E"]
	soft_child_1_mask = ~hard_child_1_mask
	hard_child_2_mask = c3["E"] >= c4["E"]
	soft_child_2_mask = ~hard_child_2_mask
	hard_parent_mask = p1["E"] >= p2["E"]
	soft_parent_mask = ~hard_parent_mask

	hard_child_1 = vector.array({"E": np.where(hard_child_1_mask, c1["E"], c2["E"]),
																"px": np.where(hard_child_1_mask, c1["px"], c2["px"]),
																"py": np.where(hard_child_1_mask, c1["py"], c2["py"]),
																"pz": np.where(hard_child_1_mask, c1["pz"], c2["pz"])})
	soft_child_1 = vector.array({"E": np.where(soft_child_1_mask, c1["E"], c2["E"]),
																"px": np.where(soft_child_1_mask, c1["px"], c2["px"]),
																"py": np.where(soft_child_1_mask, c1["py"], c2["py"]),
																"pz": np.where(soft_child_1_mask, c1["pz"], c2["pz"])})
	hard_child_2 = vector.array({"E": np.where(hard_child_2_mask, c3["E"], c4["E"]),
																"px": np.where(hard_child_2_mask, c3["px"], c4["px"]),
																"py": np.where(hard_child_2_mask, c3["py"], c4["py"]),
																"pz": np.where(hard_child_2_mask, c3["pz"], c4["pz"])})
	soft_child_2 = vector.array({"E": np.where(soft_child_2_mask, c3["E"], c4["E"]),
																"px": np.where(soft_child_2_mask, c3["px"], c4["px"]),
																"py": np.where(soft_child_2_mask, c3["py"], c4["py"]),
																"pz": np.where(soft_child_2_mask, c3["pz"], c4["pz"])})
	hard_parent = vector.array({"E": np.where(hard_parent_mask, p1["E"], p2["E"]),
															"px": np.where(hard_parent_mask, p1["px"], p2["px"]),
															"py": np.where(hard_parent_mask, p1["py"], p2["py"]),
															"pz": np.where(hard_parent_mask, p1["pz"], p2["pz"])})
	soft_parent = vector.array({"E": np.where(soft_parent_mask, p1["E"], p2["E"]),
															"px": np.where(soft_parent_mask, p1["px"], p2["px"]),
															"py": np.where(soft_parent_mask, p1["py"], p2["py"]),
															"pz": np.where(soft_parent_mask, p1["pz"], p2["pz"])})

	n0= hard_parent.to_pxpypz().cross(soft_parent.to_pxpypz()).unit()
	n1= hard_child_1.to_pxpypz().cross(soft_child_1.to_pxpypz()).unit()
	n1prime= hard_child_2.to_pxpypz().cross(soft_child_2.to_pxpypz()).unit()
	psi_1= np.arccos(n0.dot(n1))
	psi_1= np.where(n0.cross(n1).dot(hard_child_1.to_pxpypz()) > 0, psi_1, -1 * psi_1)
	psi_2= np.arccos(n0.dot(n1prime))
	psi_2= np.where(n0.cross(n1prime).dot(hard_child_2.to_pxpypz()) > 0, psi_2, -1 * psi_2)
	delta_psi= psi_1 - psi_2
	delta_psi= np.where(delta_psi < -1*np.pi, delta_psi + (2 * np.pi), delta_psi)
	delta_psi= np.where(delta_psi > np.pi, delta_psi - (2 * np.pi), delta_psi)
	# heights, bin_centres, bin_edges, weights_norm, uncert= binning(delta_psi, event_weight, 50)
	# fig, ax= plt.subplots()
	# ax.stairs(values= heights, edges= bin_edges, label="z_cut= "+str(z_cut),color='b')
	# ax.errorbar(x= bin_centres, y=heights, yerr= uncert, fmt='x', capsize=1, elinewidth=1, color='b', markersize=3)
	# ax.set_title("panscales no-nonsense interjet " + title)
	# ax.set_xlabel("Delta psi (rad)")
	# ax.set_ylabel("normalised diff cross section")
	# ax.legend()
	# fig.savefig("panscales_no-nonsense_interjet_" + title + ".png")
	return np.array([delta_psi, event_weight]).T


def richardson_intrajet(parent, parent_spectator, spectator, intermediate, gc1, gc2, event_weight, boost_bool, zcut_1, zcut_2, tag):
	# tag to be used to calculate the theory prediction
	higgs= parent + parent_spectator #parent_spectator is not useful anywhere but for the higgs calculation. It is not used in the rest of the function
	def rotate_to_z(v, pseudophi, pseudotheta):
		v_rotated_no_y = v.rotate_axis(angle= -1 * pseudophi, axis=vector.obj(x=0, y=0, z=1))
		v_rotated_no_pt = v_rotated_no_y.rotate_axis(angle= -1 * pseudotheta, axis=vector.obj(x=0, y=1, z=0))
		return v_rotated_no_pt

	if boost_bool == True:
		parent= parent.boostCM_of(higgs)
		parent_spectator= parent_spectator.boostCM_of(higgs)
		spectator= spectator.boostCM_of(higgs)
		intermediate= intermediate.boostCM_of(higgs)
		gc1= gc1.boostCM_of(higgs)
		gc2= gc2.boostCM_of(higgs)
	
	mask_cuts_1= np.true_divide(intermediate["E"], parent["E"]) <= zcut_1 #soft intermediate
	mask_cuts_2=(np.true_divide(gc1["E"], intermediate["E"]) > zcut_2) & (np.true_divide(gc1["E"], intermediate["E"]) <= 1 - zcut_2) #fair second splitting
	parent= parent[mask_cuts_1 & mask_cuts_2]
	parent_spectator= parent_spectator[mask_cuts_1 & mask_cuts_2]
	spectator= spectator[mask_cuts_1 & mask_cuts_2]
	intermediate= intermediate[mask_cuts_1 & mask_cuts_2]
	gc1= gc1[mask_cuts_1 & mask_cuts_2]
	gc2= gc2[mask_cuts_1 & mask_cuts_2]
	event_weight= event_weight[mask_cuts_1 & mask_cuts_2]

	phi_1= rotate_to_z(spectator, parent.phi, parent.theta).phi
	phi_2= rotate_to_z(gc1, parent.phi, parent.theta).phi

	delta_phi= phi_1 - phi_2
	delta_phi_1= np.where((delta_phi >= -5* np.pi) & (delta_phi <= -3*np.pi), delta_phi + (4*np.pi), delta_phi)
	delta_phi_2= np.where((delta_phi_1 >= -3* np.pi) & (delta_phi_1 <= -1*np.pi), delta_phi_1 + (2*np.pi), delta_phi_1)
	delta_phi_3= np.where((delta_phi_2 <= 5*np.pi) & (delta_phi_2 >= 3*np.pi), delta_phi_2 - (4*np.pi) , delta_phi_2)
	delta_phi_4= np.where((delta_phi_3 >= 1*np.pi) & (delta_phi_3 <= 3*np.pi), delta_phi_3 - (2*np.pi) , delta_phi_3)

	return np.array([delta_phi_4, event_weight]).T


def panscales_no_nonsense_intrajet(parent, parent_spectator, spectator, intermediate, gc1, gc2, event_weight, boost_bool, zcut_1, zcut_2, tag):
	#tag to be used to calculate the theory prediction
	higgs= parent + parent_spectator

	if boost_bool == True:
		parent= parent.boostCM_of(higgs)
		parent_spectator= parent_spectator.boostCM_of(higgs)
		spectator= spectator.boostCM_of(higgs)
		intermediate= intermediate.boostCM_of(higgs)
		gc1= gc1.boostCM_of(higgs)
		gc2= gc2.boostCM_of(higgs)
	
	mask_cuts_1= np.true_divide(intermediate["E"], parent["E"]) <= zcut_1 #soft intermediate
	mask_cuts_2=(np.true_divide(gc1["E"], intermediate["E"]) >= zcut_2) & (np.true_divide(gc1["E"], intermediate["E"]) <= 1 - zcut_2) #fair second splitting
	parent= parent[mask_cuts_1 & mask_cuts_2]
	parent_spectator= parent_spectator[mask_cuts_1 & mask_cuts_2]
	spectator= spectator[mask_cuts_1 & mask_cuts_2]
	intermediate= intermediate[mask_cuts_1 & mask_cuts_2]
	gc1= gc1[mask_cuts_1 & mask_cuts_2]
	gc2= gc2[mask_cuts_1 & mask_cuts_2]
	event_weight= event_weight[mask_cuts_1 & mask_cuts_2]

	hard_parent= np.where(parent["E"] >= parent_spectator["E"], parent, parent_spectator).view(vector.MomentumNumpy4D)
	soft_parent= np.where(parent["E"] < parent_spectator["E"], parent, parent_spectator).view(vector.MomentumNumpy4D)
	hard_child= np.where(intermediate["E"] >= spectator["E"], intermediate, spectator).view(vector.MomentumNumpy4D)
	soft_child= np.where(intermediate["E"] < spectator["E"], intermediate, spectator).view(vector.MomentumNumpy4D)
	hard_gc= np.where(gc1["E"] >= gc2["E"], gc1, gc2).view(vector.MomentumNumpy4D)
	soft_gc= np.where(gc1["E"] < gc2["E"], gc1, gc2).view(vector.MomentumNumpy4D)

	n0= hard_parent.to_pxpypz().cross(soft_parent.to_pxpypz()).unit()
	n1= hard_child.to_pxpypz().cross(soft_child.to_pxpypz()).unit()
	n2= hard_gc.to_pxpypz().cross(soft_gc.to_pxpypz()).unit()
	delta_01= np.where(n0.cross(n1).dot(hard_child.to_pxpypz()) > 0, np.arccos(n0.dot(n1)), -1 * np.arccos(n0.dot(n1))) #not used but can be useful
	delta_12= np.where(n1.cross(n2).dot(hard_gc.to_pxpypz()) > 0, np.arccos(n1.dot(n2)), -1 * np.arccos(n1.dot(n2)))

	delta_12= np.where(delta_12 < -1*np.pi, delta_12 + (2 * np.pi), delta_12)
	delta_12= np.where(delta_12 > np.pi, delta_12 - (2 * np.pi), delta_12)
	return np.array([delta_12, event_weight]).T


	

# filtering functions according to channel
# generic filters

# gg pair
def filter_gg(pid_1,pid_2):
	mask= (pid_1 == 21) & (pid_2 == 21)
	return np.argwhere(mask).flatten()

# bb pair
def filter_bb(pid_1,pid_2):
	mask= (np.abs(pid_1) == 5) & (np.abs(pid_2) == 5)
	return np.argwhere(mask).flatten()

# qq pair
def filter_qq(pid_1,pid_2):
	mask= (np.abs(pid_1) < 6) & (np.abs(pid_2) < 6) & (pid_1 != 0) & (pid_2 != 0)
	return np.argwhere(mask).flatten()

# qg pair
def filter_qg(pid_1,pid_2):
	mask= ((np.abs(pid_1) < 6) & (np.abs(pid_1) != 0) & (pid_2 == 21)) | ((np.abs(pid_2) < 6) & (np.abs(pid_2) != 0) & (pid_1 == 21))
	return np.argwhere(mask).flatten()

# q particles
def filter_q(pid):
	mask= (np.abs(pid) < 6) & (np.abs(pid) != 0)
	return np.argwhere(mask).flatten()

# g particles
def filter_g(pid):
	mask= (pid == 21)
	return np.argwhere(mask).flatten()

# ---------------------------------------------
# interjet channels
# H-> gg, g->qq, g->qq
def filter_inter_gg_qqqq(pids):
	qq_1= filter_qq(pids[2], pids[3])
	qq_2= filter_qq(pids[4], pids[5])
	return np.intersect1d(qq_1, qq_2)

def filter_inter_gg_gggg(pids):
	gg_1= filter_gg(pids[2], pids[3])
	gg_2= filter_gg(pids[4], pids[5])
	return np.intersect1d(gg_1, gg_2)

# H-> gg, g->qq, g->gg
def filter_inter_gg_qqgg(pids):  # does not need further processing
	qq_1= filter_qq(pids[2], pids[3])
	gg_2= filter_gg(pids[4], pids[5])

	gg_1= filter_gg(pids[2], pids[3])
	qq_2= filter_qq(pids[4], pids[5])
	return np.append(np.intersect1d(qq_1, gg_2), np.intersect1d(gg_1, qq_2))

# H->bb, b->qg, b->qg
def filter_inter_bb_qgqg(pids):
	qg_1= filter_qg(pids[2], pids[3])
	qg_2= filter_qg(pids[4], pids[5])
	return np.intersect1d(qg_1, qg_2)


# ---------------------------------------------
# Intrajet channels
# all analyses have to check both sides of the higgs branching
# b -> bg, g -> qq
def filter_intra_bg_qq_1(pids): # checks first higgs branch  #interesting: 2367 (category=0) 2 is the gluon , 2389 (category=1) 3 is the gluon
	h_bb= filter_bb(pids[0], pids[1])
	bg= filter_qg(pids[2], pids[3])
	qq= np.append(filter_qq(pids[6], pids[7]), filter_qq(pids[8], pids[9])) #takes care of g being on 2 or 3 but need further processing
	args= reduce(np.intersect1d, (h_bb, bg, qq))
	category= np.where(pids[2][args] == 21, 0, 1)
	return args, category

def filter_intra_bg_qq_2(pids): # checks second higgs branch    #interesting: 4 5 10 11  (category=0) 4 is the gluon,  4 5 12 13 (category=1) 5 is the gluon
	h_bb= filter_bb(pids[0], pids[1])
	bg= filter_qg(pids[4], pids[5])
	qq= np.append(filter_qq(pids[10], pids[11]), filter_qq(pids[12], pids[13])) #takes care of g being on 4 or 5 but need further processing
	args= reduce(np.intersect1d, (h_bb, bg, qq))
	category= np.where(pids[4][args] == 21, 0, 1)
	return args, category

# b -> bg, g -> gg
def filter_intra_bg_gg_1(pids): # checks first higgs branch     #interesting: 2367 (category=0) 2 is the gluon , 2389 (category=1) 3 is the gluon
	h_bb= filter_bb(pids[0], pids[1])
	bg= filter_qg(pids[2], pids[3])
	gg= np.append(filter_gg(pids[6], pids[7]), filter_gg(pids[8], pids[9])) #takes care of g being on 2 or 3 but need further processing
	args= reduce(np.intersect1d, (h_bb, bg, gg))
	category= np.where(pids[2][args] == 21, 0, 1)
	return args, category

def filter_intra_bg_gg_2(pids): # checks second higgs branch    #interesting: 4 5 10 11  (category=0) 4 is the gluon,  4 5 12 13 (category=1) 5 is the gluon
	h_bb= filter_bb(pids[0], pids[1])
	bg= filter_qg(pids[4], pids[5])
	gg= np.append(filter_gg(pids[10], pids[11]), filter_gg(pids[12], pids[13]))
	args= reduce(np.intersect1d, (h_bb, bg, gg))
	category= np.where(pids[4][args] == 21, 0, 1)
	return args, category



#g -> gg, g -> qq (2 perms, check both branches)   #interesting: 2367,2389
# THE CASE WHERE BOTH GLUONS DECAY TO QUARKS AND THEN THE SAME EVENT IS PASSED ON TO BE ANALYSED TWICE, IS NOT TAKEN INTO ACCOUNT, SWALLOW IT :)))))))) 
def filter_intra_gg_qq_1(pids): # checks first higgs branch
	h_gg= filter_gg(pids[0], pids[1])
	gg= filter_gg(pids[2], pids[3]) #takes care of g being on 6 or 7 but need further processing
	qq= np.append(filter_qq(pids[6], pids[7]), filter_qq(pids[8], pids[9])) #takes care of decaying g being on 2 or 3 but need further processing
	args= reduce(np.intersect1d, (h_gg, gg, qq))
	category= np.where(pids[6][args] != 21, 0, 1) # 67 are quarks if 0, else 89 are quarks (CASE WHERE 6789 ARE QUARKS IS NOT HANDLED)
	return args, category

def filter_intra_gg_qq_2(pids): # checks second higgs branch    #interesting: 4 5 10 11, 4 5 12 13
	h_gg= filter_gg(pids[0], pids[1])
	gg= filter_gg(pids[4], pids[5]) #takes care of g being on 6 or 7 but need further processing
	qq= np.append(filter_qq(pids[10], pids[11]), filter_qq(pids[12], pids[13])) #takes care of decaying g being on 2 or 3 but need further processing
	args= reduce(np.intersect1d, (h_gg, gg, qq))
	category= np.where(pids[10][args] != 21, 0, 1) # 10 11 are quarks if 0, else 12 13 are quarks (CASE WHERE 10 11 12 13 ARE QUARKS IS NOT HANDLED)
	return args, category


# ---------------------------------------------
# plot/implement
def interjet_obs(pids, all_momenta, event_weight, zcut, tag, richardson_obs_boosted_dict, richardson_obs_not_boosted_dict, panscales_no_nonsense_obs_boosted_dict, panscales_no_nonsense_obs_not_boosted_dict):
	funcs= [filter_inter_gg_qqqq, filter_inter_gg_gggg, filter_inter_gg_qqgg, filter_inter_bb_qgqg] #interjet functions # ORDER PROBABLY DOESN'T MATTERS
	for func in funcs:
		tag= (func.__name__).split("_")[2] + "_" + (func.__name__).split("_")[3]
		args= func(pids)
		c1= all_momenta[0][args]
		c2= all_momenta[1][args]
		c3= all_momenta[2][args]
		c4= all_momenta[3][args]
		weights= event_weight[args]
		richardson_obs_not_boosted= richardson_interjet(c1, c2, c3, c4, weights, False, zcut, tag) # tags have to be unique ()  #no boost
		richardson_obs_boosted= richardson_interjet(c1, c2, c3, c4, weights, True, zcut,tag) # higgs boost
		richardson_obs_boosted_dict[tag]= np.vstack((richardson_obs_boosted_dict[tag], richardson_obs_boosted))
		richardson_obs_not_boosted_dict[tag]= np.vstack((richardson_obs_not_boosted_dict[tag], richardson_obs_not_boosted))
		#########
		panscales_no_nonsense_obs_not_boosted= panscales_no_nonsense_interjet(c1, c2, c3, c4, weights, False, zcut, tag) #no boost
		panscales_no_nonsense_obs_boosted= panscales_no_nonsense_interjet(c1, c2, c3, c4, weights, True, zcut, tag) #higgs boost
		panscales_no_nonsense_obs_boosted_dict[tag]= np.vstack((panscales_no_nonsense_obs_boosted_dict[tag], panscales_no_nonsense_obs_boosted))
		panscales_no_nonsense_obs_not_boosted_dict[tag]= np.vstack((panscales_no_nonsense_obs_not_boosted_dict[tag], panscales_no_nonsense_obs_not_boosted))
		#########
		#implement panscales lund planes later on
	return richardson_obs_boosted_dict, richardson_obs_not_boosted_dict, panscales_no_nonsense_obs_boosted_dict, panscales_no_nonsense_obs_not_boosted_dict
		
def plot_interjet(obs_dict, z_cut, boost_bool, paper, outdir):
	for key in obs_dict.keys():
		title= key
		if paper== "panscales_no_nonsense":
			title= "panscales_no_nonsense_" + title
		elif paper== "richardson":
			title= "richardson_" + title
		elif paper== "panscales_lund":
			title= "panscales_lund_" + title
		if boost_bool == True:
			title= title + "_boosted"
		else:
			title= title + "_no boost"
		if (paper == "panscales_no_nonsense") or (paper == "panscales_lund"):
			xlabel= "Delta psi (rad)"
		elif paper== "richardson":
			xlabel= "Delta phi (rad)"
		
		heights, bin_centres, bin_edges, weights_norm, uncert= binning(obs_dict[key][:,0], obs_dict[key][:,1], 50)
		fig, ax= plt.subplots()
		ax.stairs(values= heights, edges= bin_edges, label="z_cut= "+str(z_cut),color='b')
		ax.errorbar(x= bin_centres, y=heights, yerr= uncert, fmt='x', capsize=1, elinewidth=1, color='b', markersize=3)
		ax.set_title(title)
		ax.set_xlabel(xlabel)
		ax.set_ylabel("normalised diff cross section")
		ax.legend()
		fig.savefig(outdir+title + "_interjet" +".png")
		plt.close()

	return None


def intrajet_obs(pids, all_momenta, event_weight, zcut_1, zcut_2, richardson_obs_boosted_dict, richardson_obs_not_boosted_dict, panscales_no_nonsense_obs_boosted_dict, panscales_no_nonsense_obs_not_boosted_dict):
	funcs= [filter_intra_bg_qq_1, filter_intra_bg_qq_2, filter_intra_bg_gg_1, filter_intra_bg_gg_2, filter_intra_gg_qq_1, filter_intra_gg_qq_2] #intrajet functions # ORDER PROBABLY DOESN'T MATTER
	
	for func in funcs:
		args, category= func(pids)
		weights= event_weight[args]
		tag= (func.__name__).split("_")[2] + "_" + (func.__name__).split("_")[3]
		branch= int((func.__name__).split("_")[-1])
		if branch == 1:
			parent= all_momenta[0][args]
			parent_spectator= all_momenta[1][args]
			spectator= np.where(category == 0 , all_momenta[3][args], all_momenta[2][args]).view(vector.MomentumNumpy4D)
			intermediate= np.where(category == 0 , all_momenta[2][args], all_momenta[3][args]).view(vector.MomentumNumpy4D)
			gc1= np.where(category == 0 , all_momenta[6][args], all_momenta[8][args]).view(vector.MomentumNumpy4D)
			gc2= np.where(category == 0 , all_momenta[7][args], all_momenta[9][args]).view(vector.MomentumNumpy4D)
			#spectator with category mask concatenated with spectator with ! category mask(one is gluon the other is quark)
		elif branch == 2:
			parent= all_momenta[1][args]
			parent_spectator= all_momenta[0][args]
			spectator= np.where(category == 0 , all_momenta[5][args], all_momenta[4][args]).view(vector.MomentumNumpy4D)
			intermediate= np.where(category == 0 , all_momenta[4][args], all_momenta[5][args]).view(vector.MomentumNumpy4D)
			gc1= np.where(category == 0 , all_momenta[10][args], all_momenta[12][args]).view(vector.MomentumNumpy4D)
			gc2= np.where(category == 0 , all_momenta[11][args], all_momenta[13][args]).view(vector.MomentumNumpy4D)
		
		richardson_obs_not_boosted= richardson_intrajet(parent, parent_spectator, spectator, intermediate, gc1, gc2, weights, False, zcut_1, zcut_2, tag)
		richardson_obs_boosted= richardson_intrajet(parent, parent_spectator, spectator, intermediate, gc1, gc2, weights, True, zcut_1, zcut_2, tag)
		richardson_obs_not_boosted_dict[tag]= np.vstack((richardson_obs_not_boosted_dict[tag], richardson_obs_not_boosted))
		richardson_obs_boosted_dict[tag]= np.vstack((richardson_obs_boosted_dict[tag], richardson_obs_boosted))

		panscales_no_nonsense_obs_not_boosted= panscales_no_nonsense_intrajet(parent, parent_spectator, spectator, intermediate, gc1, gc2, weights, False, zcut_1, zcut_2, tag)
		panscales_no_nonsense_obs_boosted= panscales_no_nonsense_intrajet(parent, parent_spectator, spectator, intermediate, gc1, gc2, weights, True, zcut_1, zcut_2, tag)
		panscales_no_nonsense_obs_not_boosted_dict[tag]= np.vstack((panscales_no_nonsense_obs_not_boosted_dict[tag], panscales_no_nonsense_obs_not_boosted))
		panscales_no_nonsense_obs_boosted_dict[tag]= np.vstack((panscales_no_nonsense_obs_boosted_dict[tag], panscales_no_nonsense_obs_boosted))


	return richardson_obs_boosted_dict, richardson_obs_not_boosted_dict, panscales_no_nonsense_obs_boosted_dict, panscales_no_nonsense_obs_not_boosted_dict

def plot_intrajet(obs_dict, zcut_1, zcut_2, boost_bool, paper, outdir):	
	
	for key in obs_dict.keys():
		fig, ax= plt.subplots()
		title= key
		if paper == "richardson":
			title= "richardson_" + title
			def A_richardson_func(z_1):
				if key.split("_")[0] == "bg":
					return 2 * z_1 / (1+(z_1**2))
				if key.split("_")[0] == "gg":
					return (z_1/(1-(z_1*(1-z_1))))**2
	
			def B_richardson_func(z_2):
				if key.split("_")[1] == "qq":
					helper= -2*z_2 * (1-z_2)
					return helper/(1+helper)
				if key.split("_")[1] == "gg":
					helper= z_2 * (1-z_2)
					return (helper / (1-helper))**2
			def richardson_theory(A_param, B_param, x):
				return (1/ (2* np.pi))* (1+ (A_param*B_param* np.cos(2*x)))
			def normalise(func, A_param, B_param):
					return quad(lambda x: func(A_param, B_param, x), -1*np.pi, np.pi )[0]

			# A_richardson= quad(A_richardson_func, zcut_1, 1-zcut_1)[0]
			# B_richardson= quad(B_richardson_func, zcut_2, 1-zcut_2)[0]
			# x_theory= np.linspace(-np.pi, np.pi, 1000)
			# theory= richardson_theory(A_richardson, B_richardson, x_theory)
			# theory=  theory / normalise(richardson_theory, A_richardson, B_richardson)
			# ax.plot(x_theory, theory, label="theory", color='r')
		elif paper== "panscales_no_nonsense":
			title= "panscales_no_nonsense_" + title
			def A_richardson_func(z_1):
				if key.split("_")[0] == "bg":
					return 2 * z_1 / (1+(z_1**2))
				if key.split("_")[0] == "gg":
					return (z_1/(1-(z_1*(1-z_1))))**2
	
			def B_richardson_func(z_2):
				if key.split("_")[1] == "qq":
					helper= -2*z_2 * (1-z_2)
					return helper/(1+helper)
				if key.split("_")[1] == "gg":
					helper= z_2 * (1-z_2)
					return (helper / (1-helper))**2
			def richardson_theory(A_param, B_param, x):
				return (1/ (2* np.pi))* (1+ (A_param*B_param* np.cos(2*x)))
			def normalise(func, A_param, B_param):
					return quad(lambda x: func(A_param, B_param, x), -1*np.pi, np.pi )[0]
			A_richardson= quad(A_richardson_func, zcut_1, 1-zcut_1)[0]
			B_richardson= quad(B_richardson_func, zcut_2, 1-zcut_2)[0]
			x_theory= np.linspace(-np.pi, np.pi, 1000)
			theory= richardson_theory(A_richardson, B_richardson, x_theory)
			theory=  theory / normalise(richardson_theory, A_richardson, B_richardson)
			ax.plot(x_theory, theory, label="theory", color='r')

		elif paper== "panscales_lund":
			title= "panscales_lund_" + title
		if boost_bool == True:
			title= title + "_boosted"
		else:
			title= title + "_no boost"
		if (paper == "panscales_no_nonsense") or (paper == "panscales_lund"):
			xlabel= "Delta psi (rad)"
		elif paper== "richardson":
			xlabel= "Delta phi (rad)"
		
				
		heights, bin_centres, bin_edges, weights_norm, uncert= binning(obs_dict[key][:,0], obs_dict[key][:,1], 50)
		ax.stairs(values= heights, edges= bin_edges, label=r"$z_1= $ "+str(zcut_1)+r" $z_2= $" + str(zcut_2),color='b')
		ax.errorbar(x= bin_centres, y=heights, yerr= uncert, fmt='x', capsize=1, elinewidth=1, color='b', markersize=3)
		ax.set_title(title)
		ax.set_xlabel(xlabel)
		ax.set_ylabel("normalised diff cross section")
		ax.legend()
		fig.savefig(outdir+title + "_intrajet" +".png")
		plt.close()

	return None


def main():
	
	PATH= "/Users/karimkandeel/Documents/mphys_sem_2/big_data_tests/Richardson_ult/christoph_even_with_correl/christoph_even_with_correl.parquet"
	ZCUT= 0.3 # has to be less than 0.5, is symmetric   e.g ZCUT=0.3 accepts 0.3 < z < 0.7 # for interjet
	ZCUT_1= 0.2 # maximum z for the first branch
	ZCUT_2= 0.4 # # has to be less than 0.5, is symmetric   e.g ZCUT=0.3 accepts 0.3 < z < 0.7
	dirpath= os.path.dirname(PATH) + "/"
	parquet_file = pq.ParquetFile(PATH)
	headers = parquet_file.schema.names
	chunk_count= 0

	###################### interjet dicts ######################
	richardson_interjet_boosted= {}
	richardson_interjet_not_boosted= {}
	panscales_no_nonsense_interjet_boosted= {}
	panscales_no_nonsense_interjet_not_boosted= {}
	interjet_dict_keys= ["gg_qqqq", "gg_gggg", "gg_qqgg", "bb_qgqg"] #ORDER PROBABLY DOESN'T MATTER
	richardson_interjet_boosted.update({key: np.empty([0,2]) for key in interjet_dict_keys})
	richardson_interjet_not_boosted.update({key: np.empty([0,2]) for key in interjet_dict_keys})
	panscales_no_nonsense_interjet_boosted.update({key: np.empty([0,2]) for key in interjet_dict_keys})
	panscales_no_nonsense_interjet_not_boosted.update({key: np.empty([0,2]) for key in interjet_dict_keys})
	############################################################

	###################### intrajet dicts ######################
	richardson_intrajet_boosted= {}
	richardson_intrajet_not_boosted= {}
	panscales_no_nonsense_intrajet_boosted= {}
	panscales_no_nonsense_intrajet_not_boosted= {}
	intrajet_dict_keys= ["bg_qq", "bg_gg", "gg_qq"] #ORDER PROBABLY DOESN'T MATTER ## gg_qq is not implemented yet
	richardson_intrajet_boosted.update({key: np.empty([0,2]) for key in intrajet_dict_keys})
	richardson_intrajet_not_boosted.update({key: np.empty([0,2]) for key in intrajet_dict_keys})
	panscales_no_nonsense_intrajet_boosted.update({key: np.empty([0,2]) for key in intrajet_dict_keys})
	panscales_no_nonsense_intrajet_not_boosted.update({key: np.empty([0,2]) for key in intrajet_dict_keys})

	############################################################


	for i in range(parquet_file.num_row_groups):
		chunk = parquet_file.read_row_group(i).to_pandas()

		event_weight= chunk["EventWeight"].to_numpy()
		############# interjet #############
		richardson_interjet_boosted, richardson_interjet_not_boosted, panscales_no_nonsense_interjet_boosted, panscales_no_nonsense_interjet_not_boosted= interjet_obs(
			pids(chunk), interjet_momenta(chunk), event_weight, ZCUT, interjet_dict_keys, richardson_interjet_boosted, richardson_interjet_not_boosted,
			  panscales_no_nonsense_interjet_boosted, panscales_no_nonsense_interjet_not_boosted)
		####################################

		############# intrajet #############
		richardson_intrajet_boosted, richardson_intrajet_not_boosted, panscales_no_nonsense_intrajet_boosted, panscales_no_nonsense_intrajet_not_boosted= intrajet_obs(
			pids(chunk), intrajet_momenta(chunk), event_weight, ZCUT_1, ZCUT_2, richardson_intrajet_boosted, richardson_intrajet_not_boosted,
				panscales_no_nonsense_intrajet_boosted, panscales_no_nonsense_intrajet_not_boosted)

		####################################
		chunk_count += 1
		print("chunk ", chunk_count, " done")
	plot_interjet(richardson_interjet_boosted, ZCUT, True, "richardson", dirpath)
	plot_interjet(richardson_interjet_not_boosted, ZCUT, False, "richardson", dirpath)
	plot_interjet(panscales_no_nonsense_interjet_boosted, ZCUT, True, "panscales_no_nonsense", dirpath)
	plot_interjet(panscales_no_nonsense_interjet_not_boosted, ZCUT, False, "panscales_no_nonsense", dirpath)

	plot_intrajet(richardson_intrajet_boosted, ZCUT_1, ZCUT_2, True, "richardson", dirpath)
	plot_intrajet(richardson_intrajet_not_boosted, ZCUT_1, ZCUT_2, False, "richardson", dirpath)
	plot_intrajet(panscales_no_nonsense_intrajet_boosted, ZCUT_1, ZCUT_2, True, "panscales_no_nonsense", dirpath)
	plot_intrajet(panscales_no_nonsense_intrajet_not_boosted, ZCUT_1, ZCUT_2, False, "panscales_no_nonsense", dirpath)




	return None

main()




