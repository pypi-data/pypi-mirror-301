#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' 
Display CO_2 concentration based on IoT sensor data.

Provide a configuration file .config with the following information: 
{
	"MQTT_USER": "",
	"MQTT_PASSWD": "",
}

'''

__version__ = '24.10.10'

from tkinter import Tk, Toplevel, Label, Button, Entry, StringVar, OptionMenu, Frame, messagebox, filedialog
from time import localtime
from argparse import ArgumentParser
from mqtt.mqtt import MQTT
from pandas import DataFrame, to_datetime
from matplotlib.pyplot import subplots, show
from urllib.request import urlopen

# color codes for iaq
C_GOOD = 'pale green'
C_MEDIUM = 'yellow'
C_BAD = 'tomato'
C_EXTREME = 'hot pink'

# Just a default list, is later updated via a file on Gitlab.
SENSORS = {
    'B201' : ['iot.fh-muenster.de', 1883,  'sensor/eui-64b708ac988cfeff'],
    'B203' : ['iot.fh-muenster.de', 1883,  'sensor/eui-64b708ad0a60feff'],
    'D250a': ['iot.fh-muenster.de', 1883,  'sensor/eui-64b708bb7658feff'],
    'G182' : ['iot.fh-muenster.de', 1883,  'sensor/eui-64b708ad0e84feff'],
    'VEPO' : ['iot.fh-muenster.de', 1883,  'sensor/24:62:ab:f3:b8:50_HOME'],
    'VEPH' : ['192.168.1.86'      , 32797, 'sensor/24:6f:28:7b:e5:14_HOME'],
    }

class CO2Info(Tk):

    def __init__(self, sensor='B203'):
        super().__init__()
        self.sensor = sensor
        self.title('CO2-Info')
        self.button = Button(self)
        self.button['text'] = '{}: Warte bis zu 60 s.'.format(self.sensor) 
        self.button['command'] = self.show_details
        self.button.pack()
        self.history = []
        self.tk_var_annotate=StringVar()
        self.tk_var_history=StringVar()
        self._init_mqtt()

    def _init_mqtt(self):
        func = self.parse_sensor_data_eui
        if self.sensor in ['VEPO', 'VEPH']:
            func = self.parse_sensor_data_vep
        else:
            func = self.parse_sensor_data_eui
        try:
            server = SENSORS[self.sensor][0]
            port   = SENSORS[self.sensor][1]
            topic  = SENSORS[self.sensor][2]
            self.mqtt_client = MQTT(server,
                                    port,
                                    topic,
                                    func,
                                    username=MQTT_USER,
                                    password=MQTT_PASSWD,
            )
        except Exception as e:
            messagebox.showerror(
                title='Error.',
                message= repr(e)
            )

    def show_details(self):
        tl_window = Toplevel(self)
        # change sensor
        frame_sensor = Frame(tl_window)
        frame_sensor.pack()
        label_sensor = Label(
            frame_sensor,
            text='Sensor wechseln:')
        label_sensor.pack(side='left')
        self.tk_var_sensor = StringVar()
        om_sensor = OptionMenu(
            frame_sensor,
            self.tk_var_sensor,
            *list(SENSORS.keys()),
            command = self.om_sensor_changed)
        om_sensor.pack(side='left')
        # annotate
        frame_annotate = Frame(tl_window)
        frame_annotate.pack()
        label_annotate = Label(
            frame_annotate,
            text='Nächste Messung annotieren:')
        label_annotate.pack(side='left')
        entry_annotate = Entry(
            frame_annotate,
            textvariable=self.tk_var_annotate)
        entry_annotate.pack(side='left')
        # plot
        button_plot = Button(
            tl_window,
            text='Daten plotten.',
            command=self.plot)
        button_plot.pack(fill='x')
        # save
        button_save = Button(
            tl_window,
            text='Daten exportieren.',
            command=self.export)
        button_save.pack(fill='x')
        # view history
        self.label_history = Label(
            tl_window,
            textvariable=self.tk_var_history)
        self.label_history.pack()
        # about
        button_about = Button(
            tl_window,
            text='Info.',
            command=self.about)
        button_about.pack(fill='x')

    def about(self):
        messagebox.showinfo(
            'Version',
            'Version: ' +  __version__ +
            '\nInfo: fh.ms/co2i')

    def om_sensor_changed(self, event):
        self.sensor = self.tk_var_sensor.get()
        try:
            self.mqtt_client.stop()
        except:
            pass
        self._init_mqtt()
        self.tk_var_annotate.set(self.sensor)

    def set_bg_color(self, color):
        self['background']=color
        self.button['background']=color
            
    def get_color_code(self, ppm_co2):
        if ppm_co2 < 800:
            return(C_GOOD)
        elif ppm_co2 < 1000:
            return(C_MEDIUM)
        elif ppm_co2 < 1200:
            return(C_BAD)
        else:
            return(C_EXTREME)

    def get_tendency(self, ppm_co2):
        if len(self.history) < 2:
            return('')
        elif abs(ppm_co2 - self.history[-2][-2])<5:
            return('→')
        elif ppm_co2 < self.history[-2][-2]:
            return('↓')
        else:
            return('↑')
    def parse_sensor_data_eui(self, raw_data):
        data = eval(raw_data.decode())
        self.process_sensor_data(float(data[3]), float(data[2]), float(data[1]))
        
    def parse_sensor_data_vep(self, raw_data):
        self.process_sensor_data(*[float(d) for d in raw_data.decode().split()])

    def parse_sensor_data_sef(self, raw_data):
        data = eval(raw_data.decode())
        self.process_sensor_data(float(data['T2']), float(data['Hum']), float(data['eCO2']))

    def process_sensor_data(self, *args):
        annotation = self.tk_var_annotate.get().replace('\n','')
        self.tk_var_annotate.set('')
        self.history.append([self.timestamp(), *args, annotation])
        self.tk_var_history.set(self.tail_string())
        self.check(args[-1])
        
    def check(self, ppm_co2):
        self.set_bg_color(self.get_color_code(ppm_co2))
        self.button['text'] = '{}: {} ppm {}'.format(self.sensor,
                                                     ppm_co2,
                                                     self.get_tendency(ppm_co2))

    def timestamp(self):
        lc = localtime()
        pattern = '{}-{:02}-{:02}T{:02}:{:02}:{:02}'
        return(pattern.format(lc.tm_year,
                              lc.tm_mon,
                              lc.tm_mday,
                              lc.tm_hour,
                              lc.tm_min,
                              lc.tm_sec))

    def create_dataframe(self):
        '''Create a pandas dataframe from history data.'''
        if len(self.history) > 0:
            columns=('Zeit','Temperatur (°C)','Feuchte (%)', 'CO_2 (ppm)', 'Annotation')
            df = DataFrame(
                 self.history, 
                 columns=columns)
            # convert datetime strings to datetime index
            df.index = to_datetime(df['Zeit'])
            del df['Zeit']
            # replace zeros in co_2 column
            df['CO_2 (ppm)'] = df['CO_2 (ppm)'].replace(0, None).bfill()
            return(df)
        else:
            messagebox.showinfo(
            'Info',
            'Noch keine drei Messwerte vorhanden.\n' +
            'Bitte später noch einmal versuchen.')
            
    def tail_string(self):
        if len(self.history) > 0:         
            df = self.create_dataframe()
            df = df.tail()
            return('Letzte Messwerte:\n' + df.to_string())
        else:
            return('Noch kein Messwert vorhanden.')

    def plot(self):
        '''Plot history data using pandas.'''
        if len(self.history) > 1:
            # plot data with three y axes
            df = self.create_dataframe()
            fig, ax = subplots()
            fig.subplots_adjust(right=0.75)
            twin1 = ax.twinx()
            twin2 = ax.twinx()
            twin2.spines['right'].set_position(('axes', 1.2))
            p1, = ax.plot(df.index, df['Temperatur (°C)'], 'r-', label='Temperatur')
            p2, = twin1.plot(df.index, df['Feuchte (%)'], 'b-', label='Feuchte')
            p3, = twin2.plot(df.index, df['CO_2 (ppm)'], 'g-', label='CO_2')
            ax.set_ylabel('Temperatur (°C)')
            twin1.set_ylabel('Feuchte (%)')
            twin2.set_ylabel('CO_2 (%)')
            ax.legend(handles=[p1, p2, p3])
            # annotations
            annotations = df.loc[df['Annotation'] != '', ['CO_2 (ppm)', 'Annotation']]
            for index in annotations.index:
                twin2.annotate(
                    annotations.loc[index, 'Annotation'],
                    xy=(index,annotations.loc[index, 'CO_2 (ppm)']),
                    xycoords='data',
                    xytext=(-100,30),
                    textcoords='offset points',
                    bbox=dict(boxstyle="round", fc="0.8"),
                    arrowprops=dict(arrowstyle='->',
                                    connectionstyle="angle,angleA=0,angleB=90,rad=10"))
            show()
        else:
            messagebox.showinfo(
            'Info',
            'Weniger als zwei Messwerte vorhanden.\n' +
            'Bitte später noch einmal versuchen.')

    def export(self):
        '''Export data to text file.'''
        if len(self.history) > 0:
            df = self.create_dataframe()
            filename = filedialog.asksaveasfilename()
            if len(filename) > 0:
                df.to_csv(filename)
        else:
            messagebox.showinfo(
            'Info',
            'Noch keine Messwerte vorhanden.\n' +
            'Bitte später noch einmal versuchen.')
        
    def destroy(self):
        if (messagebox.askyesno(
                title='Speichern?',
                message='Aufgezeichnete Messwerte speichern?'
        ) and len(self.history) > 0):
            self.export()
        try:
            self.mqtt_client.stop()
        except Exception as e:
            print(e)
        finally:
            super().destroy()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--config',
                        type=str,
                        required=False,
                        default='./.config',
                        help='Name of the config file. Default: ./.config')
    args = parser.parse_args()
    with open(args.config, 'r') as config_file:
        p=eval(config_file.read())
    MQTT_USER = p['MQTT_USER']
    MQTT_PASSWD = p['MQTT_PASSWD']
    co2_info = CO2Info()
    co2_info.wm_attributes("-topmost", 1)
    sensorlistpath='https://git.fh-muenster.de/pv238554/co2_info/-/raw/master/sensors.dat'
    try:
        sensorlistfile = urlopen(sensorlistpath)
        SENSORS = eval(sensorlistfile.read())
    except Exception as e:
        print(e)
        print('Using default sensor list.')
    co2_info.mainloop()
