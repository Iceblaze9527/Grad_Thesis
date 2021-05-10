import numpy as np

from param import INTENV_PAR, INTENV_LOG, RAND_SEED

np.random.seed(RAND_SEED)

class IntEnv():
    wb_min = INTENV_PAR['wb_limit'][0]
    wb_max = INTENV_PAR['wb_limit'][1]
    
    def __init__(self):
        self._hvs = np.random.binomial(n = INTENV_PAR['hv_maxs'] - INTENV_PAR['hv_mins'], p = 0.5) + INTENV_PAR['hv_mins']
        self.file = open(INTENV_LOG, 'a')
        
        self._save_vars = lambda var, cnt, var_type: np.savetxt(fname=self.file, X=var, fmt='%.3f', 
            delimiter=',', newline='\n', header='Step %5d: %s'%(cnt, var_type))
        
        print('Homeostatic Variables:', INTENV_PAR['homeo_vars'], file=self.file)

    def _update_homeo_vars(self, ext_states):
        hv_news = self._hvs
        for ext_state, gain in enumerate(INTENV_PAR['coef_hv_ext_st'].T):
            if (ext_states >> ext_state) % 2 == 1:
                hv_news += gain.reshape(-1)
        
        dec_vals = [decay(hv_old) for decay, hv_old in zip(INTENV_PAR['step_decays'], self._hvs)]
        hv_news = np.where(hv_news - self._hvs, hv_news, self._hvs - dec_vals)
        hv_news = np.clip(hv_news, INTENV_PAR['hv_mins'], INTENV_PAR['hv_maxs'])
        self._hvs = hv_news
    
    def _motivations(self, ext_states):
        self._update_homeo_vars(ext_states)
        drives = INTENV_PAR['hv_maxs'] - self._hvs
        motivs = np.where(drives < INTENV_PAR['act_levels'], 0, drives)

        return motivs

    def step(self, ext_states, cnt):
        motivs = self._motivations(ext_states)
        
        wb = IntEnv.wb_max - np.sum(INTENV_PAR['motiv_weights'] * motivs)
        wb = max([wb, IntEnv.wb_min])

        self._save_vars(self._hvs, cnt, 'Homeostatic Values')
        self._save_vars(motivs, cnt, 'Motivation Values')
        
        return wb