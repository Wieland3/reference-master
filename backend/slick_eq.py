import plugin
import optimizer
import time
import constants


class SlickEq(plugin.Plugin):

    def __init__(self, plugin_path):
        super().__init__(plugin_path)
        self.plugin.low_shape = "Bell"
        self.plugin.high_shape = "Shelf"
        self.plugin.hp_freq_hz = constants.HP_FREQ
        self.plugin.eq_sat = True
        self.plugin.auto_gain = False


    def set_params(self, values):
        self.plugin.low_gain_db = values[0]  # -18.0 to 18.0
        self.plugin.low_freq_hz = values[1]  # 30 to 1000
        self.plugin.mid_gain_db = values[2]  # -18.0 to 18.0
        self.plugin.mid_freq_hz = values[3]  # 100 to 10000
        self.plugin.high_gain_db = values[4]  # -18.0 to 18.0
        self.plugin.high_freq_hz = values[5]  # 500 to 40000


    def find_set_settings(self, bounds, raw_mono, sr_raw, power_ref, maxiter=constants.NUM_ITERATIONS, verbose=True):
        start_time = time.time()
        params = optimizer.direct_optimization(self, bounds, raw_mono, sr_raw, power_ref, maxiter=maxiter)
        if verbose:
            print("Mininm distance", params.fun)
            print("--- %s seconds ---" % (time.time() - start_time))
        params = [round(x, 1) for x in params.x]
        self.set_params(params)
        return params

