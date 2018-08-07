
import numpy as np
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
import pickle


FS_HZ = 1000.0


class Profile:

    def _plot_df(self, df, plot_title='pandas.DataFrame', filename=None):
        
        labels = list(df.columns.values)
        num_plots = df.shape[1] - 1   

        plt.figure(figsize=(6.5, 9), clear=True)
     
        for i in range(num_plots):

            plt.subplot(num_plots, 1, i + 1)
            plt.plot(df.iloc[:, 0].get_values(), df.iloc[:, i + 1].get_values(), linestyle='solid', linewidth=0.5, color=(0.0, 0.0, 0.0))
            plt.grid(linestyle=':', linewidth=1, color=(0.75, 0.75, 0.75))
            plt.ylabel(labels[i + 1])

            if i == 0:
                plt.title(plot_title)
            if i == num_plots - 1:
                plt.xlabel(labels[0])
        
        plt.tight_layout()

        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)

    def _gen_deriv(self, data, fs, init=0):

        tablen = len(data)
        deriv_tab = np.empty(tablen)
        last = np.float(init)

        i = 0
        for sample in data:
            deriv_tab[i] = np.float((sample - last) * fs)
            last = np.float(sample)
            i += 1

        return deriv_tab

    def _gen_intgrl(self, data, fs, init=0):

        tablen = len(data)
        intgrl_tab = np.empty(tablen)
        intgrl_val = np.float(init)

        i = 0
        for sample in data:
            intgrl_val += np.float(sample / fs)
            intgrl_tab[i] = intgrl_val
            i += 1

        return intgrl_tab

    def save(self, filename):
        with open(filename, 'wb') as f:  
            pickle.dump((self.settings, self.stats, self.profile), f)    

    def load(self, filename):
        with open(filename, 'rb') as f:
            (self.settings, self.stats, self.profile) = pickle.load(f)    

    def html(self, filename):
        with open(filename, 'w') as f:
            print(self.profile.to_html(), file=f)

    def csv(self, filename):
        with open(filename, 'w') as f:
            print(self.profile.to_csv(), file=f)

    def xlsx(self, filename):
        writer = pd.ExcelWriter(filename)
        self.profile.to_excel(writer,'Sheet1')
        writer.save()

    def print(self, filename=None):

        profile_str = "\n[i] Profile Data Table\n\n"
        profile_str += self.profile.to_string() + '\n'     

        settings_str = "\n[i] Profile Settings\n\n"
        for key, value in self.settings.items():
            settings_str += key + ': ' + str(value) + '\n'
    
        stats_str = "\n[i] Profile Stats\n\n"
        for key, value in self.stats.items():
            stats_str += key + ': ' + str(value) + '\n'
                
        if filename:
            with open(filename, 'w') as f:
                print(settings_str + stats_str + profile_str, file=f)     
        else:
            print(profile_str + settings_str + stats_str)


