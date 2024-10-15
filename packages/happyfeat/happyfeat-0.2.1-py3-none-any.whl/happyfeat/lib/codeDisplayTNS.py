import numpy as np
import glob
from os import listdir
import matplotlib.pyplot as plt

path1 = 'C:/Users/arthur.desbois/Documents/dev/happyFeat/workspace/Testsub/NS_MI.npy'
path2 = 'C:/Users/arthur.desbois/Documents/dev/happyFeat/workspace/Testsub/NS_Rest.npy'


MATRIX_To_Display_MI = np.load(path1)
MATRIX_To_Display_Rest = np.load(path2)
#MATRIX_To_Display_MI = MATRIX_To_Display_MI.transpose(0,2,1,3)
#MATRIX_To_Display_Rest = MATRIX_To_Display_Rest.transpose(0,2,1,3)

MATRIX_To_Display = (MATRIX_To_Display_MI.mean(0)-MATRIX_To_Display_Rest.mean(0))/MATRIX_To_Display_Rest.mean(0)

def channel_generator(number_of_channel, Ground, Ref):
    if number_of_channel == 32:
        electrodes = ['Fp1','Fp2','F7','F3','Fz','F4','F8','FC5','FC1','FC2','FC6','T7','C3','Cz','C4','T8','TP9','CP5','CP1','CP2','CP6','TP10','P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10']
        for i in range(len(electrodes)):
            if (electrodes[i] == Ground):
                index_gnd = i
            if (electrodes[i] == Ref):
                index_ref = i
        electrodes[index_gnd] = 'AFz'
        electrodes[index_ref] = 'FCz'

    if number_of_channel == 64:
        #electrodes = ['FP1','FP2','F7','F3','Fz','F4','F8','FC5','FC1','FC2','FC6','T7','C3','Cz','C4','T8','TP9','CP5','CP1','CP2','CP6','TP10','P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10','AF7','AF3','AF4','AF8','F5','F1','F2','F6','FT9','FT7','FC3','FC4','FT8','FT10','C5','C1','C2','C6','TP7','CP3','CPz','CP4','TP8','P5','P1','P2','P6','PO7','PO3','POz','PO4','PO8']
        electrodes = ['Fp1','Fz','F3','F7','FT9','FC5','FC1','C3','T7','TP9','CP5','CP1','Pz','P3','P7','O1','Oz','O2','P4','P8','TP10','CP6','CP2','Cz','C4','T8','FT10','FC6','FC2','F4','F8','Fp2','AF7','AF3','AFz','F1','F5','FT7','FC3','C1','C5','TP7','CP3','P1','P5','PO7','PO3','POz','PO4','PO8','P6','P2','CPz','CP4','TP8','C6','C2','FC4','FT8','F6','AF8','AF4','F2','Iz']
        for i in range(len(electrodes)):
            if (electrodes[i] == Ground):
                index_gnd = i
            if (electrodes[i] == Ref):
                index_ref = i
        electrodes[index_gnd] = 'FCz'
        electrodes[index_ref] = 'Fpz'

    return electrodes

electrodes = channel_generator(64, 'TP9', 'TP10')
# electrode_Cortex = ['C1','FC1','Cz','FCz','CPz','CP3']
electrode_Cortex = ['C1']

Index_electrode =[]
test = False
for i in range(len(electrodes)):
    for j in electrode_Cortex:
        if electrodes[i] == j:
            Index_electrode.append(i)
            test = True
            print(j)
            break




Index_electrode = np.array(Index_electrode)

font_princ = {'family': 'serif',
    'color':  'black',
    'weight': 'normal',
    'size': 15,
    }

font = {'family': 'serif',
    'color':  'black',
    'weight': 'normal',
    'size': 15,
    }

# electrode = ['FC3','FC1','FC5','FCz','FC6','FC2','FC4','C5','C3','C1','Cz','C2','C4','C6','CP5','CP3','CP1','CPz','CP2','CP4','CP6']
electrode = ['C1']
time_seres = []
# for i in range(24):
#     if i%6 !=0:
#         time_seres.append('')
#     else:
#         time_seres.append(i/6)
divi = 3/15
for i in range(15):
    time_seres.append(divi)
    divi = divi + 3/15



freq_seres = []
frq_dep = 4
for i in range(0,360):
    if i%10!=0:
        freq_seres.append('')
    else:
        freq_seres.append(round(frq_dep))
    frq_dep = frq_dep + 1




fig,ax = plt.subplots()

freqres = 0.1

Disp_Strat_1 = (MATRIX_To_Display[Index_electrode,:, 40:400])
im = ax.imshow(Disp_Strat_1.T,cmap='jet',origin ='lower',aspect = 'auto',
               vmin = - np.nanmax(abs(MATRIX_To_Display[Index_electrode,:, 40:400])),
               vmax =   np.nanmax(abs(MATRIX_To_Display[Index_electrode,:, 40:400])))
plt.show()
# ax.set_xticks(range(15))
# ax.set_xticklabels(time_seres, rotation=90)
# ax.set_yticks(range(0,36))
# ax.set_yticklabels(freq_seres)
# ax.tick_params(axis='both', which='both', length=0)
# cbar = fig.colorbar(im, ax=ax)
# cbar.set_label('ERD/ERS', rotation=270,labelpad = 15)
# ax.set_xlabel(' Time (s)', fontdict=font)
# ax.set_ylabel('Frequency (Hz)', fontdict=font)
# ax.set_title( 'Strat '+ str(('strat2'))+ ' Sensor ERD/ERS ',fontdict = font_princ)
# #strat_str +=1
# plt.show()
