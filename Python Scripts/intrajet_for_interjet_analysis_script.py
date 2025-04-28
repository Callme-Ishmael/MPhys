
# NOT ALL FUNCTIONS ARE THE SAME AS GLOBAL ANALYSIS SCRIPT
#^^^^^^^^^^^^^^^^^^^^^^^^^
# TAKE CARE OF THIS

import numpy as np
import pandas as pd
import matplotlib.colors as colors
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
from scipy.stats import binned_statistic_2d

def concatenate_vector_arrays(*arrays):
	keys = ["px", "py", "pz", "E"]
	return vector.array({key: np.concatenate([getattr(a, key) for a in arrays]) for key in keys })


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


def binning_2d(x, y, weights, bins):
	if len(weights) == 0:
		print("error: weights array is empty. Returning a dummy plot.")
		return np.ones(5), np.ones(5), np.ones(6), np.ones(5), np.ones(5)
	weights= weights / np.sum(weights)
	try:
		count, x_edges, y_edges, bin_number=binned_statistic_2d(x=x, y=y, values=weights,statistic='sum', bins=bins, expand_binnumbers=True)
	except:
		print("binning_2d failed")
		if np.isnan(x).any():
			print("nan values in x")
			print("number of nan vals= ",np.shape(np.where(np.isnan(x))))
		if np.isinf(x).any():
			print("inf values in x")
			print("number of inf vals= ",np.shape(np.where(np.isinf(x))))
		return 4*np.ones((5,5)), np.ones((5,5)), np.ones(6), np.ones(6), np.ones(5), np.ones((5,5))
	bin_width_x= x_edges[1] - x_edges[0]
	bin_width_y= y_edges[1] - y_edges[0]
	w2= weights**2
	bin_centres= (x_edges[:-1] + x_edges[1:]) / 2
	var= np.zeros((len(x_edges)-1, len(y_edges)-1))
	for i in range(1,len(x_edges)):
		for j in range(1,len(y_edges)):
			var[i-1,j-1]= np.sum(w2[np.intersect1d(np.argwhere(bin_number.T[:,0] == i), np.argwhere(bin_number.T[:,1] == j))])
	return count / (bin_width_x * bin_width_y), bin_centres, x_edges, y_edges, weights / (bin_width_x * bin_width_y), np.sqrt(var) / (bin_width_x * bin_width_y)

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


def intrajet_momenta_new(df):

	c1= vector.array({"E": df['b1E'],
												"px": df['b1px'],
												"py": df['b1py'],
												"pz": df['b1pz']})
	c3= vector.array({"E": df['b2E'],
												"px": df['b2px'],
												"py": df['b2py'],
												"pz": df['b2pz']})

	gc3= vector.array({"E": df['c1E'],
												"px": df['c1px'],
												"py": df['c1py'],
												"pz": df['c1pz']})
	gc4= vector.array({"E": df['c2E'],
												"px": df['c2px'],
												"py": df['c2py'],
												"pz": df['c2pz']})

	gc7= vector.array({"E": df['c3E'],
												"px": df['c3px'],
												"py": df['c3py'],
												"pz": df['c3pz']})
	gc8= vector.array({"E": df['c4E'],
												"px": df['c4px'],
												"py": df['c4py'],
												"pz": df['c4pz']})
	
	c2= gc3 + gc4
	p1= c1 + c2
	c4= gc7 + gc8
	p2= c3 + c4

	gc1= c1 * 0
	gc2= c1 * 0

	gc5= c3 * 0
	gc6= c3 * 0

	return p1, p2, c1, c2, c3, c4, gc1, gc2, gc3, gc4, gc5, gc6, gc7, gc8




