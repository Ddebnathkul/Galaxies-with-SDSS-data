import matplotlib.pyplot as plt
import math 
import numpy as np
import numpy
import csv 
import pandas as pd
import seaborn as sns

################# READING THE CSV FILE ###########

with open('MyTable_dd_Dwaipayan_0.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            line_count += 1

    print(f'Processed {line_count} lines.')

df = pd.read_csv("MyTable_dd_Dwaipayan_0.csv", header=0, skip_blank_lines=True )


########### DATA ##################################
g_data=df['g']
r_data=df['r']
Mr_data=df['Mr']
Mg_data=df['Mg']
r50_g = df['R50_g']
r50_r = df['R50_r']
r50_i = df['R50_i']
r50_u = df['R50_u']
r50_z = df['R50_z']
z=df['z']
h= 0.71 #HUBBLE CONSTANT

########### THE COLOR G-R #########################
gr_data=[]
for i in range (len(g_data)):
	gr= g_data[i]- r_data[i]
	gr_data.append(gr)

########### ABSOLUTE MAGNITUDE IN R BAND ##########
Mr=[]
for i in range (len(g_data)):
	M= Mr_data[i] - 5*math.log(h)
	Mr.append(M)
	
	
#### THE EFFECTIVE RADIUS (PETROSIAN RADIUS 50) ####
eff_r=[]
for i in range(len(g_data)):
	r50_tot= r50_r[i]
	if (r50_tot > 0):
		r50 = numpy.log10(r50_tot*h)
		eff_r.append(r50)
	else:
		r50 = numpy.log(0)
		eff_r.append(r50)
	

############### PLOTTING ##################

########### THE COLOR G-R #########################
### NORMALIZING ####
counts, bins = np.histogram(gr_data, bins=60, range=(0, 1.2))
counts_new=[]
for i in range(len(counts)):
	count_n = (counts[i] - np.min(counts))/(np.max(counts) - np.min(counts))
	counts_new.append(count_n)
fig, ax = plt.subplots(figsize=(6, 4))
plt.hist(bins[:-1], bins, weights=counts_new, align='mid', histtype='step', linewidth=1, edgecolor='k', fill=False)
ax.set_xlabel('g-r', fontsize=14)
ax.get_yaxis().set_visible(False) 
ax.get_xaxis().set_tick_params(which='minor', size=0)
ax.get_xaxis().set_tick_params(which='minor', width=0) 

plt.tight_layout()
plt.savefig('g_r')	

########### ABSOLUTE MAGNITUDE IN R BAND ##########
### NORMALIZING ####

counts_1, bins_1 = np.histogram(Mr, bins=50, range=(-22, -14))
counts_1new=[]
for i in range(len(counts_1)):
	count_1n = (counts_1[i] - np.min(counts_1))/(np.max(counts_1) - np.min(counts_1))
	counts_1new.append(count_1n)
fig, ax = plt.subplots(figsize=(6, 4))
plt.hist(bins_1[:-1], bins_1, weights=counts_1new, align='mid', histtype='step', linewidth=1, edgecolor='k', fill=False)
plt.gca().invert_xaxis()
ax.set_xlabel(r'$M_r - 5log_{10}{h}$', fontsize=14)
ax.get_yaxis().set_visible(False) 
ax.get_xaxis().set_tick_params(which='minor', size=0)
ax.get_xaxis().set_tick_params(which='minor', width=0) 
plt.tight_layout()	
plt.savefig('Mr')


#### THE EFFECTIVE RADIUS (PETROSIAN RADIUS 50) ####
### NORMALIZING ####
counts_2, bins_2 = np.histogram(eff_r, bins=50, range=(-0.4, 1.4))
counts_2new=[]
for i in range(len(counts_2)):
	count_2n = (counts_2[i] - np.min(counts_2))/(np.max(counts_2) - np.min(counts_2))
	counts_2new.append(count_2n)
fig, ax = plt.subplots(figsize=(6, 4))
plt.hist(bins_2[:-1], bins_2, weights=counts_2new, align='mid', histtype='step', linewidth=1, edgecolor='k', fill=False)
ax.set_xlabel(r'$log_{10}[{r_{50}}]$', fontsize=14)
ax.get_yaxis().set_visible(False) 
ax.get_xaxis().set_tick_params(which='minor', size=0)
ax.get_xaxis().set_tick_params(which='minor', width=0) 
plt.tight_layout()	
plt.savefig('r50')

################ REDSHIFT (Z) #####################
### NORMALIZING ####
counts_3, bins_3 = np.histogram(z, bins=20, range=(0, 0.06))
counts_3new=[]
for i in range(len(counts_3)):
	count_3n = (counts_3[i] - np.min(counts_3))/(np.max(counts_3) - np.min(counts_3))
	counts_3new.append(count_3n)
fig, ax = plt.subplots(figsize=(6, 4))
plt.hist(bins_3[:-1], bins_3, weights=counts_3new, align='mid', histtype='step', linewidth=1, edgecolor='k', fill=False)
ax.set_xlabel('Redshift(z)', fontsize=14)
ax.get_yaxis().set_visible(False) 
ax.get_xaxis().set_tick_params(which='minor', size=0)
ax.get_xaxis().set_tick_params(which='minor', width=0)
plt.tight_layout()	
plt.savefig('z')

################ CONTOUR PLOTS ######################
g_sns=[]
Mr_sns=[]
r50_sns=[]
for i in range(len(g_data)):
	if ((gr_data[i]>0.2) and (gr_data[i]<1) and (Mr[i]>-21) and (Mr[i]<-16) and (eff_r[i]>-0.2) and (eff_r[i]<1)):
		g_s=gr_data[i]
		g_sns.append(g_s)
		Mr_s=Mr[i]
		Mr_sns.append(Mr_s)
		r50_s=eff_r[i]
		r50_sns.append(r50_s)
################# G-R/M ##############################					
d = {'g_sns': g_sns, 'Mr_sns': Mr_sns}
df_pd = pd.DataFrame(data=d)
h= sns.jointplot(data=df_pd, x="g_sns", y="Mr_sns", hue="species", kind="kde", cmap='Greys' ,color='k', fill=False)
plt.gca().invert_yaxis()
h.set_axis_labels('g-r', r'$M_r - 5log_{10}{h}$', fontsize=16)
plt.tight_layout()
plt.savefig('mr_cont')


################# G-R/R50 #############################
d_1 = {'g_sns': g_sns, 'r50_sns': r50_sns}
df_1pd = pd.DataFrame(data=d_1)
h= sns.jointplot(data=df_1pd, x="g_sns", y="r50_sns", hue="species", kind="kde", cmap='Greys' ,color='k', fill=False)
h.set_axis_labels('g-r', r'$log_{10}[{r_{50}}]$', fontsize=16)
plt.tight_layout()
plt.savefig('r50_cont')

################# G-R/M_g ##############################					
d_3 = {'r50_sns': r50_sns,'Mr_sns': Mr_sns}
df_3pd = pd.DataFrame(data=d_3)
h= sns.jointplot(data=df_3pd, x="r50_sns", y="Mr_sns", hue="species", kind="kde", cmap='Greys' ,color='k', fill=False)
plt.gca().invert_yaxis()
h.set_axis_labels(r'$log_{10}[{r_{50}}]$', r'$M_r - 5log_{10}{h}$', fontsize=16)
plt.tight_layout()
plt.savefig('mr_r50')

plt.show()
