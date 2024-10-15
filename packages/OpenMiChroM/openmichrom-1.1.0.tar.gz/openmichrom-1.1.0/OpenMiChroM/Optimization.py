# Copyright (c) 2020-2023 The Center for Theoretical Biological Physics (CTBP) - Rice University
# This file is from the Open-MiChroM project, released under the MIT License.

R"""  
The :class:`~.Optimization` classes perform the energy function parameters training of the chromosomes based on experimental Hi-C data.
"""

# with OpenMM 7.7.0, the import calls have changed. So, try both, if needed
try:
    try:
        # >=7.7.0
        from openmm.app import *
    except:
        # earlier
        print('Unable to load OpenMM as \'openmm\'. Will try the older way \'simtk.openmm\'')
        from simtk.openmm.app import *
except:
    print('Failed to load OpenMM. Check your configuration.')

import numpy as np
import random
from scipy.spatial import distance
import scipy as sc
import itertools
from scipy.stats.stats import pearsonr
from sklearn.preprocessing import normalize
import os
import pandas as pd
import warnings

class AdamTraining:
    R"""
    The :class:`~.AdamTraining` class performs the parameters training for each selected loci pair interaction. 
    
    Details about the methodology are decribed in "Zhang, Bin, and Peter G. Wolynes. "Topology, structures, and energy landscapes of human chromosomes." Proceedings of the National Academy of Sciences 112.19 (2015): 6062-6067."
    
    
    The :class:`~.AdamTraining` class receive a Hi-C matrix (text file) as input. The parameters :math:`\mu` (mu) and rc are part of the probability of crosslink function :math:`f(r_{i,j}) = \frac{1}{2}\left( 1 + tanh\left[\mu(r_c - r_{i,j}\right] \right)`, where :math:`r_{i,j}` is the spatial distance between loci (beads) *i* and *j*.
    
    Args:
        mu (float, required):
            Parameter in the probability of crosslink function. (Default value = 2.0).
        rc (float, required):
            Parameter in the probability of crosslink function. (Default value = 2.0).
        eta (float, required):
            Learning rate applied in each step (Default value = 0.01).
        beta1 (float, required):
            The hyper-parameter of Adam are initial decay rates used when estimating the first and second moments of the gradient. (Default value = 0.9).
        beta2 (float, required):
            The hyper-parameter of Adam are initial decay rates used when estimating the first and second moments of the gradient. (Default value = 0.999).
        it (int, required)
            The iteration step  
        method (str, required):
            'classic':  Adam
            'qh': quassi-hyperbolic momentum Adam  
        
    """
    
    # Remove biases and hold a data storage for velocity and momentum changes phi
    def __init__(self, mu=2.0, rc = 2.0, eta=0.01, beta1=0.9, beta2=0.999, epsilon=1e-8, it=1, updateNeeded=False, update_storagePath='', method='classic'):
        self.m_dw, self.v_dw = None, None
        self.t = it
        

        # constants
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.eta = eta
        self.mu = mu
        self.rc = rc
        self.NFrames = 0
        self.method = method

      
        #HQ ADAM
        self.v_1 = 0.7
        self.v_2 = 1.0
        
        # to store the updating parameters
        if update_storagePath != '':
            self.adamStorage = os.path.join(os.getcwd(), update_storagePath)
        else:
            self.adamStorage = os.path.join(os.getcwd(), 'Adam')
        
        os.makedirs(self.adamStorage, exist_ok=True)
        self.updateNeeded = updateNeeded
        
        #this is done after to overwrite the already set values if updateNeeded was set to True
        self._getParams() 


        
    def _saveParams(self, iteration, moment, velocity):
        if self.updateNeeded == False:
            return
    
        with open(f'{self.adamStorage}/iteration.txt', 'w') as f:
            f.write(str(iteration))
        np.savetxt(f'{self.adamStorage}/moment.txt', moment)
        np.savetxt(f'{self.adamStorage}/velocity.txt', velocity)


                
    def _getParams(self):
        if self.updateNeeded == False:
            print('Adam Parameter Updating was not needed updateNeeded set to False')
            return

        iteration_file = f'{self.adamStorage}/iteration.txt'
        if not os.path.exists(iteration_file) or os.stat(iteration_file).st_size == 0:
            print(f'Warning: {iteration_file} does not exist or is empty. Starting from iteration 1.')
            self.t = 1
            return

        with open(iteration_file, 'r') as f:
            try:
                self.t = int(f.read().strip())
            except ValueError:
                print(f'Warning: {iteration_file} contains invalid data. Starting from iteration 1.')
                self.t = 1

        if self.t == 1:
            return

        self.m_dw = np.loadtxt(f'{self.adamStorage}/moment.txt')
        self.v_dw = np.loadtxt(f'{self.adamStorage}/velocity.txt')
            
        
    def _update(self, w, dw):
        R"""Adam optimization step. This function updates weights and biases for each step.
        """


        if self.m_dw is None:
            self.m_dw = np.zeros(np.shape(dw))
            self.v_dw = np.zeros(np.shape(dw))
            
        ## dw, db are from current minibatch
        ## momentum beta 1
        # *** weights *** #
        self.m_dw = self.beta1*self.m_dw + (1-self.beta1)*dw

        ## rms beta 2
        # *** weights *** #
        self.v_dw = self.beta2*self.v_dw + (1-self.beta2)*(dw**2)
        

        ## weight correction
        m_dw_corr = self.m_dw/(1-self.beta1**self.t)
        v_dw_corr = self.v_dw/(1-self.beta2**self.t)

        ## update weights
        if self.method == 'qh':
            #QH Adam
            w = w - (self.eta * ((1 - self.v_1) * dw + self.v_1 * m_dw_corr) / (np.sqrt((1 - self.v_2) * np.power(dw, 2) + self.v_2 * v_dw_corr) + self.epsilon))
        else: # else just in case theres a type error it would go to the default adam weight calculation
            # Adam
             w = w - self.eta*(m_dw_corr/(np.sqrt(v_dw_corr)+self.epsilon))
        
        self.t += 1
        
        self._saveParams(self.t, self.m_dw, self.v_dw)
        return w

    def getPars(self, HiC, centerRemove=False, centrange=[0,0], cutoff='deprecate', norm=True, cutoff_low=0.0, cutoff_high=1.0, KR=False, neighbors=0):
        R"""
        Receives the experimental Hi-C map (Full dense matrix) in a text format and performs the data normalization from Hi-C frequency/counts/reads to probability.
        
        Args:
            HiC (file, required):
                Experimental Hi-C map (Full dense matrix) in a text format.
            centerRemove (bool, optional):
                Whether to set the contact probability of the centromeric region to zero. (Default value: :code:`False`).
            centrange (list, required if **centerRemove** = :code:`True`)):
                Range of the centromeric region, *i.e.*, :code:`centrange=[i,j]`, where *i* and *j*  are the initial and final beads in the centromere. (Default value = :code:`[0,0]`).
            cutoff (float, optional):
                Cutoff value for reducing the noise in the original data. Values lower than the **cutoff** are considered :math:`0.0`.
        """
        
        warnings.warn("getPars is deprecated, use getHiCexp instead", DeprecationWarning)
        # get the file extension
        _, file_extension = os.path.splitext(HiC)
        if file_extension == '.npy':
            # use np.load if the file is a .npy file
            allmap = np.load(HiC)
        else:
            allmap = np.loadtxt(HiC)

        if KR==True:
            allmap = self.knight_ruiz_balance(allmap)

        if norm==True:
            r=self.normalize_matrix(allmap)

            for i in range(len(r)-1):
                maxElem = r[i][i+1]
                if (maxElem != np.max(r[i])):
                    for j in range(len(r[i])):
                        if maxElem != 0.0:
                            r[i][j] = float(r[i][j] / maxElem)
                        else:
                            r[i][j] = 0.0 
                        if r[i][j] > 1.0:
                            r[i][j] = np.mean(np.diag(r,k=i))

            rd = np.transpose(r) 
            self.expHiC = r+rd + np.diag(np.ones(len(r)))
        else:
            self.expHiC = allmap
        
        if (centerRemove):
            centrome = range(centrange[0],centrange[1])
            self.expHiC[centrome,:] = 0.0
            self.expHiC[:,centrome] = 0.0
        
        #remove noise by cutoff    
        if cutoff!='deprecate':
            print('Depreaction warning!\nUsing `cutoff` in getPars is deprecated! Use either `cutoff_low` or `cutoff_high`. \nSetting cutoff_low=cutoff! \n')
            assert type(cutoff)==float, 'Cut off must be a float'
            cutoff_low = cutoff

        if cutoff_low>0.0:
            self.expHiC[self.expHiC<cutoff_low] = 0.0
        
        if cutoff_high<1.0:
            self.expHiC[self.expHiC>cutoff_high] = 0.0

        # Remove the number of Neighbors to optimize.
        M=self.expHiC
        neighbor_mask = np.abs(np.subtract.outer(np.arange(len(M)), np.arange(len(M)))) <= neighbors
        M[neighbor_mask] = 0.0
        self.expHiC = M

        self.mask = self.expHiC == 0.0

        self.phi_exp = self.expHiC
        self.reset_Pi()
            
    def normalize_matrix(self, matrix):
        R"""
        Normalize the matrix for simulation optimization. Here the first neighbor should have the probability of contact P=1.0.
        """
        matrix = np.nan_to_num(matrix, nan=0, posinf=0, neginf=0)
        np.fill_diagonal(matrix,0.0)

        max_values = np.amax(np.triu(matrix), axis=1)
        
        # To avoid division by zero, replace zeros with ones
        max_values[max_values == 0] = 0.0000001
        
        normalized_matrix = np.triu(matrix) / max_values[:, np.newaxis]
        # return normalized_matrix
        matrix= normalized_matrix + np.triu(normalized_matrix,k=1).T
        np.fill_diagonal(matrix,1.0)

        return matrix


    def knight_ruiz_balance(self, matrix, tol=1e-5, max_iter=100):
        R"""
        Perform the Knight-Ruiz matrix balancing.
        """
        A = np.array(matrix, dtype=float)
        n = A.shape[0]
        row_scaling = np.ones(n)
        col_scaling = np.ones(n)
        for _ in range(max_iter):
            row_scaling = np.sqrt(np.sum(A, axis=1))
            A /= row_scaling[:, None]
            col_scaling = np.sqrt(np.sum(A, axis=0))
            A /= col_scaling

            if np.all(np.abs(row_scaling - 1) < tol) and np.all(np.abs(col_scaling - 1) < tol):
                break

        return A

    
    
    def reset_Pi(self):
        R"""
        Resets Pi matrix to zeros
        """
        if not hasattr(self, "phi_exp"):
            print("Cannot reset Pi; HiC map shape unknown. Load HiC map first!")
        else:              
            self.Pi = np.zeros(self.phi_exp.shape)
            self.NFrames = 0


    def getHiCexp(self, HiC, centerRemove=False, centrange=[0,0], norm=True, cutoff_low=0.0, cutoff_high=1.0, KR=False, neighbors=0):
        R"""
        Receives the experimental Hi-C map (Full dense matrix) in a text format and performs the data normalization from Hi-C frequency/counts/reads to probability.
        
        Args:
            HiC (file, required):
                Experimental Hi-C map (Full dense matrix) in a text format.
            centerRemove (bool, optional):
                Whether to set the contact probability of the centromeric region to zero. (Default value: :code:`False`).
            centrange (list, required if **centerRemove** = :code:`True`)):
                Range of the centromeric region, *i.e.*, :code:`centrange=[i,j]`, where *i* and *j*  are the initial and final beads in the centromere. (Default value = :code:`[0,0]`).
            cutoff (float, optional):
                Cutoff value for reducing the noise in the original data. Values lower than the **cutoff** are considered :math:`0.0`.
        """

        # get the file extension
        _, file_extension = os.path.splitext(HiC)
        if file_extension == '.npy':
            # use np.load if the file is a .npy file
            allmap = np.load(HiC)
        else:
            allmap = np.loadtxt(HiC)

        if KR==True:
            allmap = self.knight_ruiz_balance(allmap)

        if norm==True:
            r=self.normalize_matrix(allmap)

            for i in range(len(r)-1):
                maxElem = r[i][i+1]
                if (maxElem != np.max(r[i])):
                    for j in range(len(r[i])):
                        if maxElem != 0.0:
                            r[i][j] = float(r[i][j] / maxElem)
                        else:
                            r[i][j] = 0.0 
                        if r[i][j] > 1.0:
                            r[i][j] = np.mean(np.diag(r,k=i))

            rd = np.transpose(r) 
            self.expHiC = r+rd + np.diag(np.ones(len(r)))
        else:
            self.expHiC = allmap
        
        if (centerRemove):
            centrome = range(centrange[0],centrange[1])
            self.expHiC[centrome,:] = 0.0
            self.expHiC[:,centrome] = 0.0
        
        #remove noise by cutoff 

        if cutoff_low>0.0:
            self.expHiC[self.expHiC<cutoff_low] = 0.0
        
        if cutoff_high<1.0:
            self.expHiC[self.expHiC>cutoff_high] = 0.0

        # Remove the number of Neighbors to optimize.
        M=self.expHiC
        neighbor_mask = np.abs(np.subtract.outer(np.arange(len(M)), np.arange(len(M)))) <= neighbors
        M[neighbor_mask] = 0.0
        self.expHiC = M

        self.mask = self.expHiC == 0.0

        self.phi_exp = self.expHiC
        self.reset_Pi()
    
    def reset_Pi(self):
        R"""
        Resets Pi matrix to zeros
        """
        if not hasattr(self, "phi_exp"):
            print("Cannot reset Pi; HiC map shape unknown. Load HiC map first!")
        else:              
            self.Pi = np.zeros(self.phi_exp.shape)
            self.NFrames = 0

    def probCalc(self, state):
        R"""
        Calculates the contact probability matrix for a given state.
        """

        Pi = 0.5*(1.0 + np.tanh(self.mu*(self.rc - distance.cdist(state,state, 'euclidean'))))
    
        self.Pi += Pi
        self.NFrames += 1

    def _getGrad(self):
        R"""
        Calcultes the gradient function.
        """
        return (-self.phi_sim + self.phi_exp)

    def getLamb(self, Lambdas, fixedPoints=None):
        R"""
        Calculates the Lagrange multipliers of each pair of interaction and returns the matrix containing the energy values for the optimization step.
        
        Args:
            Lambdas (file, required):
                The matrix containing the energies values used to make the simulation in that step. 
            fixedPoints (list, optional):
                List of all pairs (i,j) of interactions that will remain unchanged throughout the optimization procedure.
        
        Returns:
            :math:`(N,N)` :class:`numpy.ndarray`:
                Returns an updated matrix of interactions between each pair of bead.
        """
        self.phi_sim = self.Pi/self.NFrames
        self.phi_sim[self.mask] = 0.0

        grad = self._getGrad()

        self.lambdas = pd.read_csv(Lambdas, sep=None, engine='python')
        newlamb_values = self._update(self.lambdas.values, grad)



        if fixedPoints == None:
            lamb  = pd.DataFrame(newlamb_values,columns=list(self.lambdas.columns.values))
        else:
            for p in fixedPoints: #fixedPoints is a list of tuples for iteraction fixed i,j
                self.mask[p] = True

            lambs_final = np.where(self.mask,self.lambdas.values, newlamb_values)
            lamb  = pd.DataFrame(lambs_final,columns=list(self.lambdas.columns.values))

        self.error = np.sum(np.absolute(np.triu(self.phi_sim, k=3) - np.triu(self.phi_exp, k=3)))/np.sum(np.triu(self.phi_exp, k=3))

        return (lamb)

