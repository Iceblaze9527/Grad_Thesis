import numpy as np

from param import ENV_LOG_NAME, WB_MAX, WB_MIN

# num_ext_states = np.floor(np.log2(self.ext_states)).astype(np.int) + 1

linear_decay = lambda delta: delta

class IntEnv():
    homeo_vars = ['ENERGY', 'COMFORT']
    hv_maxs = np.array([100,100])
    hv_mins = np.array([0,0])
    
    coef_hv_ext = np.array([[6,0],[0,-6]])## num_of_hv * num_of_s_ext
    decay_funcs = [linear_decay, linear_decay]## a func list, decay_func_of_hv_vars

    act_levels = np.array([5,5])
    
    coef_emo_motiv = np.array([[-0.2,0.3], [0.7,0], [-0.2,0.7], [0.2,0.1]])
    motiv_weights = np.array([0,0])##

    wb_max = WB_MAX
    wb_min = WB_MIN
    
    def __init__(self):
        self._hvs = np.random.binomial(n=hv_maxs-hv_mins, p=0.5)## random start, close to the middle
        self._file = open(ENV_LOG_NAME, 'a')
        self._decay_funcs = decay_funcs
    
    @staticmethod
    def _save_vars(file, var, cnt, var_type):
        np.savetxt(fname=file, X=var, fmt='%.3f', delimiter=',', newline='\n', 
            header='Step %5d'%(cnt), footer=var_type)

    def _homeo_vars(self):
        for ext_state in range(2):## num_ext_states
            if self.ext_states >> ext_state == 1:## if ext_stimuli enabled
                self._hvs[ext_state] += coef_hv_ext[:, ext_state].reshape(-1)
            else:## hv_vars!= ext_state, cnt != time_step
                self._hvs[ext_state] -= (self._decay_funcs[ext_state])(self.cnt, self._hvs[ext_state])
        self._hvs = np.clip(self._hvs, hv_mins, hv_maxs)
        
        self._save_vars(self._file, self._hvs, self.cnt, 'Homeostatic Values')
        
        return self._hvs
    
    def _drives(self):
        return hv_maxs - self._homeo_vars()# saturation level
    
    def _motivations(self):
        drives = self._drives()
        motivs = np.where(drives < act_levels, 0, drives)
        
        self._save_vars(self._file, motivs, self.cnt, 'Motivation Values')
        
        return motivs
    
    def step(self, ext_states, cnt):
        self.cnt = cnt
        self.ext_states = ext_states
        
        motivs = self._motivations()

        int_state = np.argmax(np.dot(coef_emo_motiv, motivs)).reshape(-1)
        int_state = np.random.choice(int_state)## TODO: if more than one emotions are dominant
        wb = wb_max - np.sum(motiv_weights * motivs)
        
        return int_state, max([wb, wb_min])