def pids_new(df):

	C1_pid= df['b1PID'].to_numpy()

	C3_pid= df['b2PID'].to_numpy()

	GC3_pid= df['c1PID'].to_numpy()
	GC4_pid= df['c2PID'].to_numpy()

	GC7_pid= df['c3PID'].to_numpy()
	GC8_pid= df['c4PID'].to_numpy()


	P1_pid= C1_pid
	C2_pid= np.ones(len(C1_pid)) * 21  #always a gluon

	P2_pid= C3_pid
	C4_pid= np.ones(len(C3_pid)) * 21  #always a gluon

	GC1_pid= np.zeros(len(C1_pid))
	GC2_pid= np.zeros(len(C1_pid))
	GC5_pid= np.zeros(len(C1_pid))
	GC6_pid= np.zeros(len(C1_pid))

	return P1_pid, P2_pid, C1_pid, C2_pid, C3_pid, C4_pid, GC1_pid, GC2_pid, GC3_pid, GC4_pid, GC5_pid, GC6_pid, GC7_pid, GC8_pid




def panscales_no_nonsense_intrajet(parent, parent_spectator, spectator, intermediate, gc1, gc2, event_weight, boost_bool, zcut_1, zcut_2):
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
	return np.array([delta_12, event_weight]).T, np.argwhere((mask_cuts_1 & mask_cuts_2)).flatten()


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




def intrajet_for_interjet_obs(pids, all_momenta, event_weight, zcut_1, zcut_2, pan_dict):
	# only implemented for unboosted case
	# only implemented for panscales no nonsense observable
	funcs_primary_list= [[filter_intra_bg_qq_1, filter_intra_bg_qq_2], [filter_intra_bg_gg_1, filter_intra_bg_gg_2], [filter_intra_gg_qq_1, filter_intra_gg_qq_2]] #intrajet functions # ORDER MATTERS

	for func_pair in funcs_primary_list:
		func_1= func_pair[0]
		func_2= func_pair[1]
		args_1, category_1= func_1(pids)
		args_2, category_2= func_2(pids)
		args, indices_1, indices_2= np.intersect1d(args_1, args_2, assume_unique=False, return_indices=True)
		category_1= category_1[indices_1]
		category_2= category_2[indices_2]

		weights= event_weight[args]
		tag= (func_1.__name__).split("_")[2] + "_" + (func_1.__name__).split("_")[3]
		parent_1= all_momenta[0][args]
		parent_spectator_1= all_momenta[1][args]
		spectator_1= np.where(category_1 == 0 , all_momenta[3][args], all_momenta[2][args]).view(vector.MomentumNumpy4D)
		intermediate_1= np.where(category_1 == 0 , all_momenta[2][args], all_momenta[3][args]).view(vector.MomentumNumpy4D)
		gc1_1= np.where(category_1 == 0 , all_momenta[6][args], all_momenta[8][args]).view(vector.MomentumNumpy4D)
		gc2_1= np.where(category_1 == 0 , all_momenta[7][args], all_momenta[9][args]).view(vector.MomentumNumpy4D)
		#spectator with category mask concatenated with spectator with ! category mask(one is gluon the other is quark)
		parent_2= all_momenta[1][args]
		parent_spectator_2= all_momenta[0][args]
		spectator_2= np.where(category_2 == 0 , all_momenta[5][args], all_momenta[4][args]).view(vector.MomentumNumpy4D)
		intermediate_2= np.where(category_2 == 0 , all_momenta[4][args], all_momenta[5][args]).view(vector.MomentumNumpy4D)
		gc1_2= np.where(category_2 == 0 , all_momenta[10][args], all_momenta[12][args]).view(vector.MomentumNumpy4D)
		gc2_2= np.where(category_2 == 0 , all_momenta[11][args], all_momenta[13][args]).view(vector.MomentumNumpy4D)

		pan_branch_1_obs, surviving_args_1= panscales_no_nonsense_intrajet(parent_1, parent_spectator_1, spectator_1, intermediate_1, gc1_1, gc2_1, weights, False, zcut_1, zcut_2)
		pan_branch_2_obs, surviving_args_2= panscales_no_nonsense_intrajet(parent_2, parent_spectator_2, spectator_2, intermediate_2, gc1_2, gc2_2, weights, False, zcut_1, zcut_2)
		#addressing the case where cuts remove events from one branch but not the other # THE LOGIC IS SO TRICKY IN THE FOLLOWING LINES
		matched_surviving_args_1, matched_surviving_args_2= np.intersect1d(surviving_args_1, surviving_args_2, return_indices=True)[1:3]
		pan_dict[tag + "_1"]= np.vstack((pan_dict[tag + "_1"], pan_branch_1_obs[matched_surviving_args_1]))
		pan_dict[tag + "_2"]= np.vstack((pan_dict[tag + "_2"], pan_branch_2_obs[matched_surviving_args_2]))

	return pan_dict
	