class FullTraining:
    R"""
    The :class:`~.FullTraining` class performs the parameters training for each selected loci pair interaction. 
    
    Details about the methodology are decribed in "Zhang, Bin, and Peter G. Wolynes. "Topology, structures, and energy landscapes of human chromosomes." Proceedings of the National Academy of Sciences 112.19 (2015): 6062-6067."
    
    
    The :class:`~.FullTraining` class receive a Hi-C matrix (text file) as input. The parameters :math:`\mu` (mu) and rc are part of the probability of crosslink function :math:`f(r_{i,j}) = \frac{1}{2}\left( 1 + tanh\left[\mu(r_c - r_{i,j}\right] \right)`, where :math:`r_{i,j}` is the spatial distance between loci (beads) *i* and *j*.
    
    Args:
        mu (float, required):
            Parameter in the probability of crosslink function. (Default value = 2.0).
        rc (float, required):
            Parameter in the probability of crosslink function, :math:`f(rc) = 0.5`. (Default value = 2.5).
        cutoff (float, optional):
            Cutoff value for reducing the noise in the original data. Values lower than the **cutoff** are considered :math:`0.0`.
        reduce (bool, optional):
            Whether to reduce the number of interactions to be considered in the inversion. If False, it will consider every possible interaction :math:`(N*(N-1)/2)`. If True, it is necessary to give values for the lower and higher cutoffs. (Default value: :code:`True`). 
        pair_h (int, required if **reduce** = :code:`True`):
            Loci selection to apply the high-resolution cutoff. If **pair_h** = 2, the interaction in the high-resolution index grid :math:`2 : 2 : N × 2:2:N`  are subject to a cutoff value **c_h**, where `N` is the total number of monomers interactions  (Default value = 2).
        c_h (float, required if **reduce** = :code:`True`)):
            The the high-resolution cutoff. (Default value = 0.1).
        pair_l (int, required if **reduce** = :code:`True`)):
            Loci selection to apply the high-resolution cutoff. If **pair_l** = 4, the interaction in the low-resolution index grid :math:`1:4:N×1:4:N`  are subject to a cutoff value **c_l**, where `N` is the total number of monomers interactions  (Default value = 4).
        c_l (float, required if **reduce** = :code:`True`)):
            The the low-resolution cutoff. (Default value = 0.02).
    """
    def __init__(self, expHiC, mu=2.0, rc=2.5, 
                 cutoff=0.0, reduce=True,
                 pair_h=2, c_h=0.1, pair_l=4, c_l=0.02
                ):
            
        self.mi = mu
        self.rc = rc
        self.cutoff = cutoff
        
        self.getHiCexp(expHiC, centerRemove=False, centrange=[0,0])
        self.hic_sparse = sc.sparse.csr_matrix(np.triu(self.expHiC, k=2))
        if (reduce):
            self.appCutoff(pair_h, c_h, pair_l, c_l)
       

        self.ind = self.get_indices(self.hic_sparse)

        self.size = len(self.ind)     
        self.Pi = np.zeros(self.size)
        self.Prob_dist = np.zeros(self.hic_sparse.shape)
        self.PiPj = np.zeros((self.size,self.size))
        self.NFrames = 0

    def createInitialLambda(self, sequenceFile, outputPath=".", initialGuess=0.0, baseLine=-0.2):
        lambdas = np.zeros(self.hic_sparse.shape) + baseLine
        for i in self.ind:
            lambdas[i] = initialGuess
        lambdas = np.triu(lambdas) + np.triu(lambdas).T
        
    def saveLambdas(self, sequenceFile, data, outputPath, name):
        seq = np.loadtxt(sequenceFile, dtype=str)[:,1]

        lamb = pd.DataFrame(data,columns=seq)
        lamb.to_csv(os.path.join(outputPath, name), index=False)
        print("{} file save in {}".format(name, outputPath))

        #self.saveLambdas(sequenceFile=sequenceFile, data=lambdas, outputPath=outputPath, name="lambda_0")

    def appCutoff(self, pair_h, c_h, pair_l, c_l):
        R"""
        Applies the cutoff for low- and high-resolution values.
        """
        N = self.hic_sparse.shape[0]
        print('Non-zero interactions before the cutoff: ', self.hic_sparse.nnz)

        hic_full = self.hic_sparse.todense()
        hic_final = np.zeros(self.hic_sparse.shape)


        values = [n for n in range(0,N,pair_h)]
        index =  [x for x in itertools.combinations_with_replacement(values, r=2)]
        for i in index:
            if (hic_full[i] > c_h):
                hic_final[i] = hic_full[i]

        high_cut_number =   sc.sparse.csr_matrix(np.triu(hic_final, k=2)).nnz
        print('Non-zero interactions after high-resolution cutoff ({}): {}'.format( c_h, high_cut_number ))

        values = [n for n in range(1,N,pair_l)]
        index =  [x for x in itertools.combinations_with_replacement(values, r=2)]
        for i in index:
            if (hic_full[i] > c_l):
                hic_final[i] = hic_full[i]
        self.hic_sparse = sc.sparse.csr_matrix(np.triu(hic_final, k=2))
        print('Non-zero interactions after low-resolution cutoff ({}): {}'.format(c_l,  (self.hic_sparse.nnz-high_cut_number) ))
        print('Total Non-zero interactions: {}'.format(self.hic_sparse.nnz))

    
    def get_indices(self, hic):
        R"""
        Receives non-zero interaction indices, *i.e.*, the loci pair *i* and *j* which interaction will be optimized.
        """
        index = sc.sparse.find(hic)
        self.rows = index[0]
        self.cols = index[1]
        self.values = index[2]
        ind = []
        for i in range(len(index[0])):
            ind.append((self.rows[i], self.cols[i]))
        return(ind)
        
    def probCalc(self, state):
        R"""
        Calculates the contact probability matrix and the cross term of the Hessian.
        """

        Prob = 0.5*(1.0 + np.tanh(self.mi*(self.rc - distance.cdist(state,state, 'euclidean'))))
    
        Pi = []
        for i in self.ind:
            Pi.append(Prob[i[0], i[1]])
        Pi = np.array(Pi)
    

        PiPj = np.outer(Pi,Pi)
        self.PiPj += PiPj                                       

     
        self.Prob_dist += Prob
        self.Pi += Pi
        self.NFrames += 1
        
    def getPearson(self):
        R"""
        Calculates the Pearson's Correlation between the experimental Hi-C used as a reference for the training and the *in silico* Hi-C obtained from the optimization step.
        """
        r1 = sc.sparse.csr_matrix((self.Pi/self.NFrames,(self.rows,self.cols)), shape=(self.expHiC.shape[0],self.expHiC.shape[0])).todense()
        r2 = self.hic_sparse.todense()

        r1[np.isinf(r1)]= 0.0
        r1[np.isnan(r1)]= 0.0
        r1[r1 <= 0.001]= 0.0
        r2[np.isinf(r2)]= 0.0
        r2[np.isnan(r2)]= 0.0
        r2[r2<=0.001] = 0.0

        np.fill_diagonal(r1,0.0)
        np.fill_diagonal(r2,0.0)


        SEED = 100
        random.seed(SEED)
        print(len(list(r1[np.triu_indices(np.shape(r1)[0])])))
        print("\n")
        print(int(0.01*np.shape(r1)[0]*np.shape(r1)[0]))                              
        
        a1 = np.asarray(random.sample(list(r1[np.triu_indices(np.shape(r1)[0])]),int(0.01*np.shape(r1)[0]*np.shape(r1)[0])))
        a1 = r1[np.triu_indices(np.shape(r1)[0])]
        random.seed(SEED)
        a2 = np.asarray(random.sample(list(r2[np.triu_indices(np.shape(r2)[0])]),int(0.01*np.shape(r2)[0]*np.shape(r2)[0])))
        a2 = r2[np.triu_indices(np.shape(r1)[0])]


        return(pearsonr(a1,a2)[0])


        
    def getLambdas(self):
        R"""
        Calculates the Lagrange multipliers of each selected interaction and returns the matrix containing the energy values for the optimization step.
        """
        self.phi_exp = self.values
        self.phi_sim = self.Pi/self.NFrames
        gij = self.phi_exp - self.phi_sim
        

        Pi2_mean = np.outer(self.phi_sim,self.phi_sim)

        PiPj_mean = self.PiPj/self.NFrames

        Bij = PiPj_mean - Pi2_mean
        
        invBij = sc.linalg.pinvh(Bij)

        lambdas = np.matmul(invBij, gij)

        
        lamb_matrix = sc.sparse.csr_matrix((lambdas,(self.rows,self.cols)), shape=(self.expHiC.shape[0],self.expHiC.shape[0]))
        
        self.error = (np.sum(np.absolute(gij)))/(np.sum(self.phi_exp))
        
        return(lamb_matrix)

