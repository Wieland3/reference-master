import plugin
import optimizer
import time
import constants


class NovaEq(plugin.Plugin):

    def __init__(self, plugin_path, band_4_type="High S"):
        super().__init__(plugin_path)
        self.plugin.eq_auto_gain = False
        self.plugin.band_1_active = True
        self.plugin.band_2_active = True
        self.plugin.band_3_active = True
        self.plugin.band_4_active = True
        self.plugin.band_1_type = "Bell"
        self.plugin.band_2_type = "Bell"
        self.plugin.band_3_type = "Bell"
        self.plugin.band_4_type = band_4_type

    def set_params(self, values):
        self.plugin.band_1_gain_db = values[0]  # -18.0 to 18.0
        self.plugin.band_1_q = values[1]  # 0.1 to 6.0
        self.plugin.band_1_frequency_hz = values[2]  # 10.0 to 40000.0
        self.plugin.band_2_gain_db = values[3]  # -18.0 to 18.0
        self.plugin.band_2_q = values[4]  # 0.1 to 6.0
        self.plugin.band_2_frequency_hz = values[5]  # 10.0 to 40000.0
        self.plugin.band_3_gain_db = values[6]  # -18.0 to 18.0
        self.plugin.band_3_q = values[7]  # 0.1 to 6.0
        self.plugin.band_3_frequency_hz = values[8]  # 10.0 to 40000.0
        self.plugin.band_4_gain_db = values[9]  # -18.0 to 18.0
        self.plugin.band_4_q = values[10]  # 0.1 to 6.0
        self.plugin.band_4_frequency_hz = values[11]  # 10.0 to 40000.0
        self.plugin.hp_active = True
        self.plugin.hp_frequency_hz = constants.HP_FREQ

    def find_set_settings(self, bounds, raw_mono, sr_raw, power_ref, maxiter=constants.NUM_ITERATIONS, verbose=True, mode="annealing"):
        start_time = time.time()
        if mode == "direct":
            print("Direct optimization")
            params = optimizer.direct_optimization(self, bounds, raw_mono, sr_raw, power_ref, maxiter=maxiter)
        elif mode == "annealing":
            print("Annealing optimization")
            params = optimizer.dual_annealing_optimization(self, bounds, raw_mono, sr_raw, power_ref, maxiter=maxiter)
        if verbose:
            print("Mininm distance", params.fun)
            print("--- %s seconds ---" % (time.time() - start_time))
        params = [round(x, 1) for x in params.x]
        self.set_params(params)
        return params

