"""
    Uses the .hdf5 file generated by pyVox.py to visualize the active-site
    ligand interactions.
    User has four inputs:
        1) what set to look at (train, val, test)
        2) what index from that set would you like to see
        3) what mode (e: shows electrons only, n:shows nuclei only, b: shows both)
        4) path to file with protein ligand dataset hdf5
"""

import numpy as np
import h5py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import sys



def make_ax(grid=False):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_axis_off()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.grid(grid)
    return ax

def main():
    voxelizedDataPath = str(sys.argv[4]) #path to file with protein ligand dataset hdf5
    activeCache = str(sys.argv[5]) #path to file with active cache
    set = str(sys.argv[1]) #Which set to pull from, (train, val, test)
    index = int(sys.argv[2]) #Which index in the set to graph data
    mode = str(sys.argv[3]) #e = electrons, n = nuclei, b = both


    validSets = ['Train', 'train', 'Test', 'test', 'validation', 'Validation', 'val', 'Val']
    trainSet = ['Train', 'train']
    testSet = ['Test', 'test']
    valSet = ['Val', 'val']
    validModes = ['b','B','e','E','n','N']
    eSet = ['E','e']
    nSet = ['N','n']
    bSet = ['B','b']

    if set not in validSets:
        raise RuntimeError('valid sets are train, test, val') from error
    if mode not in validModes:
        raise RuntimeError('valid modes are e, n, b') from error

    if mode in eSet:
        eShow = True
        nShow = False
        modePrintLabel = "Showing only electrons"
    elif mode in nSet:
        nShow = True
        eShow = False
        modePrintLabel = "Showing only nuclei"
    elif mode in bSet:
        eShow = True
        nShow = True
        modePrintLabel = "Showing both electrons and nuclei"

    h5f = h5py.File(activeCache,'r')
    siteMatrix = h5f['activeCacheMatrix'][:]
    h5f.close()



    h5f = h5py.File(voxelizedDataPath,'r')
    if set in trainSet:
        ligandProMatrix = h5f['train_ligands'][index,:,:,:,:]
        ligandProLabel = h5f['train_labels'][index]
        setName = 'training data'
    elif set in valSet:
        ligandProMatrix = h5f['val_ligands'][index,:,:,:,:]
        ligandProLabel = h5f['val_labels'][index]
        setName = 'validation data'
    elif set in testSet:
        ligandProMatrix = h5f['test_ligands'][index,:,:,:,:]
        ligandProLabel = h5f['test_labels'][index]
        setName = 'testing data'
    h5f.close()




    ligandMatrixElectrons = np.subtract(ligandProMatrix[:,:,:,0], siteMatrix[:,:,:,0])
    ligandMatrixNuclei = np.subtract(ligandProMatrix[:,:,:,1], siteMatrix[:,:,:,1])

    np.set_printoptions(threshold=np.nan)
    ligandMatrixElectrons = ligandMatrixElectrons.clip(min=0)
    ligandMatrixNuclei = ligandMatrixNuclei.clip(min=0)

    print("\n" * 5)
    print('---------------------------------------------------------')
    print('                     Voxel Viewer')
    print('---------------------------------------------------------')
    print("Mode               : "+modePrintLabel)
    print("Using              : "+setName)
    print("Data index         : "+str(index))
    print("Interaction energy : "+str(ligandProLabel))
    print('---------------------------------------------------------')
    print('            Graph may take a minute to load')
    print("\n" * 3)


    actEColor = [1, 0, 0, .01]
    actNColor = [0, 1, 1, .05]
    ligEColor = [0, 0, 1, .1]
    ligNColor = [1, 1, 0, .5]
    line = [255/255,182/255,193/255,.03]

    ax = make_ax(True)
    if eShow:
        ax.voxels(siteMatrix[:,:,:,0], facecolors=actEColor, edgecolors=line)
        ax.voxels(ligandMatrixElectrons, facecolors=ligEColor, edgecolors=line)


    if nShow:
        ax.voxels(siteMatrix[:,:,:,1], facecolors=actNColor, edgecolors=line)
        ax.voxels(ligandMatrixNuclei, facecolors=ligNColor, edgecolors=line)

    ax.elev = -60
    ax.azim = 230.1
    ax.dist = 8.0


    plt.show()

#Run the main fuction
if __name__ == "__main__":
    main()
