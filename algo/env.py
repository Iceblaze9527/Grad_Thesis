import sys 
sys.path.append("..") 

import numpy as np

from param import INTENV_PAR

np.random.seed(INTENV_PAR['rand_seed'])

class IntEnv():
    wb_min = INTENV_PAR['wb_limit'][0]
    wb_max = INTENV_PAR['wb_limit'][1]
    
    def __init__(self):
        self._hvs = np.random.binomial(n = INTENV_PAR['hv_maxs'] - INTENV_PAR['hv_mins'], p = INTENV_PAR['init_expct']) + INTENV_PAR['hv_mins']
        self.wb = (self._get_wb()).copy()
        self.file = open(INTENV_PAR['logfile'], 'a')
        
        self._save_vars = lambda cnt: np.savetxt(fname=self.file, X=self._hvs, fmt='%.3f', 
            delimiter='\n', newline='\n', header='Step %3d'%(cnt))
        
        print('Homeostatic Variables:', INTENV_PAR['homeo_vars'], file=self.file)
        self._save_vars(0)

    def _update_homeo_vars(self, ext_states):
        hv_news = (self._hvs).copy()
        
        for ext_state, gain in enumerate(INTENV_PAR['coef_hv_ext_st'].T):
            if (ext_states >> ext_state) % 2 == 1:
                hv_news += gain.reshape(-1)
        
        dec_vals = [decay(hv_old) for decay, hv_old in zip(INTENV_PAR['step_decays'], self._hvs)]
        hv_news = np.where(hv_news - self._hvs, hv_news, self._hvs - dec_vals)
        
        hv_news = np.clip(hv_news, INTENV_PAR['hv_mins'], INTENV_PAR['hv_maxs'])
        
        self._hvs = (hv_news).copy()
    
    def _get_wb(self):
        drives = INTENV_PAR['hv_maxs'] - self._hvs
        motivs = np.where(drives < INTENV_PAR['act_levels'], 0, drives)
        wb = IntEnv.wb_max - np.sum(INTENV_PAR['motiv_weights'] * motivs)
        wb = max([wb, IntEnv.wb_min])

        return wb

    def step(self, ext_states, cnt):
        self._update_homeo_vars(ext_states)
        
        wb = self._get_wb()
        reward = wb - self.wb
        self.wb = wb.copy()

        self._save_vars(cnt)
        
        return reward