class CustomMiChroMTraining:
    R"""
    The :class:`~.CustomMiChroMTraining` class performs the parameters training employing MiChroM (Minimal Chromatin Model) energy function. 
    
    Details about the methodology are decribed in "Di Pierro, Michele, et al. "Transferable model for chromosome architecture." Proceedings of the National Academy of Sciences 113.43 (2016): 12168-12173."
    
    
    The :class:`~.CustomMiChroMTraining` class receive a Hi-C matrix (text file) as input. The parameters :math:`\mu` (mi) and rc are part of the probability of crosslink function :math:`f(r_{i,j}) = \frac{1}{2}\left( 1 + tanh\left[\mu(r_c - r_{i,j}\right] \right)`, where :math:`r_{i,j}` is the spatial distance between loci (beads) *i* and *j*.
    
    :class:`~.CustomMiChroMTraining` optimizes the type-to-type (Types) and the Ideal Chromosome (IC) potential parameters separately. 
    
    Args:
        ChromSeq (file, required):
           Chromatin sequence of types file. The first column should contain the locus index. The second column should have the locus type annotation. A template of the chromatin sequence of types file can be found at the `Nucleome Data Bank (NDB) <https://ndb.rice.edu/static/text/chr10_beads.txt>`_.
        TypesTable (file, required):
                A txt/TSV/CSV file containing the upper triangular matrix of the type-to-type interactions. (Default value: :code:`None`).
        mu (float, required):
            Parameter in the probability of crosslink function (Default value = 3.22, for human chromosomes in interphase).
        rc (float, required):
            Parameter in the probability of crosslink function, :math:`f(rc) = 0.5` (Default value = 1.78, for human chromosomes in interphase).
        cutoff (float, optional):
            Cutoff value for reducing the noise in the original data. Values lower than the **cutoff** are considered :math:`0.0`.
        IClist (file, required for Ideal Chromosome training):
            A one-column text file containing the energy interaction values for loci *i* and *j* separated by a genomic distance :math:`d`. The list should be at least of the size :math:`dend-dinit`. (Default value: :code:`None`).
        dinit (int, required):
            The first neighbor in sequence separation (Genomic Distance) to be considered in the Ideal Chromosome potential for training. (Default value = 3).
        dend (int, required):
            The last neighbor in sequence separation (Genomic Distance) to be considered in the Ideal Chromosome potential for training. (Default value = 200).
    """
   
    def __init__(self, ChromSeq="chr_beads.txt", TypesTable=None, mu=3.22, rc=1.78, cutoff=0.0, IClist=None, dinit=3, dend=200): 
        self.ChromSeq = self.get_chrom_seq(ChromSeq)
        self.size = len(self.ChromSeq)
        self.P=np.zeros((self.size,self.size))
        self.Pold=np.zeros((self.size,self.size))
        self.r_cut = rc 
        self.mu  = mu
        
        tab = pd.read_csv(TypesTable, sep=None, engine='python')
        self.header_types = list(tab.columns.values) 
        self.diff_types = set(self.ChromSeq)

        if not self.diff_types.issubset(set(self.header_types)):
            errorlist = []
            for i in self.diff_types:
                if not (i in set(self.header_types)):
                    errorlist.append(i)
            raise ValueError("Types: {} are not present in TypesTables: {}\n".format(errorlist, self.header_types))

        self.lambdas_old = np.triu(tab.values) + np.triu(tab.values, k=1).T

        self.n_types = len(self.diff_types)
        self.n_inter = int(self.n_types*(self.n_types-1)/2 + self.n_types)
        self.Pold_type = np.zeros((self.n_types, self.n_types))
        self.PiPj_type = np.zeros((self.n_inter,self.n_inter))
        self.Nframes = 0 
        
        self.PiPj_IC = np.zeros((dend-dinit,dend-dinit))
        self.dinit = dinit
        self.dend = dend
        self.cutoff = cutoff

        if not IClist == None:
            try:
                f = open(str(IClist),"r")
                self.IClist = IClist
            except IOError:
                print("Error in opening the file containing the Ideal Chromosome interactions!")

    def get_chrom_seq(self, filename):
        R"""Reads the chromatin sequence as letters of the types/compartments.
        
        Args:

            filename (file, required):
                Chromatin sequence of types file. The first column should contain the locus index. The second column should have the locus type annotation. A template of the chromatin sequence of types file can be found at the `Nucleome Data Bank (NDB) <https://ndb.rice.edu/static/text/chr10_beads.txt>`_.
                
        Returns:
            :math:`(N,1)` :class:`numpy.ndarray`:
                Returns an array of the sequence of chromatin types.

        """
        my_list = []
        af = open(filename,'r')
        pos = af.read().splitlines()
        for t in range(len(pos)):
            pos[t] = pos[t].split()
            my_list.append(pos[t][1])

        return np.array(my_list)

   
    def prob_calculation_IC(self, state):
        R"""
        Calculates the contact probability matrix and the cross term of the Hessian for the Ideal Chromosome optimization.
        """

        dmax = self.dend - self.dinit

        self.Pold += self.P
        self.P = 0.5*(1.0 + np.tanh(self.mu*(self.r_cut - distance.cdist(state,state, 'euclidean'))))
        self.P[self.P<self.cutoff] = 0.0
        
        Pi = np.array([])
        for i in range(dmax):
             Pi = np.append(Pi, np.mean(np.diagonal(self.P, offset=(i+self.dinit))))
        
        PiPj = np.outer(Pi, Pi)
        self.PiPj_IC += PiPj
        self.Nframes += 1 
        
    def calc_phi_sim_IC(self):
        R"""
        Calculates the contact probability as a function of the genomic distance from simulations for the Ideal Chromosome optimization.
        """
        dmax = self.dend - self.dinit
        phi = np.zeros(dmax)
        Pmean = self.Pold/self.Nframes
        for i in range(dmax):
             phi[i] =  np.mean(np.diagonal(Pmean, offset=(i+self.dinit)))
        return phi
    
    def get_PiPj_sim_IC(self):
        R"""
        Normalizes the cross term of the Hessian by the number of frames in the simulation for the Ideal Chromosome optimization.
        """
        return self.PiPj_IC/self.Nframes


    def normalize_matrix(self, matrix):
        R"""
        Normalize the matrix for simulation optimization. Here the first neighbor should have the probability of contact P=1.0.
        """
        matrix = np.nan_to_num(matrix, nan=0, posinf=0, neginf=0)
        np.fill_diagonal(matrix,0.0)

        max_values = np.amax(np.triu(matrix), axis=1)
        
        # To avoid division by zero, replace zeros with ones
        max_values[max_values == 0] = 0.0000001
        
        normalized_matrix = np.triu(matrix) / max_values[:, np.newaxis]
        # return normalized_matrix
        matrix= normalized_matrix + np.triu(normalized_matrix,k=1).T
        np.fill_diagonal(matrix,1.0)

        return matrix

    def get_HiC_exp(self, HiC, centerRemove=False, centrange=[0,0], norm=False, cutoff_low=0.0, cutoff_high=1.0, KR=False, neighbors=0):
        R"""
        Receives the experimental Hi-C map (Full dense matrix) in a text format and performs the data normalization from Hi-C frequency/counts/reads to probability.
        
        Args:
            HiC (file, required):
                Experimental Hi-C map (Full dense matrix) in a text format.
            centerRemove (bool, optional):
                Whether to set the contact probability of the centromeric region to zero. (Default value: :code:`False`).
            centrange (list, required if **centerRemove** = :code:`True`)):
                Range of the centromeric region, *i.e.*, :code:`centrange=[i,j]`, where *i* and *j*  are the initial and final beads in the centromere. (Default value = :code:`[0,0]`).
            cutoff (float, optional):
                Cutoff value for reducing the noise in the original data. Values lower than the **cutoff** are considered :math:`0.0`.
        """

        # get the file extension
        _, file_extension = os.path.splitext(HiC)
        if file_extension == '.npy':
            # use np.load if the file is a .npy file
            allmap = np.load(HiC)
        else:
            allmap = np.loadtxt(HiC)

        if KR==True:
            allmap = self.knight_ruiz_balance(allmap)

        if norm==True:
            r=self.normalize_matrix(allmap)

            for i in range(len(r)-1):
                maxElem = r[i][i+1]
                if (maxElem != np.max(r[i])):
                    for j in range(len(r[i])):
                        if maxElem != 0.0:
                            r[i][j] = float(r[i][j] / maxElem)
                        else:
                            r[i][j] = 0.0 
                        if r[i][j] > 1.0:
                            r[i][j] = np.mean(np.diag(r,k=i))

            rd = np.transpose(r) 
            self.expHiC = r+rd + np.diag(np.ones(len(r)))
        else:
            self.expHiC = allmap
        
        if (centerRemove):
            centrome = range(centrange[0],centrange[1])
            self.expHiC[centrome,:] = 0.0
            self.expHiC[:,centrome] = 0.0
        
        #remove noise by cutoff 

        if cutoff_low>0.0:
            self.expHiC[self.expHiC<cutoff_low] = 0.0
        
        if cutoff_high<1.0:
            self.expHiC[self.expHiC>cutoff_high] = 0.0

        # Remove the number of Neighbors to optimize.
        M=self.expHiC
        neighbor_mask = np.abs(np.subtract.outer(np.arange(len(M)), np.arange(len(M)))) <= neighbors
        M[neighbor_mask] = 0.0
        self.expHiC = M

        self.mask = self.expHiC == 0.0

        self.phi_exp = self.expHiC

    def calc_phi_exp_IC(self):
        R"""
        Calculates the contact probability as a function of the genomic distance from the experimental Hi-C for the Ideal Chromosome optimization.
        """
        dmax = self.dend - self.dinit
        phi = np.zeros(dmax)
        for i in range(dmax):
             phi[i] =  np.mean(np.diagonal(self.expHiC, offset=(i+self.dinit)))
        return phi
    
    def get_lambdas_IC(self, exp_map='file.dense', damp=3*10**-7, write_error=True):
        R"""
        Calculates the Lagrange multipliers for the Ideal Chromosome optimization and returns a array containing the energy values for the IC optimization step.
        Args:
            exp_map (file, required):
                The experimental Hi-C map with the .dense file. (Default value: :code:`file.dense`).
            damp (float):
                The learning parameter for the new lambda. (Default value = :math:`3*10**-7`).
            dmax (float):
                The maximum distance in the sequence separation (Genomic Distance) to be considered for the convergence of the potential interations. (Default value = 200).    
                The learning parameter for the new lambda. (Default value = :math:`3*10**-7`).
            write_error (boolean):
                Flag to write the tolerance and Pearson's correlation values. (Default value: :code:`True`). 
        """    
        
        dmax = self.dend - self.dinit

        self.get_HiC_exp(exp_map)
        
        phi_exp = self.calc_phi_exp_IC()
        
        phi_sim = self.calc_phi_sim_IC()
        
        g = -phi_sim + phi_exp   # *1/beta = 1     
    
        B = np.zeros((dmax,dmax))
        PiPj_mean = self.get_PiPj_sim_IC()

        for i, j in itertools.product(range(dmax),range(dmax)):
            B[i,j] = PiPj_mean[i,j] - (phi_sim[i]*phi_sim[j])
         
        invB = sc.linalg.pinv(B)

        self.lambdas_new = np.dot(invB,g)
        self.lambdas_old = np.genfromtxt(str(self.IClist))
        
        lambdas_final = self.lambdas_old[:dmax] - damp*self.lambdas_new

        if write_error:
            self.tolerance = np.sum(np.absolute(g))/np.sum(phi_exp)
            self.pearson = self.get_Pearson()
                                            
            with open('tolerance_and_pearson_IC','a') as tf:
                tf.write("Tolerance: %f  Pearson's Correlation: %f\n" % (self.tolerance, self.pearson))
        
        return(lambdas_final)
    
    def prob_calculation_types(self, state):
        R"""
        Calculates the contact probability matrix and the cross term of the Hessian for the type-to-type interactions optimization.
        """    
        PiPj = np.zeros((self.n_types,self.n_types))
        n = int(self.n_types)
        p_instant = np.zeros((n,n))
        
        just = {}
        ind = np.triu_indices(n)
        
        for tt in self.header_types:
            just[tt] = ([i for i, e in enumerate(self.ChromSeq) if e == tt])

        self.Pold += self.P       
        
        self.P = 0.5*(1.0 + np.tanh(self.mu*(self.r_cut - distance.cdist(state,state, 'euclidean'))))
        self.P[self.P<self.cutoff] = 0.0
        
        vec = []
        for pcount,q in enumerate(itertools.combinations_with_replacement(just.keys(), r=2)):
            p_instant[ind[0][pcount], ind[1][pcount]] = np.average(self.P[np.ix_(just[q[0]], just[q[1]])])
            vec.append(p_instant[ind[0][pcount], ind[1][pcount]])
        vec = np.array(vec)

        PiPj = np.outer(vec,vec)
        
        self.Pold_type += p_instant 
        self.PiPj_type += PiPj
        self.Nframes += 1  
    
    def calc_phi_exp_types(self):
        R"""
        Calculates the average of the contact probability for each chromatin type (compartment annotation) from the experimental Hi-C for the Types optimization.
        """
        n = int(self.n_types)
        phi = np.zeros((n,n))
        just = {}
        ind = np.triu_indices(n)
        
        for tt in self.header_types:
            just[tt] = ([i for i, e in enumerate(self.ChromSeq) if e == tt])

        for pcount,q in enumerate(itertools.combinations_with_replacement(just.keys(), r=2)):
            nt=0
            for i, j in itertools.product(just[q[0]],just[q[1]]):
                phi[ind[0][pcount], ind[1][pcount]] += self.expHiC[i,j]
                nt += 1
            phi[ind[0][pcount], ind[1][pcount]] = phi[ind[0][pcount], ind[1][pcount]]/nt

        return phi
    
    
    def calc_phi_sim_types(self):
        R"""
        Calculates the average of the contact probability for each chromatin type (compartment annotation) from simulation for the Types optimization.
        """
        return self.Pold_type/self.Nframes
    
    def get_PiPj_sim_types(self):
        R"""
        Normalizes the cross term of the Hessian by the number of frames in the simulation for the Types optimization.
        """
        return self.PiPj_type/self.Nframes
    
    def get_HiC_sim(self):
        R"""
        Calculates the *in silico* Hi-C map (Full dense matrix).
        """
        return self.Pold/self.Nframes
    
    def get_Pearson(self):
        R"""
        Calculates the Pearson's Correlation between the experimental Hi-C used as a reference for the training and the *in silico* Hi-C obtained from the optimization step.
        """
        r1 = self.get_HiC_sim()
        r2 = self.expHiC

        r1[np.isinf(r1)]= 0.0
        r1[np.isnan(r1)]= 0.0
        r1[r1 <= 0.001]= 0.0
        r2[np.isinf(r2)]= 0.0
        r2[np.isnan(r2)]= 0.0
        r2[r2<=0.001] = 0.0

        np.fill_diagonal(r1,0.0)
        np.fill_diagonal(r2,0.0)


        SEED = 100
        random.seed(SEED)
        a1 = np.asarray(random.sample(list(r1[np.triu_indices(np.shape(r1)[0])]),int(0.1*np.shape(r1)[0]*np.shape(r1)[0])))
        a1 = r1[np.triu_indices(np.shape(r1)[0])]
        random.seed(SEED)
        a2 = np.asarray(random.sample(list(r2[np.triu_indices(np.shape(r2)[0])]),int(0.1*np.shape(r2)[0]*np.shape(r2)[0])))
        a2 = r2[np.triu_indices(np.shape(r1)[0])]


        return(pearsonr(a1,a2)[0])
        
    def get_lambdas_types(self, exp_map, damp=5*10**-7, write_error=True):
        R"""
        Calculates the Lagrange multipliers of each type-to-type interaction and returns the matrix containing the energy values for the optimization step.
        """
        self.get_HiC_exp(exp_map)
        
        phi_exp = self.calc_phi_exp_types()
        
        phi_sim = self.calc_phi_sim_types()
        
        g = -phi_sim + phi_exp

        PiPj_mean = self.get_PiPj_sim_types()
        
        ind = np.triu_indices(self.n_types)
        phi_sim_linear = []

        for pcount,q in enumerate(itertools.combinations_with_replacement(range(self.n_types), r=2)):
            phi_sim_linear.append(phi_sim[ind[0][pcount], ind[1][pcount]])
           
        phi_sim_linear = np.array(phi_sim_linear)

        Pi2_mean = np.outer(phi_sim_linear,phi_sim_linear)

        B = PiPj_mean - Pi2_mean
    
        invB = sc.linalg.pinv(B)

        if write_error:
            tolerance = np.sum(np.absolute(g))/np.sum(phi_exp)
            pearson = self.get_Pearson()

            with open('tolerance_and_pearson_types','a') as tf:
                    tf.write("Tolerance: %f  Pearson's Correlation: %f\n" % (tolerance, pearson))   
        
        g_vec = []
        for pcount,q in enumerate(itertools.combinations_with_replacement(range(self.n_types), r=2)):
            g_vec.append(g[ind[0][pcount], ind[1][pcount]])
        g_vec = np.array(g_vec)
        
        lambdas = np.matmul(invB, g_vec)
        
        self.lambdas_new = np.zeros((self.n_types,self.n_types))
        
        inds = np.triu_indices_from(self.lambdas_new)
        self.lambdas_new[inds] = lambdas
        self.lambdas_new[(inds[1], inds[0])] = lambdas 
        
        lambdas_final = self.lambdas_old  - damp*self.lambdas_new

        return(pd.DataFrame(lambdas_final,columns=self.header_types))