class LinearMotion(Profile):

    def __init__(self,
        settings=None,
        fs = 1000,
        max_velocity = 1,
        acc_mode = 'T',
        acc_value = 1,
        acc_smooth = True,
        con_mode = 'T',
        con_value = 1,
        dec_mode = 'T',
        dec_value = 1,
        dec_smooth = True,
        ):

        if settings is None:
            self.settings = {
                'fs': fs,
                'max_velocity': max_velocity,
                'acc_mode': acc_mode,
                'acc_value': acc_value,
                'acc_smooth': acc_smooth,
                'con_mode': con_mode,
                'con_value': con_value,
                'dec_mode': dec_mode,
                'dec_value': dec_value,
                'dec_smooth': dec_smooth,
                }
        else:
            self.settings = settings

    def generate(self):
        (self.profile, self.stats) = self._gen_linpro(self.settings)

    def plot(self, 
        filename=None,
        plot_title='Linear Motion Profile',
        t_label='Time (s)',
        x_label='Distance (m)',
        v_label='Velocity (m/s)',
        a_label='Acceleration (m/s^2)'
        ):

        df = self.profile[['t', 'a', 'v', 'x']]
        df = df.rename(columns={'t': t_label, 'a': a_label, 'v': v_label, 'x': x_label})
        self._plot_df(df, plot_title=plot_title, filename=filename)

    def _gen_x_from_v(self, v, fs, x0=0):
        return self._gen_intgrl(v, fs, x0)

    def _gen_v_from_a(self, a, fs, v0=0):
        return self._gen_intgrl(a, fs, v0)

    def _gen_v_from_x(self, x, fs, x0=0):
        return self._gen_deriv(x, fs, x0)

    def _gen_a_from_v(self, v, fs, v0=0):
        return self._gen_deriv(v, fs, v0)

    def _gen_t_from_v(self, v, fs):
        t = np.arange(len(v), dtype='float')
        t = t / fs
        return t

    def _get_t1_from_v1_and_x1(v1, x1):
        return (2 / v1) * x1

    def _get_t1_from_v1_and_a1(v1, a1):
        return (1 / a1) * v1

    def _gen_acc_from_v_and_t(self, v1, t1, fs=FS_HZ, smooth=True):

        tablen = np.int(t1 * fs)

        if smooth is True:
            v = signal.get_window('hann', tablen * 2)
        else:
            v = signal.get_window('triang', tablen * 2)

        v = v[:tablen]
        v = v * v1
        x = self._gen_x_from_v(v, fs)
        a = self._gen_a_from_v(v, fs)
        t = self._gen_t_from_v(v, fs)

        profile = pd.DataFrame({'t': t, 'x': x, 'v': v, 'a': a})

        return profile

    def _gen_con_from_v_and_t(self, v1, t1, x0, fs=FS_HZ):

        v1 = np.float(v1)
        t1 = np.float(t1)
        tablen = np.int(t1 * fs)

        v = np.empty(tablen, dtype='float')
        v.fill(v1)
        
        x = self._gen_x_from_v(v, fs=fs, x0=x0)
        a = np.zeros(tablen, dtype='float')
        t = self._gen_t_from_v(v, fs)
             
        profile = pd.DataFrame({'t': t, 'x': x, 'v': v, 'a': a})

        return profile

    def _gen_dec_from_v_and_t(self, v1, t1, v0, x0, fs=FS_HZ, smooth=True):

        tablen = np.int(t1 * fs)

        if smooth is True:
            v = signal.get_window('hann', tablen * 2)
        else:
            v = signal.get_window('triang', tablen * 2)

        v = v[tablen:]
        v = v * v1

        x = self._gen_x_from_v(v, fs, x0)
        a = self._gen_a_from_v(v, fs, v0)
        t = self._gen_t_from_v(v, fs)
             
        profile = pd.DataFrame({'t': t, 'x': x, 'v': v, 'a': a})

        return profile

    def _gen_linpro(self, settings):

        fs = settings['fs']
        max_velocity = settings['max_velocity']
        acc_mode = settings['acc_mode']
        acc_value = settings['acc_value']
        con_mode = settings['con_mode']
        con_value = settings['con_value']
        dec_mode = settings['dec_mode']
        dec_value = settings['dec_value']

        if settings['acc_smooth'] is None or settings['acc_smooth'] is False:
            acc_smooth = False
        else:
            acc_smooth = True
        
        if settings['dec_smooth'] is None or settings['dec_smooth'] is False:
            dec_smooth = False
        else:
            dec_smooth = True

        if acc_mode == 'X':
            acc_t1 = self._get_t1_from_v1_and_x1(max_velocity, acc_value)
        elif acc_mode == 'A':
            acc_t1 = self._get_t1_from_v1_and_a1(max_velocity, acc_value)
        elif acc_mode == 'T':
            acc_t1 = acc_value
        else:
            raise ValueError("Acceptable input for acc_mode is 'X', 'T', or 'A'.")    

        if con_mode == 'X':
            con_t1 = self._get_t1_from_v1_and_x1(max_velocity, con_value)
        elif con_mode == 'T':
            con_t1 = con_value
        else:
            raise ValueError("Acceptable input for con_mode is 'X' or 'T'.")

        if dec_mode == 'X':
            dec_t1 = self._get_t1_from_v1_and_x1(max_velocity, dec_value)
        elif dec_mode == 'A':
            dec_t1 = self._get_t1_from_v1_and_a1(max_velocity, dec_value)
        elif dec_mode == 'T':
            dec_t1 = dec_value
        else:
            raise ValueError("Acceptable input for dec_mode is 'X', 'T', or 'A'.")

        acc_profile = self._gen_acc_from_v_and_t(v1=max_velocity, t1=acc_t1, smooth=acc_smooth, fs=fs)
        con_profile = self._gen_con_from_v_and_t(v1=max_velocity, t1=con_t1, x0=acc_profile['x'].iloc[-1], fs=fs)
        dec_profile = self._gen_dec_from_v_and_t(v1=max_velocity, t1=dec_t1, v0=con_profile['v'].iloc[-1], x0=con_profile['x'].iloc[-1], smooth=dec_smooth, fs=fs)
        
        profile = pd.concat([acc_profile, con_profile, dec_profile], ignore_index=True)
        
        t = np.arange(profile['x'].size)
        t = t / fs
        t = pd.Series(t)
        profile['t'] = t

        stats = {
            'acc_size': acc_profile['x'].size,
            'acc_a_max': acc_profile['a'].max(),
            'acc_a_mean': acc_profile['a'].mean(),
            'acc_t': acc_profile['x'].size / fs,
            'acc_x': acc_profile['x'].ptp(),
            'con_size': con_profile['x'].size,
            'con_t': con_profile['x'].size / fs,
            'con_x': con_profile['x'].ptp(),
            'dec_size': dec_profile['x'].size,
            'dec_a_min': dec_profile['a'].min(),
            'dec_a_mean': dec_profile['a'].mean(),
            'dec_t': dec_profile['x'].size / fs,
            'dec_x': dec_profile['x'].ptp(),
            }

        return (profile, stats)


if __name__ == '__main__':

    lm_settings = {
        'fs': 1000.0,
        'max_velocity': 1,
        'acc_mode': 'T',
        'acc_value': 1,
        'acc_smooth': True,
        'con_mode': 'T',
        'con_value': 1,
        'dec_mode': 'T',
        'dec_value': 1,
        'dec_smooth': False,
    }

    lm = LinearMotion(lm_settings)
    lm.generate()
    lm.print()
    lm.plot()
