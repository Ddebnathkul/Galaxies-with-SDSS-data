import matplotlib.pyplot as plt
import math 
import numpy as np
import numpy
import csv 
import pandas as pd
import seaborn as sns
from pyrolite.plot import pyroplot
from pyrolite.plot.density import density
from pyrolite.comp.codata import close

################# READING THE CSV FILE ###########

with open('MyTable_1_Dwaipayan.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            line_count += 1

    print(f'Processed {line_count} lines.')

df = pd.read_csv("MyTable_1_Dwaipayan.csv", header=0, skip_blank_lines=True, )


########### DATA ##################################
g_data=df['g']
r_data=df['r']
Mr_data=df['Mr']
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
	r50_tot= r50_g[i] + r50_r[i] + r50_u[i] + r50_i[i] + r50_z[i]
	if (r50_tot > 0):
		r50 = numpy.log(r50_tot)
		eff_r.append(r50)
	else:
		r50 = numpy.log(0)
		eff_r.append(r50)
	


fig, axs = plt.subplots(figsize=(6,4))
counts,xbins,ybins=np.histogram2d(gr_data,Mr_data,bins=100, range=[[0,1],[-26, -14]], density=True)

#mylevels=[0.001, 0.1, 1]
pcp0= plt.contour(counts.transpose(), extent=[xbins.min(),xbins.max(),ybins.min(),ybins.max()], cmap='rainbow')
fig.colorbar(pcp0, ax=axs)



g_sns=[]
Mr_sns=[]
r50_sns=[]


for i in range(len(g_data)):
	if ((gr_data[i]>0) and (gr_data[i]<1.1) and (Mr[i]>-22) and (Mr[i]<-16) and (eff_r[i]>1) and (eff_r[i]<5)):
		g_s=gr_data[i]
		g_sns.append(g_s)
		Mr_s=Mr[i]
		Mr_sns.append(Mr_s)
		r50_s=eff_r[i]
		r50_sns.append(r50_s)
				



d = {'g_sns': g_sns, 'Mr_sns': Mr_sns}
df_pd = pd.DataFrame(data=d)

fig, axs = plt.subplots(figsize=(6,4))
h= sns.jointplot(data=df_pd, x="g_sns", y="Mr_sns", hue="species", kind="kde", cmap='rocket_r' ,color='k', fill=False, cbar=True)
h.set_axis_labels('g-r', r'$M_r - 5log_{10}{h}$', fontsize=16)
plt.tight_layout()
plt.savefig('mr_cont')


d_1 = {'g_sns': g_sns, 'r50_sns': r50_sns}
df_1pd = pd.DataFrame(data=d_1)

fig, axs = plt.subplots(figsize=(6,4))
h= sns.jointplot(data=df_1pd, x="g_sns", y="r50_sns", hue="species", kind="kde", cmap='rocket_r' ,color='k', fill=False, cbar=True)
h.set_axis_labels('g-r', r'$log_{10}[{r_{50}}]$', fontsize=16)
plt.tight_layout()
plt.savefig('r50_cont')