def plot(array_of_dicts, zcut_1, zcut_2, boosted, tag, dirpath):
	CMAP= "viridis"
	os.system("mkdir -p " + dirpath)
	bin_edges= np.linspace(-np.pi, np.pi, 15)
	dict_1, dict_2= array_of_dicts
	keys= dict_1.keys()
	print(keys)
	channels= []
	for key in keys:
		channels.append(key.split('_')[0] + "_" + key.split('_')[1])
	channels= np.unique(channels)
	print(channels)

	for channel in channels:
		print("plotting ", channel)
		first_branch_1= dict_1[channel + "_1"]
		second_branch_1= dict_1[channel + "_2"]
		first_branch_2= dict_2[channel + "_1"]
		second_branch_2= dict_2[channel + "_2"]
		print("lengths are ", len(first_branch_1), len(second_branch_1), len(first_branch_2), len(second_branch_2))
		try:
			min_weight_1= np.min(first_branch_1[:,1])
			min_weight_2= np.min(first_branch_2[:,1])
			max_weight_1= np.max(first_branch_1[:,1])
			max_weight_2= np.max(first_branch_2[:,1])
			
			#plot weighted counts
			fig, ax= plt.subplots(1, 2, figsize=(20, 10))
			#norm = colors.Normalize(vmin= min(min_weight_1,min_weight_2), vmax= max(max_weight_1,max_weight_2))

			hist_count_1= ax[0].hist2d(first_branch_1[:,0], second_branch_1[:,0], bins= bin_edges, weights=first_branch_1[:,1], cmap=CMAP)
			hist_count_2= ax[1].hist2d(first_branch_2[:,0], second_branch_2[:,0], bins= bin_edges, weights=first_branch_2[:,1], cmap=CMAP)
			ax[0].set_title(channel + " data in path 1")
			ax[1].set_title(channel + " data in path 2")
			ax[0].set_xlabel(r"$\Delta \psi$")
			ax[1].set_xlabel(r"$\Delta \psi$")
			ax[0].set_ylabel(r"$\Delta \psi$")
			ax[1].set_ylabel(r"$\Delta \psi$")
			fig.colorbar(hist_count_1[3], ax=ax[0])
			fig.colorbar(hist_count_2[3], ax=ax[1])
			plt.savefig(dirpath + channel + "_counts.png")
			plt.close(fig)

			#plot weighted asymmetry parameter
			fig,ax= plt.subplots(1, 2, figsize=(20, 10))
			
			count_1, bin_centres, x_edges, y_edges, weights_1, errors_1= binning_2d(first_branch_1[:,0], second_branch_1[:,0], first_branch_1[:,1], bin_edges)
			count_2, bin_centres, x_edges, y_edges, weights_2, errors_2= binning_2d(first_branch_2[:,0], second_branch_2[:,0], first_branch_2[:,1], bin_edges)
			asymmetry= np.true_divide(count_1 - count_2, count_1 + count_2)
			error_on_asymmetry= np.sqrt((1 - (asymmetry**2)) / (count_1 + count_2))
			asymmetry= np.nan_to_num(asymmetry)
			error_on_asymmetry= np.nan_to_num(error_on_asymmetry)

			asymm_hist= ax[0].pcolormesh(x_edges, y_edges, asymmetry, cmap=CMAP)
			error_asymm_hist= ax[1].pcolormesh(x_edges, y_edges, error_on_asymmetry, cmap=CMAP)
			ax[0].set_xlabel(r"$\Delta \psi$")
			ax[1].set_xlabel(r"$\Delta \psi$")
			ax[0].set_ylabel(r"$\Delta \psi$")
			ax[1].set_ylabel(r"$\Delta \psi$")
			ax[0].set_title(channel + " asymmetry parameter")
			ax[1].set_title(channel + " error on asymmetry parameter")
			fig.colorbar(asymm_hist, ax=ax[0])
			fig.colorbar(error_asymm_hist, ax=ax[1])
			plt.savefig(dirpath + channel + "_asymmetry.png")
			plt.close(fig)

			#plot significance
			fig, ax= plt.subplots(1, 1, figsize=(10, 10))
			significance= np.true_divide(asymmetry, error_on_asymmetry)
			significance= np.nan_to_num(significance)
			significance_hist= ax.pcolormesh(x_edges, y_edges, significance, cmap=CMAP)
			ax.set_xlabel(r"$\Delta \psi$")
			ax.set_ylabel(r"$\Delta \psi$")
			ax.set_title(channel + " significance")
			fig.colorbar(significance_hist, ax=ax)
			plt.savefig(dirpath + channel + "_significance.png")
			plt.close(fig)


			#plot asymmetry parameter



		except Exception as e:
			print("plotting failed for ", channel, " probably due to empty arrays")
			print(e)
			continue



	




	return None

