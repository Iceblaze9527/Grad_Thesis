import numpy as np

from param import ext_state_vars, ENV_LOG_NAME, WB_MAX, WB_MIN, RAND_SEED

np.random.seed(RAND_SEED)

linear_decay = lambda hv_old: 2

## TODO: PARAM VALS & CONSTRAINTS!!!
## max(c_hs[hv, :]) > decay(hv) (there is always a means to increase it)
## estimate theta: 
## wb = wb_max - sum(i)(theta[i] * motiv[i]) \approx wb_max - sum(i)(theta[i] * (hv_max[i] - hv_min[i]))
## estimate reward:
## reward \approx sum(i)(theta[i] * (hv[i][t+1] - hv[i][t]))
## estimate q-val:
## delta = alpha(reward + gamma * approx_avr(q(s[t+1], a[:])) - q(s[t], a[t]))

_homeo_vars = ['ENERGY', 'COMFORT']
_hv_maxs = np.array([100,100])
_hv_mins = np.array([0,0])

_coef_hv_ext_st = np.array([[6,0],[4,-6]])## num_of_hv * num_of_s_ext
_step_decays = [linear_decay, linear_decay]## a func list, return hv_func[cnt] - hv_func[cnt - 1] based on hv_func[cnt - 1]

_act_levels = np.array([5,5])

_coef_emo_motiv = np.array([[-0.2,0.3], [0.7,0], [-0.2,0.2], [0.2,0.1]])
_motiv_weights = np.array([0.5,0.5])

class IntEnv():
    wb_max = WB_MAX
    wb_min = WB_MIN
    
    def __init__(self):
        self._hvs = np.random.binomial(n = _hv_maxs - _hv_mins, p = 0.5) + _hv_mins ## random start, close to the middle point
        self.file = open(ENV_LOG_NAME, 'a')
        
        self._save_vars = lambda var, cnt, var_type: np.savetxt(fname=self.file, X=var, fmt='%.3f', 
            delimiter=',', newline='\n', header='Step %5d: %s'%(cnt, var_type))
        
        print('Homeostatic Variables:', _homeo_vars, file=self.file)

    def _update_homeo_vars(self, ext_states):
        hv_news = self._hvs
        for ext_state in range(len(ext_state_vars)):
            if ext_states >> ext_state == 1:
                hv_news += _coef_hv_ext_st[:, ext_state].reshape(-1)
        
        dec_vals = [decay(hv_old) for decay, hv_old in zip(_step_decays, self._hvs)]
        hv_news = np.where(hv_news - self._hvs, hv_news, self._hvs - dec_vals)
        hv_news = np.clip(hv_news, _hv_mins, _hv_maxs)
        self._hvs = hv_news
    
    def _motivations(self, ext_states):
        self._update_homeo_vars(ext_states)
        drives = _hv_maxs - self._hvs
        motivs = np.where(drives < _act_levels, 0, drives)

        return motivs

    def step(self, ext_states, cnt):
        motivs = self._motivations(ext_states)

        int_state = np.argmax(np.dot(_coef_emo_motiv, motivs)).reshape(-1)
        ## TODO: if more than one emotions are dominant
        int_state = np.random.choice(int_state)
        wb = IntEnv.wb_max - np.sum(_motiv_weights * motivs)
        wb = max([wb, IntEnv.wb_min])

        self._save_vars(self._hvs, cnt, 'Homeostatic Values')
        self._save_vars(motivs, cnt, 'Motivation Values')
        
        return int_state, wb