import numpy as np

from param import WB_MAX, WB_MIN

## homeo_vars = ['ENERGY', 'COMFORT']#optimal values

## ext_stimuli params
## increasing func params
## satisfaction time params
## satuation level params

env_log_name = 'env.txt'

class IntEnv():
    ## TODO: param processing
    hv_optims = np.array([100,100])
    act_levels = np.array([1,1])##
    coef_emo_motiv = np.array(np.ones(4,2))##
    motiv_weights = np.array([0,0])##

    wb_max = WB_MAX
    wb_min = WB_MIN
    
    def __init__(self):
        self._file = open(env_log_name, 'a')
    
    @staticmethod
    def _save_vars(file, var, cnt, var_type):
        np.savetxt(fname=file, X=var, fmt='%.3f', delimiter=',', newline='\n', 
            header='Step %5d'%(cnt), footer=var_type)
    
    def _homeo_vars(self):
        ## TODO: bounds (saturation level)
        self._save_vars(self._file, self._hvs, self.cnt, 'HomeoVar Values')
        
        return self._hvs
    
    def _drives(self):
        ## TODO: bounds (saturation level)
        return hv_optims - self._homeo_vars()
    
    def _motivations(self):
        drives = self._drives()
        motivs = np.where(drives < act_levels, 0, drives)
        
        self._save_vars(self._file, motivs, self.cnt, 'Motivation Values')
        
        return motivs
    
    def step(self, ext_state, cnt):
        self.cnt = cnt
        self.ext_state = ext_state
        
        motivs = self._motivations()

        int_state = np.argmax(np.dot(coef_emo_motiv, motivs))
        int_state = np.random.choice(int_state.reshape(-1))## TODO: if more than one emotions are dominant
        wb = wb_max - np.sum(motiv_weights * motivs)
        
        return int_state, max([wb, wb_min])