def analyse_file(file_path, ZCUT_1, ZCUT_2, RIVET_BOOL):
	fname= os.path.basename(file_path)
	parquet_file = pq.ParquetFile(file_path)
	headers = parquet_file.schema.names
	chunk_count= 0

	###################### intrajet dicts ######################
	pan_dict= {}
	intrajet_dict_keys= ["bg_qq", "bg_gg", "gg_qq"] #ORDER PROBABLY DOESN'T MATTER ## gg_qq is not implemented yet
	pan_dict.update({key + "_1": np.empty([0,2]) for key in intrajet_dict_keys})
	pan_dict.update({key + "_2": np.empty([0,2]) for key in intrajet_dict_keys})

	############################################################


	for i in range(parquet_file.num_row_groups):
		chunk = parquet_file.read_row_group(i).to_pandas()

		
		event_weight= chunk["EventWeight"].to_numpy()
		############# intrajet #############
		if RIVET_BOOL:
			pan_dict= intrajet_for_interjet_obs(
				pids_new(chunk), intrajet_momenta_new(chunk), event_weight, ZCUT_1, ZCUT_2, pan_dict)
		else:
			pan_dict= intrajet_for_interjet_obs(
				pids(chunk), intrajet_momenta(chunk), event_weight, ZCUT_1, ZCUT_2, pan_dict)

		####################################
		chunk_count += 1
		print("chunk ", chunk_count, " done in ", fname)
		# if i == 10:
		# 	break
	
	return pan_dict




def main():
	RIVET_BOOL= True # True assumes the new rivet (where only the momenta of c1, gc3, gc4 + other side are included in the csv) old: richardson_ult / new: HBB_G_ALL
	PATH_1= "/Users/karimkandeel/Documents/mphys_sem_2/big_data_tests/HBB_G_ALL/even_spin_on_100M/cleaned/even_spin_on.parquet"
	PATH_2= "/Users/karimkandeel/Documents/mphys_sem_2/big_data_tests/HBB_G_ALL/odd_spin_on_100M/cleaned/odd_spin_on.parquet"
	OUTPUT_DIR= "/Users/karimkandeel/Documents/mphys_sem_2/big_data_tests/HBB_G_ALL/even_odd_intrajet_for_interjet/"
	ZCUT= 0.3 # has to be less than 0.5, is symmetric   e.g ZCUT=0.3 accepts 0.3 < z < 0.7
	ZCUT_1= 0.3 # maximum z for the first branch
	ZCUT_2= 0.3 # # has to be less than 0.5, is symmetric   e.g ZCUT=0.3 accepts 0.3 < z < 0.7
	array_of_dicts= []
	for PATH in [PATH_1, PATH_2]:
		array_of_dicts.append(analyse_file(PATH, ZCUT_1, ZCUT_2, RIVET_BOOL))
		
	plot(array_of_dicts, ZCUT_1, ZCUT_2, False, "panscales_no_nonsense", OUTPUT_DIR)



	return None

main()
