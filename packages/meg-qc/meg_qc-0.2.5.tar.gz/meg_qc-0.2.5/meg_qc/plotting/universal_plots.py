import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from io import BytesIO
import numpy as np
import pandas as pd
import mne
import warnings
import random
import copy
import os
from mne.preprocessing import compute_average_dev_head_t
import matplotlib #this is in case we will need to suppress mne matplotlib plots

# mne.viz.set_browser_backend('matplotlib')
# matplotlib.use('Agg') 
#this command will suppress showing matplotlib figures produced by mne. They will still be saved for use in report but not shown when running the pipeline


class MEG_channels:

    """ 
    Channel with info for plotting: name, type, lobe area, color code, location, initial time series 
    + other data calculated by QC metrics (assigned in each metric separately while plotting).

    """

    def __init__(self, name: str, type: str, lobe: str, lobe_color: str, system: str, loc: list, time_series: list or np.ndarray = None, std_overall: float = None, std_epoch: list or np.ndarray = None, ptp_overall: float = None, ptp_epoch: list or np.ndarray = None, psd: list or np.ndarray = None, freq: list or np.ndarray = None, mean_ecg: list or np.ndarray = None, mean_ecg_smoothed: list or np.ndarray = None, mean_eog: list or np.ndarray = None, mean_eog_smoothed: list or np.ndarray = None, ecg_time = None, eog_time = None, ecg_corr_coeff = None, ecg_pval = None, ecg_amplitude_ratio = None, ecg_similarity_score = None, eog_corr_coeff = None, eog_pval = None, eog_amplitude_ratio = None, eog_similarity_score = None, muscle = None, head = None, muscle_time = None, head_time = None):

        """
        Constructor method
        
        Parameters
        ----------
        name : str
            The name of the channel.
        type : str
            The type of the channel: 'mag', 'grad'
        lobe : str
            The lobe area of the channel: 'left frontal', 'right frontal', 'left temporal', 'right temporal', 'left parietal', 'right parietal', 'left occipital', 'right occipital', 'central', 'subcortical', 'unknown'.
        lobe_color : str
            The color code for plotting with plotly according to the lobe area of the channel.
        system : str
            The system of the channel: 'CTF', 'TRIUX', 'OTHER'
        loc : list
            The location of the channel on the helmet.
        time_series : array
            The time series of the channel.
        std_overall : float
            The standard deviation of the channel time series.
        std_epoch : array
            The standard deviation of the channel time series per epochs.
        ptp_overall : float
            The peak-to-peak amplitude of the channel time series.
        ptp_epoch : array
            The peak-to-peak amplitude of the channel time series per epochs.
        psd : array
            The power spectral density of the channel.
        freq: array
            Frequencies for psd.
        mean_ecg : float
            The mean ECG artifact of the channel.
        mean_eog : float
            The mean EOG artifact of the channel.
        mean_ecg_smoothed : float
            The mean ECG artifact of the channel smoothed.
        mean_eog_smoothed : float
            The mean EOG artifact of the channel smoothed.
        ecg_corr_coeff : float
            The correlation coefficient of the channel with ECG.
        ecg_pval : float
            The p-value of the correlation coefficient of the channel with ECG.
        ecg_amplitude_ratio : float
            relation of the amplitude of a particular channel to all other channels for ECG contamination.
        ecg_similarity_score : float
            similarity score of the mean ecg data of this channel to refernce ecg/eog data comprised of both correlation and amplitude like: similarity_score = corr_coef * amplitude_ratio
        eog_corr_coeff : float
            The correlation coefficient of the channel with EOG.
        eog_pval : float
            The p-value of the correlation coefficient of the channel with EOG.
        eog_amplitude_ratio : float
            relation of the amplitude of a particular channel to all other channels for EOG contamination.
        eog_similarity_score : float
            similarity score of the mean eog data of this channel to refernce ecg/eog data comprised of both correlation and amplitude like: similarity_score = corr_coef * amplitude_ratio
        ecg_time : float
            The time vector of the ECG artifact.
        eog_time : float
            The time vector of the EOG artifact.
        muscle : float
            The muscle artifact data of the channel.
        head : float
            The head movement artifact data of the channel.
        muscle_time : float
            The time vector of the muscle artifact.
        head_time : float
            The time vector of the head movement artifact.
        

        """

        self.name = name
        self.type = type
        self.lobe = lobe
        self.lobe_color = lobe_color
        self.system = system
        self.loc = loc
        self.time_series = time_series
        self.std_overall = std_overall
        self.std_epoch = std_epoch
        self.ptp_overall = ptp_overall
        self.ptp_epoch = ptp_epoch
        self.psd = psd
        self.freq = freq
        self.mean_ecg = mean_ecg
        self.mean_ecg_smoothed = mean_ecg_smoothed
        self.mean_eog = mean_eog
        self.mean_eog_smoothed = mean_eog_smoothed
        self.ecg_corr_coeff = ecg_corr_coeff
        self.ecg_pval = ecg_pval
        self.ecg_amplitude_ratio = ecg_amplitude_ratio
        self.ecg_similarity_score = ecg_similarity_score
        self.eog_corr_coeff = eog_corr_coeff
        self.eog_pval = eog_pval
        self.eog_amplitude_ratio = eog_amplitude_ratio
        self.eog_similarity_score = eog_similarity_score
        self.ecg_time = ecg_time
        self.eog_time = eog_time
        self.muscle = muscle
        self.head = head
        self.muscle_time = muscle_time
        self.head_time = head_time


    def __repr__(self):

        """
        Returns the string representation of the object.

        """

        all_metrics = [self.std_overall, self.std_epoch, self.ptp_overall, self.ptp_epoch, self.psd, self.mean_ecg, self.mean_eog, self.ecg_corr_coeff, self.ecg_pval, self.ecg_amplitude_ratio, self.ecg_similarity_score, self.eog_corr_coeff, self.eog_pval, self.eog_amplitude_ratio, self.eog_similarity_score, self.muscle, self.head]
        all_metrics_names= ['std_overall', 'std_epoch', 'ptp_overall', 'ptp_epoch', 'psd', 'mean_ecg', 'mean_eog', 'ecg_corr_coeff', 'ecg_pval', 'ecg_amplitude_ratio', 'ecg_similarity_score', 'eog_corr_coeff', 'eog_pval', 'eog_amplitude_ratio', 'eog_similarity_score', 'muscle', 'head']
        non_none_indexes = [i for i, item in enumerate(all_metrics) if item is not None]

        return self.name + f' (type: {self.type}, lobe area: {self.lobe}, color code: {self.lobe_color}, location: {self.loc}, metrics_assigned: {", ".join([all_metrics_names[i] for i in non_none_indexes])}, | ecg_corr_coeff {self.ecg_corr_coeff}, eog_corr_coeff {self.eog_corr_coeff}, ecg_amplitude_ratio {self.ecg_amplitude_ratio}, eog_amplitude_ratio {self.eog_amplitude_ratio}, ecg_similarity_score {self.ecg_similarity_score}, eog_similarity_score {self.eog_similarity_score})'
    
    def to_df(self):

        """
        Returns the object as a pandas DataFrame. To be later exported into a tsv file.

        """

        data_dict = {}
        freqs = self.freq

        for attr, column_name in zip(['name', 'type', 'lobe', 'lobe_color', 'system', 'loc', 'time_series', 'std_overall', 'std_epoch', 'ptp_overall', 'ptp_epoch', 'psd', 'freq', 'mean_ecg', 'mean_ecg_smoothed', 'mean_eog', 'mean_eog_smoothed', 'ecg_corr_coeff', 'ecg_pval', 'ecg_amplitude_ratio', 'ecg_similarity_score', 'eog_corr_coeff', 'eog_pval', 'eog_amplitude_ratio', 'eog_similarity_score','muscle', 'head'], 
                                    ['Name', 'Type', 'Lobe', 'Lobe Color', 'System', 'Sensor_location', 'Time series', 'STD all', 'STD epoch', 'PtP all', 'PtP epoch', 'PSD', 'Freq', 'mean_ecg', 'smoothed_mean_ecg', 'mean_eog', 'smoothed_mean_eog', 'ecg_corr_coeff', 'ecg_pval', 'ecg_amplitude_ratio', 'ecg_similarity_score', 'eog_corr_coeff', 'eog_pval', 'eog_amplitude_ratio', 'eog_similarity_score', 'Muscle', 'Head']):
            
            
            #adding psds/ecg/eog/etc over time or over freqs for plotting later:
            value = getattr(self, attr)
            if isinstance(value, (list, np.ndarray)):

                
                if 'psd' == attr:
                    freqs = getattr(self, 'freq') #??? right
                    for i, v in enumerate(value):
                        fr = freqs[i]
                        data_dict[f'{column_name}_Hz_{fr}'] = [v]

                elif 'mean_ecg' in attr or 'mean_eog' in attr or 'muscle' == attr or 'head' == attr:
                    if attr == 'mean_ecg':
                        times = getattr(self, 'ecg_time') #attr can be 'mean_ecg', etc
                    elif attr == 'mean_eog':
                        times = getattr(self, 'eog_time') #attr can be 'mean_ecg', etc
                    elif attr == 'head':
                        times = getattr(self, 'head_time') #attr can be 'mean_ecg', etc
                    elif attr == 'muscle':
                        times = getattr(self, 'muscle_time') #attr can be 'mean_ecg', etc
                    
                    for i, v in enumerate(value):
                        t = times[i]
                        data_dict[f'{column_name}_sec_{t}'] = [v]

                else: #TODO: here maybe change to elif std/ptp?
                    for i, v in enumerate(value):
                        data_dict[f'{column_name}_{i}'] = [v]
            else:
                data_dict[column_name] = [value]

        return pd.DataFrame(data_dict)
    

    def add_ecg_info(self, Avg_artif_list: list, artif_time_vector: list):

        """
        Adds ECG artifact info to the channel object.

        Parameters
        ----------
        Avg_artif_list : list
            List of the average artifact objects.
        artif_time_vector : list
            Time vector of the artifact.

        """

        for artif_ch in Avg_artif_list:
            if artif_ch.name == self.name:
                self.mean_ecg = artif_ch.artif_data
                self.mean_ecg_smoothed = artif_ch.artif_data_smoothed
                self.ecg_time = artif_time_vector
                self.ecg_corr_coeff = artif_ch.corr_coef
                self.ecg_pval = artif_ch.p_value
                self.ecg_amplitude_ratio = artif_ch.amplitude_ratio
                self.ecg_similarity_score = artif_ch.similarity_score
                

    def add_eog_info(self, Avg_artif_list: list, artif_time_vector: list):

        """
        Adds EOG artifact info to the channel object.

        Parameters
        ----------
        Avg_artif_list : list
            List of the average artifact objects.
        artif_time_vector : list
            Time vector of the artifact.

        """

        for artif_ch in Avg_artif_list:
            if artif_ch.name == self.name:
                self.mean_eog = artif_ch.artif_data
                self.mean_eog_smoothed = artif_ch.artif_data_smoothed
                self.eog_time = artif_time_vector
                self.eog_corr_coeff = artif_ch.corr_coef
                self.eog_pval = artif_ch.p_value
                self.eog_amplitude_ratio = artif_ch.amplitude_ratio
                self.eog_similarity_score = artif_ch.similarity_score

                #Attention: here time_vector, corr_coeff, p_val and everything get assigned to ecg or eog, 
                # but artif_ch doesnt have this separation to ecg/eog. 
                # Need to just make sure that the function is called in the right place.

def add_CTF_lobes(channels_objs):

    # Initialize dictionary to store channels by lobe and side
    lobes_ctf = {
        'Left Frontal': [],
        'Right Frontal': [],
        'Left Temporal': [],
        'Right Temporal': [],
        'Left Parietal': [],
        'Right Parietal': [],
        'Left Occipital': [],
        'Right Occipital': [],
        'Central': [],
        'Reference': [],
        'EEG/EOG/ECG': [],
        'Extra': []  # Add 'Extra' lobe
    }

    # Iterate through the channel names and categorize them
    for key, value in channels_objs.items():
        for ch in value:
            categorized = False  # Track if the channel is categorized
            # Magnetometers (assuming they start with 'M')
            if ch.name.startswith('MLF'):  # Left Frontal
                lobes_ctf['Left Frontal'].append(ch.name)
                categorized = True
            elif ch.name.startswith('MRF'):  # Right Frontal
                lobes_ctf['Right Frontal'].append(ch.name)
                categorized = True
            elif ch.name.startswith('MLT'):  # Left Temporal
                lobes_ctf['Left Temporal'].append(ch.name)
                categorized = True
            elif ch.name.startswith('MRT'):  # Right Temporal
                lobes_ctf['Right Temporal'].append(ch.name)
                categorized = True
            elif ch.name.startswith('MLP'):  # Left Parietal
                lobes_ctf['Left Parietal'].append(ch.name)
                categorized = True
            elif ch.name.startswith('MRP'):  # Right Parietal
                lobes_ctf['Right Parietal'].append(ch.name)
                categorized = True
            elif ch.name.startswith('MLO'):  # Left Occipital
                lobes_ctf['Left Occipital'].append(ch.name)
                categorized = True
            elif ch.name.startswith('MRO'):  # Right Occipital
                lobes_ctf['Right Occipital'].append(ch.name)
                categorized = True
            elif ch.name.startswith('MLC') or ch.name.startswith('MRC'):  # Central (Midline)
                lobes_ctf['Central'].append(ch.name)
                categorized = True
            elif ch.name.startswith('MZ'):  # Reference Sensors
                lobes_ctf['Reference'].append(ch.name)
                categorized = True
            elif ch.name in ['Cz', 'Pz', 'ECG', 'VEOG', 'HEOG']:  # EEG/EOG/ECG channels
                lobes_ctf['EEG/EOG/ECG'].append(ch.name)
                categorized = True
            
            # Gradiometers (assuming they have a different prefix or suffix, such as 'G')
            elif ch.name.startswith('GLF'):  # Left Frontal Gradiometers
                lobes_ctf['Left Frontal'].append(ch.name)
                categorized = True
            elif ch.name.startswith('GRF'):  # Right Frontal Gradiometers
                lobes_ctf['Right Frontal'].append(ch.name)
                categorized = True
            elif ch.name.startswith('GLT'):  # Left Temporal Gradiometers
                lobes_ctf['Left Temporal'].append(ch.name)
                categorized = True
            elif ch.name.startswith('GRT'):  # Right Temporal Gradiometers
                lobes_ctf['Right Temporal'].append(ch.name)
                categorized = True
            elif ch.name.startswith('GLP'):  # Left Parietal Gradiometers
                lobes_ctf['Left Parietal'].append(ch.name)
                categorized = True
            elif ch.name.startswith('GRP'):  # Right Parietal Gradiometers
                lobes_ctf['Right Parietal'].append(ch.name)
                categorized = True
            elif ch.name.startswith('GLO'):  # Left Occipital Gradiometers
                lobes_ctf['Left Occipital'].append(ch.name)
                categorized = True
            elif ch.name.startswith('GRO'):  # Right Occipital Gradiometers
                lobes_ctf['Right Occipital'].append(ch.name)
                categorized = True
            elif ch.name.startswith('GLC') or ch.name.startswith('GRC'):  # Central (Midline) Gradiometers
                lobes_ctf['Central'].append(ch.name)
                categorized = True
            
            # If the channel was not categorized, add it to 'Extra'
            if not categorized:
                lobes_ctf['Extra'].append(ch.name)

    lobe_colors = {
        'Left Frontal': '#1f77b4',
        'Right Frontal': '#ff7f0e',
        'Left Temporal': '#2ca02c',
        'Right Temporal': '#9467bd',
        'Left Parietal': '#e377c2',
        'Right Parietal': '#d62728',
        'Left Occipital': '#bcbd22',
        'Right Occipital': '#17becf',
        'Central': '#8c564b',
        'Reference': '#7f7f7f',
        'EEG/EOG/ECG': '#bcbd22',
        'Extra': '#d3d3d3'  
    }

    lobes_color_coding_str = 'Color coding by lobe is applied as per CTF system.'
    for key, value in channels_objs.items():
        for ch in value:
            for lobe in lobes_ctf.keys():
                if ch.name in lobes_ctf[lobe]:
                    ch.lobe = lobe
                    ch.lobe_color = lobe_colors[lobe]

    return channels_objs, lobes_color_coding_str


def add_Triux_lobes(channels_objs):

    lobes_treux = {
            'Left Frontal': ['MEG0621', 'MEG0622', 'MEG0623', 'MEG0821', 'MEG0822', 'MEG0823', 'MEG0121', 'MEG0122', 'MEG0123', 'MEG0341', 'MEG0342', 'MEG0343', 'MEG0321', 'MEG0322', 'MEG0323', 'MEG0331',  'MEG0332', 'MEG0333', 'MEG0643', 'MEG0642', 'MEG0641', 'MEG0611', 'MEG0612', 'MEG0613', 'MEG0541', 'MEG0542', 'MEG0543', 'MEG0311', 'MEG0312', 'MEG0313', 'MEG0511', 'MEG0512', 'MEG0513', 'MEG0521', 'MEG0522', 'MEG0523', 'MEG0531', 'MEG0532', 'MEG0533'],
            'Right Frontal': ['MEG0811', 'MEG0812', 'MEG0813', 'MEG0911', 'MEG0912', 'MEG0913', 'MEG0921', 'MEG0922', 'MEG0923', 'MEG0931', 'MEG0932', 'MEG0933', 'MEG0941', 'MEG0942', 'MEG0943', 'MEG1011', 'MEG1012', 'MEG1013', 'MEG1021', 'MEG1022', 'MEG1023', 'MEG1031', 'MEG1032', 'MEG1033', 'MEG1211', 'MEG1212', 'MEG1213', 'MEG1221', 'MEG1222', 'MEG1223', 'MEG1231', 'MEG1232', 'MEG1233', 'MEG1241', 'MEG1242', 'MEG1243', 'MEG1411', 'MEG1412', 'MEG1413'],
            'Left Temporal': ['MEG0111', 'MEG0112', 'MEG0113', 'MEG0131', 'MEG0132', 'MEG0133', 'MEG0141', 'MEG0142', 'MEG0143', 'MEG0211', 'MEG0212', 'MEG0213', 'MEG0221', 'MEG0222', 'MEG0223', 'MEG0231', 'MEG0232', 'MEG0233', 'MEG0241', 'MEG0242', 'MEG0243', 'MEG1511', 'MEG1512', 'MEG1513', 'MEG1521', 'MEG1522', 'MEG1523', 'MEG1531', 'MEG1532', 'MEG1533', 'MEG1541', 'MEG1542', 'MEG1543', 'MEG1611', 'MEG1612', 'MEG1613', 'MEG1621', 'MEG1622', 'MEG1623'],
            'Right Temporal': ['MEG1311', 'MEG1312', 'MEG1313', 'MEG1321', 'MEG1322', 'MEG1323', 'MEG1421', 'MEG1422', 'MEG1423', 'MEG1431', 'MEG1432', 'MEG1433', 'MEG1441', 'MEG1442', 'MEG1443', 'MEG1341', 'MEG1342', 'MEG1343', 'MEG1331', 'MEG1332', 'MEG1333', 'MEG2611', 'MEG2612', 'MEG2613', 'MEG2621', 'MEG2622', 'MEG2623', 'MEG2631', 'MEG2632', 'MEG2633', 'MEG2641', 'MEG2642', 'MEG2643', 'MEG2411', 'MEG2412', 'MEG2413', 'MEG2421', 'MEG2422', 'MEG2423'],
            'Left Parietal': ['MEG0411', 'MEG0412', 'MEG0413', 'MEG0421', 'MEG0422', 'MEG0423', 'MEG0431', 'MEG0432', 'MEG0433', 'MEG0441', 'MEG0442', 'MEG0443', 'MEG0711', 'MEG0712', 'MEG0713', 'MEG0741', 'MEG0742', 'MEG0743', 'MEG1811', 'MEG1812', 'MEG1813', 'MEG1821', 'MEG1822', 'MEG1823', 'MEG1831', 'MEG1832', 'MEG1833', 'MEG1841', 'MEG1842', 'MEG1843', 'MEG0631', 'MEG0632', 'MEG0633', 'MEG1631', 'MEG1632', 'MEG1633', 'MEG2011', 'MEG2012', 'MEG2013'],
            'Right Parietal': ['MEG1041', 'MEG1042', 'MEG1043', 'MEG1111', 'MEG1112', 'MEG1113', 'MEG1121', 'MEG1122', 'MEG1123', 'MEG1131', 'MEG1132', 'MEG1133', 'MEG2233', 'MEG1141', 'MEG1142', 'MEG1143', 'MEG2243', 'MEG0721', 'MEG0722', 'MEG0723', 'MEG0731', 'MEG0732', 'MEG0733', 'MEG2211', 'MEG2212', 'MEG2213', 'MEG2221', 'MEG2222', 'MEG2223', 'MEG2231', 'MEG2232', 'MEG2233', 'MEG2241', 'MEG2242', 'MEG2243', 'MEG2021', 'MEG2022', 'MEG2023', 'MEG2441', 'MEG2442', 'MEG2443'],
            'Left Occipital': ['MEG1641', 'MEG1642', 'MEG1643', 'MEG1711', 'MEG1712', 'MEG1713', 'MEG1721', 'MEG1722', 'MEG1723', 'MEG1731', 'MEG1732', 'MEG1733', 'MEG1741', 'MEG1742', 'MEG1743', 'MEG1911', 'MEG1912', 'MEG1913', 'MEG1921', 'MEG1922', 'MEG1923', 'MEG1931', 'MEG1932', 'MEG1933', 'MEG1941', 'MEG1942', 'MEG1943', 'MEG2041', 'MEG2042', 'MEG2043', 'MEG2111', 'MEG2112', 'MEG2113', 'MEG2141', 'MEG2142', 'MEG2143'],
            'Right Occipital': ['MEG2031', 'MEG2032', 'MEG2033', 'MEG2121', 'MEG2122', 'MEG2123', 'MEG2311', 'MEG2312', 'MEG2313', 'MEG2321', 'MEG2322', 'MEG2323', 'MEG2331', 'MEG2332', 'MEG2333', 'MEG2341', 'MEG2342', 'MEG2343', 'MEG2511', 'MEG2512', 'MEG2513', 'MEG2521', 'MEG2522', 'MEG2523', 'MEG2531', 'MEG2532', 'MEG2533', 'MEG2541', 'MEG2542', 'MEG2543', 'MEG2431', 'MEG2432', 'MEG2433', 'MEG2131', 'MEG2132', 'MEG2133'],
            'Extra': []}  # Add 'Extra' lobe

    # These were just for Aarons presentation:
    # lobes_treux = {
    #         'Left Frontal': ['MEG0621', 'MEG0622', 'MEG0623', 'MEG0821', 'MEG0822', 'MEG0823', 'MEG0121', 'MEG0122', 'MEG0123', 'MEG0341', 'MEG0342', 'MEG0343', 'MEG0321', 'MEG0322', 'MEG0323', 'MEG0331',  'MEG0332', 'MEG0333', 'MEG0643', 'MEG0642', 'MEG0641', 'MEG0541', 'MEG0542', 'MEG0543', 'MEG0311', 'MEG0312', 'MEG0313', 'MEG0511', 'MEG0512', 'MEG0513', 'MEG0521', 'MEG0522', 'MEG0523', 'MEG0531', 'MEG0532', 'MEG0533'],
    #         'Right Frontal': ['MEG0811', 'MEG0812', 'MEG0813', 'MEG0911', 'MEG0912', 'MEG0913', 'MEG0921', 'MEG0922', 'MEG0923', 'MEG0931', 'MEG0932', 'MEG0933', 'MEG0941', 'MEG0942', 'MEG0943', 'MEG1011', 'MEG1012', 'MEG1013', 'MEG1021', 'MEG1022', 'MEG1023', 'MEG1031', 'MEG1032', 'MEG1033', 'MEG1211', 'MEG1212', 'MEG1213', 'MEG1221', 'MEG1222', 'MEG1223', 'MEG1231', 'MEG1232', 'MEG1233', 'MEG1241', 'MEG1242', 'MEG1243', 'MEG1411', 'MEG1412', 'MEG1413'],
    #         'Left Temporal': ['MEG0111', 'MEG0112', 'MEG0113', 'MEG0131', 'MEG0132', 'MEG0133', 'MEG0141', 'MEG0142', 'MEG0143', 'MEG0211', 'MEG0212', 'MEG0213', 'MEG0221', 'MEG0222', 'MEG0223', 'MEG0231', 'MEG0232', 'MEG0233', 'MEG0241', 'MEG0242', 'MEG0243', 'MEG1511', 'MEG1512', 'MEG1513', 'MEG1521', 'MEG1522', 'MEG1523', 'MEG1531', 'MEG1532', 'MEG1533', 'MEG1541', 'MEG1542', 'MEG1543', 'MEG1611', 'MEG1612', 'MEG1613', 'MEG1621', 'MEG1622', 'MEG1623'],
    #         'Right Temporal': ['MEG1311', 'MEG1312', 'MEG1313', 'MEG1321', 'MEG1322', 'MEG1323', 'MEG1421', 'MEG1422', 'MEG1423', 'MEG1431', 'MEG1432', 'MEG1433', 'MEG1441', 'MEG1442', 'MEG1443', 'MEG1341', 'MEG1342', 'MEG1343', 'MEG1331', 'MEG1332', 'MEG1333', 'MEG2611', 'MEG2612', 'MEG2613', 'MEG2621', 'MEG2622', 'MEG2623', 'MEG2631', 'MEG2632', 'MEG2633', 'MEG2641', 'MEG2642', 'MEG2643', 'MEG2411', 'MEG2412', 'MEG2413', 'MEG2421', 'MEG2422', 'MEG2423'],
    #         'Left Parietal': ['MEG0411', 'MEG0412', 'MEG0413', 'MEG0421', 'MEG0422', 'MEG0423', 'MEG0431', 'MEG0432', 'MEG0433', 'MEG0441', 'MEG0442', 'MEG0443', 'MEG0711', 'MEG0712', 'MEG0713', 'MEG0741', 'MEG0742', 'MEG0743', 'MEG1811', 'MEG1812', 'MEG1813', 'MEG1821', 'MEG1822', 'MEG1823', 'MEG1831', 'MEG1832', 'MEG1833', 'MEG1841', 'MEG1842', 'MEG1843', 'MEG0631', 'MEG0632', 'MEG0633', 'MEG1631', 'MEG1632', 'MEG1633', 'MEG2011', 'MEG2012', 'MEG2013'],
    #         'Right Parietal': ['MEG1041', 'MEG1042', 'MEG1043', 'MEG1111', 'MEG1112', 'MEG1113', 'MEG1121', 'MEG1122', 'MEG1123', 'MEG1131', 'MEG1132', 'MEG1133', 'MEG2233', 'MEG1141', 'MEG1142', 'MEG1143', 'MEG2243', 'MEG0721', 'MEG0722', 'MEG0723', 'MEG0731', 'MEG0732', 'MEG0733', 'MEG2211', 'MEG2212', 'MEG2213', 'MEG2221', 'MEG2222', 'MEG2223', 'MEG2231', 'MEG2232', 'MEG2233', 'MEG2241', 'MEG2242', 'MEG2243', 'MEG2021', 'MEG2022', 'MEG2023', 'MEG2441', 'MEG2442', 'MEG2443'],
    #         'Left Occipital': ['MEG1641', 'MEG1642', 'MEG1643', 'MEG1711', 'MEG1712', 'MEG1713', 'MEG1721', 'MEG1722', 'MEG1723', 'MEG1731', 'MEG1732', 'MEG1733', 'MEG1741', 'MEG1742', 'MEG1743', 'MEG1911', 'MEG1912', 'MEG1913', 'MEG1921', 'MEG1922', 'MEG1923', 'MEG1931', 'MEG1932', 'MEG1933', 'MEG1941', 'MEG1942', 'MEG1943', 'MEG2041', 'MEG2042', 'MEG2043', 'MEG2111', 'MEG2112', 'MEG2113', 'MEG2141', 'MEG2142', 'MEG2143', 'MEG2031', 'MEG2032', 'MEG2033', 'MEG2121', 'MEG2122', 'MEG2123', 'MEG2311', 'MEG2312', 'MEG2313', 'MEG2321', 'MEG2322', 'MEG2323', 'MEG2331', 'MEG2332', 'MEG2333', 'MEG2341', 'MEG2342', 'MEG2343', 'MEG2511', 'MEG2512', 'MEG2513', 'MEG2521', 'MEG2522', 'MEG2523', 'MEG2531', 'MEG2532', 'MEG2533', 'MEG2541', 'MEG2542', 'MEG2543', 'MEG2431', 'MEG2432', 'MEG2433', 'MEG2131', 'MEG2132', 'MEG2133'],
    #         'Right Occipital': ['MEG0611', 'MEG0612', 'MEG0613']}

    # #Now add to lobes_treux also the name of each channel with space in the middle:
    for lobe in lobes_treux.keys():
        lobes_treux[lobe] += [channel[:-4]+' '+channel[-4:] for channel in lobes_treux[lobe]]

    lobe_colors = {
        'Left Frontal': '#1f77b4',
        'Right Frontal': '#ff7f0e',
        'Left Temporal': '#2ca02c',
        'Right Temporal': '#9467bd',
        'Left Parietal': '#e377c2',
        'Right Parietal': '#d62728',
        'Left Occipital': '#bcbd22',
        'Right Occipital': '#17becf',
        'Extra': '#d3d3d3'}
    
    # These were just for Aarons presentation:
    # lobe_colors = {
    #     'Left Frontal': '#2ca02c',
    #     'Right Frontal': '#2ca02c',
    #     'Left Temporal': '#2ca02c',
    #     'Right Temporal': '#2ca02c',
    #     'Left Parietal': '#2ca02c',
    #     'Right Parietal': '#2ca02c',
    #     'Left Occipital': '#2ca02c',
    #     'Right Occipital': '#d62728'}
    
    
    #loop over all values in the dictionary:
    lobes_color_coding_str='Color coding by lobe is applied as per Treux system. Separation by lobes based on Y. Hu et al. "Partial Least Square Aided Beamforming Algorithm in Magnetoencephalography Source Imaging", 2018. '
    for key, value in channels_objs.items():
        for ch in value:
            categorized = False
            for lobe in lobes_treux.keys():
                if ch.name in lobes_treux[lobe]:
                    ch.lobe = lobe
                    ch.lobe_color = lobe_colors[lobe]
                    categorized = True
                    break
            # If the channel was not categorized, assign it to 'extra' lobe
            if not categorized:
                ch.lobe = 'Extra'
                ch.lobe_color = lobe_colors[lobe]

    return channels_objs, lobes_color_coding_str

def assign_channels_properties(raw: mne.io.Raw, meg_system: str):

    """
    Assign lobe area to each channel according to the lobe area dictionary + the color for plotting + channel location.

    Can later try to make this function a method of the MEG_channels class. 
    At the moment not possible because it needs to know the total number of channels to figure which meg system to use for locations. And MEG_channels class is created for each channel separately.

    Parameters
    ----------
    raw : mne.io.Raw
        Raw data set.
    meg_system: str
        CTF, Triux, None...

    Returns
    -------
    channels_objs : dict
        Dictionary with channel names for each channel type: mag, grad. Each channel has assigned lobe area and color for plotting + channel location.
    lobes_color_coding_str : str
        A string with information about the color coding of the lobes.

    """
    channels_objs={'mag': [], 'grad': []}
    if 'mag' in raw:
        mag_locs = raw.copy().pick('mag').info['chs']
        for ch in mag_locs:
            channels_objs['mag'] += [MEG_channels(ch['ch_name'], 'mag', 'unknown lobe', 'blue', 'OTHER', ch['loc'][:3])]
    else:
        channels_objs['mag'] = []

    if 'grad' in raw:
        grad_locs = raw.copy().pick('grad').info['chs']
        for ch in grad_locs:
            channels_objs['grad'] += [MEG_channels(ch['ch_name'], 'grad', 'unknown lobe', 'red', 'OTHER', ch['loc'][:3])]
    else:
        channels_objs['grad'] = []


    # for understanding how the locations are obtained. They can be extracted as:
    # mag_locs = raw.copy().pick('mag').info['chs']
    # mag_pos = [ch['loc'][:3] for ch in mag_locs]
    # (XYZ locations are first 3 digit in the ch['loc']  where ch is 1 sensor in raw.info['chs'])

    
    # Assign lobe labels to the channels:

    if meg_system.upper() == 'TRIUX' and len(channels_objs['mag']) == 102 and len(channels_objs['grad']) == 204: 
        #for 306 channel data in Elekta/Neuromag Treux system
        channels_objs, lobes_color_coding_str = add_Triux_lobes(channels_objs)

        #assign 'TRIUX' to all channels:
        for key, value in channels_objs.items():
            for ch in value:
                ch.system = 'TRIUX'

    elif meg_system.upper() == 'CTF':
        channels_objs, lobes_color_coding_str = add_CTF_lobes(channels_objs)

        #assign 'CTF' to all channels:
        for key, value in channels_objs.items():
            for ch in value:
                ch.system = 'CTF'

    else:
        lobes_color_coding_str='For MEG systems other than MEGIN Triux or CTF color coding by lobe is not applied.'
        lobe_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#e377c2', '#d62728', '#bcbd22', '#17becf']
        print('___MEGqc___: ' + lobes_color_coding_str)

        for key, value in channels_objs.items():
            for ch in value:
                ch.lobe = 'All channels'
                #take random color from lobe_colors:
                ch.lobe_color = random.choice(lobe_colors)
                ch.system = 'OTHER'

    #sort channels by name:
    for key, value in channels_objs.items():
        channels_objs[key] = sorted(value, key=lambda x: x.name)

    return channels_objs, lobes_color_coding_str


def sort_channels_by_lobe(channels_objs: dict):

    """ Sorts channels by lobes.

    Parameters
    ----------
    channels_objs : dict
        A dictionary of channel objects.
    
    Returns
    -------
    chs_by_lobe : dict
        A dictionary of channels sorted by ch type and lobe.

    """
    chs_by_lobe = {}
    for m_or_g in channels_objs:

        #put all channels into separate lists based on their lobes:
        lobes_names=list(set([ch.lobe for ch in channels_objs[m_or_g]]))
        
        lobes_dict = {key: [] for key in lobes_names}
        #fill the dict with channels:
        for ch in channels_objs[m_or_g]:
            lobes_dict[ch.lobe].append(ch) 

        # Sort the dictionary by lobes names (by the second word in the key, if it exists)
        chs_by_lobe[m_or_g] = dict(sorted(lobes_dict.items(), key=lambda x: x[0].split()[1] if len(x[0].split()) > 1 else ''))


    return chs_by_lobe


def check_num_channels_correct(chs_by_lobe: dict, note: str):

    """ 
    Print total number of channels in all lobes for 1 ch type (must be 102 mag and 204 grad in Elekta/Neuromag)
    
    Parameters
    ----------
    chs_by_lobe : dict
        A dictionary of channels sorted by ch type and lobe.
    note : str
        A note to print with the total number of channels.
    
    
    """
    for m_or_g in ['mag', 'grad']:
        total_number = sum([len(chs_by_lobe[m_or_g][key]) for key in chs_by_lobe[m_or_g].keys()])
        print("_______"+note+"_______total number in " + m_or_g, total_number)
        print("_______"+note+"_______must be 102 mag and 204 grad in Elekta/Neuromag")

    return 

def get_tit_and_unit(m_or_g: str, psd: bool = False):

    """
    Return title and unit for a given type of data (magnetometers or gradiometers) and type of plot (psd or not)
    
    Parameters
    ----------
    m_or_g : str
        'mag' or 'grad'
    psd : bool, optional
        True if psd plot, False if not, by default False

    Returns
    -------
    m_or_g_tit : str
        'Magnetometers' or 'Gradiometers'
    unit : str
        'T' or 'T/m' or 'T/Hz' or 'T/m / Hz'

    """
    
    if m_or_g=='mag':
        m_or_g_tit='Magnetometers'
        if psd is False:
            unit='Tesla'
        elif psd is True:
            unit='Tesla/Hz'
    elif m_or_g=='grad':
        m_or_g_tit='Gradiometers'
        if psd is False:
            unit='Tesla/m'
        elif psd is True:
            unit='Tesla/m / Hz'
    elif m_or_g == 'ECG':
        m_or_g_tit = 'ECG channel'
        unit = 'V'
    elif m_or_g == 'EOG':
        m_or_g_tit = 'EOG channel'
        unit = 'V'
    else:
        m_or_g_tit = '?'
        unit='?'

    return m_or_g_tit, unit


class QC_derivative:

    """ 
    Derivative of a QC measurement, main content of which is figure, data frame (saved later as csv) or html string.

    Attributes
    ----------
    content : figure, pd.DataFrame or str
        The main content of the derivative.
    name : str
        The name of the derivative (used to save in to file system)
    content_type : str
        The type of the content: 'plotly', 'matplotlib', 'csv', 'report' or 'mne_report'.
        Used to choose the right way to save the derivative in main function.
    description_for_user : str, optional
        The description of the derivative, by default 'Add measurement description for a user...'
        Used in the report to describe the derivative.
    

    """

    def __init__(self, content, name, content_type, description_for_user = '', fig_order = 0):

        """
        Constructor method
        
        Parameters
        ----------
        content : figure, pd.DataFrame or str
            The main content of the derivative.
        name : str
            The name of the derivative (used to save in to file system)
        content_type : str
            The type of the content: 'plotly', 'matplotlib', 'df', 'report' or 'mne_report'.
            Used to choose the right way to save the derivative in main function.
        description_for_user : str, optional
            The description of the derivative, by default 'Add measurement description for a user...'
            Used in the report to describe the derivative.
        fig_order : int, optional
            The order of the figure in the report, by default 0. Used for sorting.
        

        """

        self.content =  content
        self.name = name
        self.content_type = content_type
        self.description_for_user = description_for_user
        self.fig_order = fig_order

    def __repr__(self):

        """
        Returns the string representation of the object.
        """

        return 'MEG QC derivative: \n content: ' + str(type(self.content)) + '\n name: ' + self.name + '\n type: ' + self.content_type + '\n description for user: ' + self.description_for_user + '\n '

    def convert_fig_to_html(self):

        """
        Converts figure to html string.
        
        Returns
        -------
        html : str or None
            Html string or None if content_type is not 'plotly' or 'matplotlib'.

        """

        if self.content_type == 'plotly':
            return plotly.io.to_html(self.content, full_html=False)
        elif self.content_type == 'matplotlib':
            tmpfile = BytesIO()
            self.content.savefig(tmpfile, format='png', dpi=130) #writing image into a temporary file
            encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
            html = '<img src=\'data:image/png;base64,{}\'>'.format(encoded)
            return html
            # return mpld3.fig_to_html(self.content)
        elif not self.content_type:
            warnings.warn("Empty content_type of this QC_derivative instance")
        else:
            return None

    def convert_fig_to_html_add_description(self):

        """
        Converts figure to html string and adds description.

        Returns
        -------
        html : str or None
            Html string: fig + description or None + description if content_type is not 'plotly' or 'matplotlib'.

        """

        figure_report = self.convert_fig_to_html()

        return """<br></br>"""+ figure_report + """<p>"""+self.description_for_user+"""</p>"""


    def get_section(self):

        """ 
        Return a section of the report based on the info saved in the name. Normally not used. Use if cant figure out the derivative type.
        
        Returns
        -------
        section : str
            'RMSE', 'PTP_MANUAL', 'PTP_AUTO', 'PSD', 'EOG', 'ECG', 'MUSCLE', 'HEAD'.

        """

        if 'std' in self.name or 'rmse' in self.name or 'STD' in self.name or 'RMSE' in self.name:
            return 'RMSE'
        elif 'ptp_manual' in self.name or 'pp_manual' in self.name or 'PTP_manual' in self.name or 'PP_manual'in self.name:
            return 'PTP_MANUAL'
        elif 'ptp_auto' in self.name or 'pp_auto' in self.name or 'PTP_auto' in self.name or 'PP_auto' in self.name:
            return 'PTP_AUTO'
        elif 'psd' in self.name or 'PSD' in self.name:
            return 'PSD'
        elif 'eog' in self.name or 'EOG' in self.name:
            return 'EOG'
        elif 'ecg' in self.name or 'ECG' in self.name:
            return 'ECG'
        elif 'head' in self.name or 'HEAD' in self.name:
            return 'HEAD'
        elif 'muscle' in self.name or 'MUSCLE' in self.name:
            return 'MUSCLE'
        else:  
            warnings.warn("Check description of this QC_derivative instance: " + self.name)


def plot_df_of_channels_data_as_lines_by_lobe(chs_by_lobe: dict, df_data: pd.DataFrame, x_values: list):

    """
    Plots data from a data frame as lines, each lobe has own color as set in chs_by_lobe.

    Currntly not used.

    Parameters
    ----------
    chs_by_lobe : dict
        Dictionary with lobes as keys and lists of channels as values.
    df_data : pd.DataFrame
        Data frame with data to plot.
    x_values : list
        List of x values for the plot.
    
    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plotly figure.

    """

    fig = go.Figure()
    traces_lobes=[]
    traces_chs=[]
    for lobe, ch_list in chs_by_lobe.items():
        
        #Add lobe as a category to the plot
        
        for ch_obj in ch_list:
            if ch_obj.name in df_data.columns:
                ch_data=df_data[ch_obj.name].values
                color = ch_obj.lobe_color 
                # normally color must be same for all channels in lobe, so we could assign it before the loop as the color of the first channel,
                # but here it is done explicitly for every channel so that if there is any color error in chs_by_lobe, it will be visible

                traces_chs += [go.Scatter(x=x_values, y=ch_data, line=dict(color=color), name=ch_obj.name, legendgroup=ch_obj.lobe, legendgrouptitle=dict(text=lobe.upper(), font=dict(color=color)))]
                #legendgrouptitle is group tile on the plot. legendgroup is not visible on the plot - it s used for sorting the legend items in update_layout() below.

    # sort traces in random order:
    # When you plot traves right away in the order of the lobes, all the traces of one color lay on top of each other and yu can't see them all.
    # This is why they are not plotted in the loop. So we sort them in random order, so that traces of different colors are mixed.
    traces = traces_lobes + sorted(traces_chs, key=lambda x: random.random())

    downsampling_factor = 1  # replace with your desired downsampling factor
    # Create a new list for the downsampled traces
    traces_downsampled = []

    # Go through each trace
    for trace in traces:
        # Downsample the x and y values of the trace
        x_downsampled = trace['x'][::downsampling_factor]
        y_downsampled = trace['y'][::downsampling_factor]

        # Create a new trace with the downsampled values
        trace_downsampled = go.Scatter(x=x_downsampled, y=y_downsampled, line=trace['line'], name=trace['name'], legendgroup=trace['legendgroup'], legendgrouptitle=trace['legendgrouptitle'])

        # Add the downsampled trace to the list
        traces_downsampled.append(trace_downsampled)


    # Now first add these traces to the figure and only after that update the layout to make sure that the legend is grouped by lobe.
    fig = go.Figure(data=traces_downsampled)

    fig.update_layout(legend_traceorder='grouped', legend_tracegroupgap=12, legend_groupclick='toggleitem')
    #You can make it so when you click on lobe title or any channel in lobe you activate/hide all related channels if u set legend_groupclick='togglegroup'.
    #But then you cant see individual channels, it turn on/off the whole group. There is no option to tun group off by clicking on group title. Grup title and group items behave the same.

    #to see the legend: there is really nothing to sort here. The legend is sorted by default by the order of the traces in the figure. The onl way is to group the traces by lobe.
    #print(fig['layout'])

    #https://plotly.com/python/reference/?_ga=2.140286640.2070772584.1683497503-1784993506.1683497503#layout-legend-traceorder
    

    return fig


def plot_df_of_channels_data_as_lines_by_lobe_csv(f_path: str, metric: str, x_values, m_or_g, df=None):

    """
    Plots data from a data frame as lines, each lobe has own color.
    Data is taken from previously saved tsv file.

    Parameters
    ----------
    f_path : str
        Path to the csv file with the data to plot.
    metric : str
        The metric of the data to plot: 'psd', 'ecg', 'eog', 'smoothed_ecg', 'smoothed_eog'.
    x_values : list
        List of x values for the plot.
    m_or_g : str
        'mag' or 'grad'.
    
    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plotly figure.

    """
    if f_path is not None:
        df = pd.read_csv(f_path, sep='\t') #TODO: maybe remove reading csv and pass directly the df here?
    else:
        df = df


    fig = go.Figure()
    traces_lobes=[]
    traces_chs=[]

    add_scores = False #in most cases except ecg/eog we dont add scores to the plot
    if metric.lower() == 'psd':
        col_prefix = 'PSD_Hz_'
    elif metric.lower() == 'ecg':
        col_prefix = 'mean_ecg_sec_'
    elif metric.lower() == 'eog':
        col_prefix = 'mean_eog_sec_'
    elif metric.lower() == 'smoothed_ecg' or metric.lower() == 'ecg_smoothed':
        col_prefix = 'smoothed_mean_ecg_sec_'
        #Need to check if all 3 columns exist in df, are not empty and are not none - if so, add scores to hovertemplate:
        ecg_eog_scores = ['ecg_corr_coeff', 'ecg_pval', 'ecg_amplitude_ratio', 'ecg_similarity_score']
        add_scores = all(column_name in df.columns and not df[column_name].empty and df[column_name].notnull().any() for column_name in ecg_eog_scores)
    elif metric.lower() == 'smoothed_eog' or metric.lower() == 'eog_smoothed':
        col_prefix = 'smoothed_mean_eog_sec_'
        #Need to check if all 3 columns exist in df, are not empty and are not none - if so, add scores to hovertemplate:
        ecg_eog_scores = ['eog_corr_coeff', 'eog_pval', 'eog_amplitude_ratio', 'eog_similarity_score']
        add_scores = all(column_name in df.columns and not df[column_name].empty and df[column_name].notnull().any() for column_name in ecg_eog_scores)
    else:
        print('No proper column in df! Check the metric!')

   
    for index, row in df.iterrows():

        if row['Type'] == m_or_g: #plot only mag/grad
            ch_data = []
            for col in df.columns:
                if col_prefix in col:

                    #ch_data = row[col] #or maybe 
                    ch_data.append(row[col])

                    # normally color must be same for all channels in lobe, so we could assign it before the loop as the color of the first channel,
                    # but here it is done explicitly for every channel so that if there is any color error in chs_by_lobe, it will be visible
            
            color = row['Lobe Color']

            #traces_chs += [go.Scatter(x=x_values, y=ch_data, line=dict(color=color), name=row['Name'] , legendgroup=row['Lobe'] , legendgrouptitle=dict(text=row['Lobe'].upper(), font=dict(color=color)))]

            if add_scores:

                traces_chs += [go.Scatter(
                    x=x_values, 
                    y=ch_data, 
                    line=dict(color=color), 
                    name=row['Name'],
                    legendgroup=row['Lobe'],
                    legendgrouptitle=dict(text=row['Lobe'].upper(), font=dict(color=color)),

                    hovertemplate = (
                    '<b>'+row['Name']+'</b><br>' +
                    'time: %{x} s<br>'+
                    'magnitude: %{y} T<br>' +
                    '<i>corr_coeff: </i>'+'{:.2f}'.format(row[ecg_eog_scores[0]])+'<br>' +
                    '<i>p-value: </i>'+str(row[ecg_eog_scores[1]])+'<br>' +
                    '<i>amplitude_ratio: </i>'+'{:.2f}'.format(row[ecg_eog_scores[2]])+'<br>' +
                    '<i>similarity_score: </i>'+'{:.2f}'.format(row[ecg_eog_scores[3]])+'<br>'
                ))]
            else:
                traces_chs += [go.Scatter(
                    x=x_values, 
                    y=ch_data, 
                    line=dict(color=color), 
                    name=row['Name'],
                    legendgroup=row['Lobe'],
                    legendgrouptitle=dict(text=row['Lobe'].upper(), font=dict(color=color))
                )]
               
    # sort traces in random order:
    # When you plot traves right away in the order of the lobes, all the traces of one color lay on top of each other and yu can't see them all.
    # This is why they are not plotted in the loop. So we sort them in random order, so that traces of different colors are mixed.
    traces = traces_lobes + sorted(traces_chs, key=lambda x: random.random())

    if not traces:
        return None

    # Now first add these traces to the figure and only after that update the layout to make sure that the legend is grouped by lobe.
    fig = go.Figure(data=traces)

    fig.update_layout(legend_traceorder='grouped', legend_tracegroupgap=12, legend_groupclick='toggleitem')
    #You can make it so when you click on lobe title or any channel in lobe you activate/hide all related channels if u set legend_groupclick='togglegroup'.
    #But then you cant see individual channels, it turn on/off the whole group. There is no option to tun group off by clicking on group title. Grup title and group items behave the same.

    #to see the legend: there is really nothing to sort here. The legend is sorted by default by the order of the traces in the figure. The onl way is to group the traces by lobe.
    #print(fig['layout'])

    #https://plotly.com/python/reference/?_ga=2.140286640.2070772584.1683497503-1784993506.1683497503#layout-legend-traceorder
    

    return fig
        

def plot_time_series(raw: mne.io.Raw, m_or_g: str, chs_by_lobe: dict):

    """
    Plots time series of the chosen channels.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw file to be plotted.
    m_or_g : str
        The type of the channels to be plotted: 'mag' or 'grad'.
    chs_by_lobe : dict
        A dictionary with the keys as the names of the lobes and the values as the lists of the channels in the lobe.
    
    Returns
    -------
    qc_derivative : list
        A list of QC_derivative objects containing the plotly figure with interactive time series of each channel.

    """
    qc_derivative = []
    tit, unit = get_tit_and_unit(m_or_g)

    picked_channels = mne.pick_types(raw.info, meg=m_or_g)

    # Downsample data
    raw_resampled = raw.copy().resample(100, npad='auto') 
    #downsample the data to 100 Hz. The `npad` parameter is set to `'auto'` to automatically determine the amount of padding to use during the resampling process

    data = raw_resampled.get_data(picks=picked_channels) 

    ch_names=[]
    for i in range(data.shape[0]):
        ch_names.append(raw.ch_names[picked_channels[i]])


    #put data in data frame with ch_names as columns:
    df_data=pd.DataFrame(data.T, columns=ch_names)

    fig = plot_df_of_channels_data_as_lines_by_lobe(chs_by_lobe, df_data, raw_resampled.times)

    if fig is None:
        return []

    # Add title, x axis title, x axis slider and y axis units+title:
    fig.update_layout(
        title={
            'text': tit+' time series per channel',
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},

        xaxis_title='Time (s)',

        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="linear"),

        yaxis = dict(
                showexponent = 'all',
                exponentformat = 'e'),
            yaxis_title = unit) 
    
    qc_derivative += [QC_derivative(content=fig, name=tit+'_time_series', content_type='plotly')]

    return qc_derivative


def plot_time_series_avg(raw: mne.io.Raw, m_or_g: str):

    """
    Plots time series of the chosen channels.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw file to be plotted.
    m_or_g_chosen : str
        The type of the channels to be plotted: 'mag' or 'grad'.
    
    Returns
    -------
    qc_derivative : list
        A list of QC_derivative objects containing the plotly figure with interactive average time series.

    """
    qc_derivative = []
    tit, unit = get_tit_and_unit(m_or_g)

    picked_channels = mne.pick_types(raw.info, meg=m_or_g)

    # Downsample data
    raw_resampled = raw.copy().resample(100, npad='auto') 
    #downsample the data to 100 Hz. The `npad` parameter is set to `'auto'` to automatically determine the amount of padding to use during the resampling process

    t = raw_resampled.times
    data = raw_resampled.get_data(picks=picked_channels) 

    #average the data over all channels:
    data_avg = np.mean(data, axis = 0)

    #plot:
    trace = go.Scatter(x=t, y=data_avg, mode='lines', name=tit)
    fig = go.Figure(data=trace)

    # Add title, x axis title, x axis slider and y axis units+title:
    fig.update_layout(
        title={
            'text': tit+': time series averaged over all channels',
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},

        xaxis_title='Time (s)',

        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="linear"),

        yaxis = dict(
                showexponent = 'all',
                exponentformat = 'e'),
            yaxis_title = unit) 
    
    qc_derivative += [QC_derivative(content=fig, name=tit+'_time_series_avg', content_type='plotly')]

    return qc_derivative


def switch_names_on_off(fig: go.Figure):

    """
    Switches between showing channel names when hovering and always showing channel names.
    
    Parameters
    ----------
    fig : go.Figure
        The figure to be modified.
        
    Returns
    -------
    fig : go.Figure
        The modified figure.
        
    """

    # Define the buttons
    buttons = [
    dict(label='Show channels names on hover',
         method='update',
         args=[{'mode': 'markers'}]),
    dict(label='Always show channels names',
         method='update',
         args=[{'mode': 'markers+text'}])
    ]

    # Add the buttons to the layout
    fig.update_layout(updatemenus=[dict(type='buttons',
                                        showactive=True,
                                        buttons=buttons)])

    return fig


def plot_sensors_3d_separated(raw: mne.io.Raw, m_or_g_chosen: str):

    """
    Plots the 3D locations of the sensors in the raw file.
    Not used any more. As it plots mag and grad sensors separately and only if both are chosen for analysis. 
    Also it doesnt care for the lobe areas.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw file to be plotted.
    m_or_g_chosen : str
        The type of the channels to be plotted: 'mag' or 'grad'.
    
    Returns
    -------
    qc_derivative : list
        A list of QC_derivative objects containing the plotly figures with the sensor locations.

    """
    qc_derivative = []

    # Check if there are magnetometers and gradiometers in the raw file:
    if 'mag' in m_or_g_chosen:

        # Extract the sensor locations and names for magnetometers
        mag_locs = raw.copy().pick('mag').info['chs']
        mag_pos = [ch['loc'][:3] for ch in mag_locs]
        mag_names = [ch['ch_name'] for ch in mag_locs]

        if mag_pos:
            # Create the magnetometer plot with markers only

            mag_fig = go.Figure(data=[go.Scatter3d(x=[pos[0] for pos in mag_pos],
                                                y=[pos[1] for pos in mag_pos],
                                                z=[pos[2] for pos in mag_pos],
                                                mode='markers',
                                                marker=dict(size=5),
                                                text=mag_names,
                                                hovertemplate='%{text}')],
                                                layout=go.Layout(width=800, height=800))

            mag_fig.update_layout(
                title={
                'text': 'Magnetometers positions',
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
                hoverlabel=dict(font=dict(size=10)))
            

            mag_fig = switch_names_on_off(mag_fig)

            qc_derivative += [QC_derivative(content=mag_fig, name='Magnetometers_positions', content_type='plotly')]

    if 'grad' in m_or_g_chosen:

        # Extract the sensor locations and names for gradiometers
        grad_locs = raw.copy().pick('grad').info['chs']
        grad_pos = [ch['loc'][:3] for ch in grad_locs]
        grad_names = [ch['ch_name'] for ch in grad_locs]

        if grad_pos:

            #since grads have 2 sensors located in the same spot - need to put their names together to make pretty plot labels:

            grad_pos_together = []
            grad_names_together = []

            for i in range(len(grad_pos)-1):
                if all(x == y for x, y in zip(grad_pos[i], grad_pos[i+1])):
                    grad_pos_together += [grad_pos[i]]
                    grad_names_together += [grad_names[i]+', '+grad_names[i+1]]
                else:
                    pass


            # Add both sets of gradiometer positions to the plot:
            grad_fig = go.Figure(data=[go.Scatter3d(x=[pos[0] for pos in grad_pos_together],
                                                    y=[pos[1] for pos in grad_pos_together],
                                                    z=[pos[2] for pos in grad_pos_together],
                                                    mode='markers',
                                                    marker=dict(size=5),
                                                    text=grad_names_together,
                                                    hovertemplate='%{text}')],
                                                    layout=go.Layout(width=800, height=800))

            grad_fig.update_layout(
                title={
                'text': 'Gradiometers positions',
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
                hoverlabel=dict(font=dict(size=10)))


            # Add the button to have names show up on hover or always:
            grad_fig = switch_names_on_off(grad_fig)

            qc_derivative += [QC_derivative(content=grad_fig, name='Gradiometers_positions', content_type='plotly')]

    return qc_derivative


def keep_unique_locs(ch_list: list):

    """
    Combines channel names that have the same location and returns the unique locations and combined channel names for 3D plotting.

    Parameters
    ----------
    ch_list : list
        A list of channel objects.

    Returns
    -------
    new_locations : list
        A list of unique locations.
    new_names : list
        A list of combined channel names.
    new_colors : list
        A list of colors for each unique location.
    new_lobes : list
        A list of lobes for each unique location.

    """


    channel_names = [ch.name for ch in ch_list]
    channel_locations = [ch.loc for ch in ch_list]
    channel_colors = [ch.lobe_color for ch in ch_list]
    channel_lobes = [ch.lobe for ch in ch_list]

    # Create dictionaries to store unique locations and combined channel names
    unique_locations = {}
    combined_names = {}
    unique_colors = {}
    unique_lobes = {}

    # Loop through each channel and its location
    for i, (name, loc, color, lobe) in enumerate(zip(channel_names, channel_locations, channel_colors, channel_lobes)):
        # Convert location to a tuple for use as a dictionary key
        loc_key = tuple(loc)
        
        # If location is already in the unique_locations dictionary, add channel name to combined_names
        if loc_key in unique_locations:
            combined_names[unique_locations[loc_key]].append(name)
        # Otherwise, add location to unique_locations and channel name to combined_names
        else:
            unique_locations[loc_key] = i
            combined_names[i] = [name]
            unique_colors[i] = color
            unique_lobes[i] = lobe

    # Create new lists of unique locations and combined channel names
    new_locations = list(unique_locations.keys())
    new_names = [' & '.join(combined_names[i]) for i in combined_names]
    new_colors = [unique_colors[i] for i in unique_colors]
    new_lobes = [unique_lobes[i] for i in unique_lobes]

    return new_locations, new_names, new_colors, new_lobes 


def make_3d_sensors_trace(d3_locs: list, names: list, color: str, textsize: int, legend_category: str = 'channels', symbol: str = 'circle', textposition: str = 'top right'):

    """ Since grads have 2 sensors located in the same spot - need to put their names together to make pretty plot labels.

    Parameters
    ----------
    d3_locs : list
        A list of 3D locations of the sensors.
    names : list
        A list of names of the sensors.
    color : str
        A color of the sensors.
    textsize : int
        A size of the text.
    ch_type : str
        A type of the channels.
    symbol : str
        A symbol of the sensors.
    textposition : str
        A position of the text.
    
    Returns
    -------
    trace : plotly.graph_objs._scatter3d.Scatter3d
        A trace of the sensors.
    
    
    """

    trace = go.Scatter3d(
    x=[loc[0] for loc in d3_locs],
    y=[loc[1] for loc in d3_locs],
    z=[loc[2] for loc in d3_locs],
    mode='markers',
    marker=dict(
        color=color,
        size=8,
        symbol=symbol,
    ),
    text=names,
    hoverinfo='text',
    name=legend_category,
    textposition=textposition,
    textfont=dict(size=textsize, color=color))

    return trace


def plot_sensors_3d(chs_by_lobe: dict):

    """
    Plots the 3D locations of the sensors in the raw file. Plot both mags and grads (if both present) in 1 figure. 
    Can turn mags/grads visialisation on and off.
    Separete channels into brain areas by color coding.


    Parameters
    ----------
    chs_by_lobe : dict
        A dictionary of channels by ch type and lobe.
    
    Returns
    -------
    qc_derivative : list
        A list of QC_derivative objects containing the plotly figures with the sensor locations.

    """

    chs_by_lobe_copy = copy.deepcopy(chs_by_lobe)
    #otherwise we will change the original dict here and keep it messed up for the next function

    qc_derivative = []

    # Put all channels into a simplier dictiary: separatin by lobe byt not by ch type any more as we plot all chs in 1 fig here:
    lobes_dict = {}
    for ch_type in chs_by_lobe_copy:
        for lobe in chs_by_lobe_copy[ch_type]:
            if lobe not in lobes_dict:
                lobes_dict[lobe] = chs_by_lobe_copy[ch_type][lobe]
            else:
                lobes_dict[lobe] += chs_by_lobe_copy[ch_type][lobe]

    traces = []

    if len(lobes_dict)>1: #if there are lobes - we use color coding: one clor pear each lobe
        for lobe in lobes_dict:
            ch_locs, ch_names, ch_color, ch_lobe = keep_unique_locs(lobes_dict[lobe])
            traces.append(make_3d_sensors_trace(ch_locs, ch_names, ch_color[0], 10, ch_lobe[0], 'circle', 'top left'))
            #here color and lobe must be identical for all channels in 1 trace, thi is why we take the first element of the list
            # TEXT SIZE set to 10. This works for the "Always show names" option but not for "Show names on hover" option

    else: #if there are no lobes - we use random colors previously assigned to channels, channel names will be used instead of lobe names in make_3d_trace function
        ch_locs, ch_names, ch_color, ch_lobe = keep_unique_locs(lobes_dict[lobe])
        for i, _ in enumerate(ch_locs):
            traces.append(make_3d_sensors_trace([ch_locs[i]], ch_names[i], ch_color[i], 10, ch_names[i], 'circle', 'top left'))

    print(lobes_dict)

    if not traces:
        return []

    fig = go.Figure(data=traces)

    fig.update_layout(
        width=900, height=900,
        title={
        'text': 'Sensors positions',
        'y':0.85,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    
    fig.update_layout(
        scene = dict(
        xaxis = dict(visible=False),
        yaxis = dict(visible=False),
        zaxis =dict(visible=False)
        )
    )

    #check_num_channels_correct(chs_by_lobe, 'END_PLOT') #check we didnt change the original dict


    # Add the button to have names show up on hover or always:
    fig = switch_names_on_off(fig)

    fig.update_traces(hoverlabel=dict(font=dict(size=10))) #TEXT SIZE set to 10 again. This works for the "Show names on hover" option, but not for "Always show names" option

    qc_derivative += [QC_derivative(content=fig, name='Sensors_positions', content_type='plotly', description_for_user="Magnetometers names end with '1' like 'MEG0111'. Gradiometers names end with '2' and '3' like 'MEG0112', 'MEG0113'. ")]

    return qc_derivative

def get_meg_system(sensors_df):

    """
    Get which meg system we work with from the df. Make sure there is only 1 system.
    
    """
    
    # Get unique values, avoiding NaNs and empty strings
    system = sensors_df['System'].dropna().unique().tolist()
    system = [s for s in system if s != '']

    # Check the number of unique values
    if len(system) == 1:
        result = system[0]
    else:
        result = 'OTHER'

    return result

def plot_sensors_3d_csv(sensors_csv_path: str):

    """
    Plots the 3D locations of the sensors in the raw file. 
    Plot both mags and grads (if both present) in 1 figure. 
    Can turn mags/grads visialisation on and off.
    Separete channels into brain areas by color coding.

    Plot is made on base of the tsv file with sensors locations.


    Parameters
    ----------
    sensors_csv_path : str
        Path to the tsv file with the sensors locations.
    
    Returns
    -------
    qc_derivative : list
        A list of QC_derivative objects containing the plotly figures with the sensor locations.

    """
    file_name = os.path.basename(sensors_csv_path)
    if 'ecgchannel' in file_name.lower() or 'eogchannel' in file_name.lower():
        return []
    #we will get tsv representing ECG/EOG channel itself landed here. We dont need to plot it with this func.

    df = pd.read_csv(sensors_csv_path, sep='\t')

    #double check: if there are no lobes in df - skip this plot, it s not the right df:
    if 'Lobe' not in df.columns or 'System' not in df.columns:
        return []

    system = get_meg_system(df)

    if system.upper() == 'TRIUX':
        fig_desc = "Magnetometers names end with '1' like 'MEG0111'. Gradiometers names end with '2' and '3' like 'MEG0112', 'MEG0113'."
    else:
        fig_desc = ""

    #to not rewrite the whole func, just turn the df back into dic of MEG_channels:
    
    unique_lobes = df['Lobe'].unique().tolist()

    lobes_dict={}
    for lobe in unique_lobes:
        lobes_dict[lobe] = []
        for index, row in df.iterrows():
            if row['Lobe'] == lobe:
                locs = [float(row[col]) for col in df.columns if 'Sensor_location' in col]
                lobes_dict[lobe].append(MEG_channels(name = row['Name'], type = row['Type'], lobe = row['Lobe'], lobe_color = row['Lobe Color'], system = row ['System'], loc = locs))

    traces = []

    #system = df['System'].unique().tolist()

    if len(lobes_dict)>1: #if there are lobes - we use color coding: one color pear each lobe
        for lobe in lobes_dict:
            ch_locs, ch_names, ch_color, ch_lobe = keep_unique_locs(lobes_dict[lobe])
            traces.append(make_3d_sensors_trace(ch_locs, ch_names, ch_color[0], 10, ch_lobe[0], 'circle', 'top left'))
            #here color and lobe must be identical for all channels in 1 trace, thi is why we take the first element of the list
            # TEXT SIZE set to 10. This works for the "Always show names" option but not for "Show names on hover" option

    else: #if there are no lobes - we use random colors previously assigned to channels, channel names will be used instead of lobe names in make_3d_trace function
        ch_locs, ch_names, ch_color, ch_lobe = keep_unique_locs(lobes_dict[lobe])
        for i, _ in enumerate(ch_locs):
            traces.append(make_3d_sensors_trace([ch_locs[i]], ch_names[i], ch_color[i], 10, ch_names[i], 'circle', 'top left'))

    if not traces:
        return []
    
    fig = go.Figure(data=traces)

    fig.update_layout(
        width=900, height=900,
        title={
        'text': 'Sensors positions',
        'y':0.85,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    
    fig.update_layout(
        scene = dict(
        xaxis = dict(visible=False),
        yaxis = dict(visible=False),
        zaxis =dict(visible=False)
        )
    )


    # Add the button to have names show up on hover or always:
    fig = switch_names_on_off(fig)

    fig.update_traces(hoverlabel=dict(font=dict(size=10))) #TEXT SIZE set to 10 again. This works for the "Show names on hover" option, but not for "Always show names" option
    
    qc_derivative = [QC_derivative(content=fig, name='Sensors_positions', content_type='plotly', description_for_user=fig_desc, fig_order=-1)]

    return qc_derivative 


def boxplot_epochs(df_mg: pd.DataFrame, ch_type: str, what_data: str, x_axis_boxes: str):

    """
    Creates representation of calculated data as multiple boxplots. Used in STD and PtP_manual measurements. 

    - If x_axis_boxes is 'channels', each box represents 1 epoch, each dot is std of 1 channel for this epoch
    - If x_axis_boxes is 'epochs', each box represents 1 channel, each dot is std of 1 epoch for this channel

    
    Parameters
    ----------
    df_mg : pd.DataFrame
        Data frame with std or peak-to-peak values for each channel and epoch. Columns are epochs, rows are channels.
    ch_type : str
        Type of the channel: 'mag', 'grad'
    what_data : str
        Type of the data: 'peaks' or 'stds'
    x_axis_boxes : str
        What to plot as boxplot on x axis: 'channels' or 'epochs'

    Returns
    -------
    fig_deriv : QC_derivative 
        derivative containing plotly figure
    
    """

    ch_tit, unit = get_tit_and_unit(ch_type)

    if what_data=='peaks':
        hover_tit='Amplitude'
        y_ax_and_fig_title='Peak-to-peak amplitude'
        fig_name='PP_manual_epoch_per_channel_'+ch_tit
    elif what_data=='stds':
        hover_tit='STD'
        y_ax_and_fig_title='Standard deviation'
        fig_name='STD_epoch_per_channel_'+ch_tit
    else:
        print('what_data should be either peaks or stds')

    if x_axis_boxes=='channels':
        #transpose the data to plot channels on x axes
        df_mg = df_mg.T
        legend_title = ''
        hovertemplate='Epoch: %{text}<br>'+hover_tit+': %{y: .2e}'
    elif x_axis_boxes=='epochs':
        legend_title = 'Epochs'
        hovertemplate='%{text}<br>'+hover_tit+': %{y: .2e}'
    else:
        print('x_axis_boxes should be either channels or epochs')

    #collect all names of original df into a list to use as tick labels:
    boxes_names = df_mg.columns.tolist() #list of channel names or epoch names
    #boxes_names=list(df_mg) 

    fig = go.Figure()

    for col in df_mg:
        fig.add_trace(go.Box(y=df_mg[col].values, 
        name=str(df_mg[col].name), 
        opacity=0.7, 
        boxpoints="all", 
        pointpos=0,
        marker_size=3,
        line_width=1,
        text=df_mg[col].index,
        ))
        fig.update_traces(hovertemplate=hovertemplate)

    
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [v for v in range(0, len(boxes_names))],
            ticktext = boxes_names,
            rangeslider=dict(visible=True)
        ),
        xaxis_title='Experimental epochs',
        yaxis = dict(
            showexponent = 'all',
            exponentformat = 'e'),
        yaxis_title=y_ax_and_fig_title+' in '+unit,
        title={
            'text': y_ax_and_fig_title+' over epochs for '+ch_tit,
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        legend_title=legend_title)
        

    fig_deriv = QC_derivative(content=fig, name=fig_name, content_type='plotly')

    return fig_deriv


def boxplot_epoched_xaxis_channels(chs_by_lobe: dict, df_std_ptp: pd.DataFrame, ch_type: str, what_data: str):

    """
    Creates representation of calculated data as multiple boxplots. Used in STD and PtP_manual measurements. 
    Color tagged channels by lobes. 
    One box is one channel, boxes are on x axis. Epoch are inside as dots. Y axis shows the STD/PtP value.
    
    Parameters
    ----------
    chs_by_lobe : dict
        Dictionary with channel objects sorted by lobe.
    df_std_ptp : pd.DataFrame
        Data Frame containing std or ptp value for each chnnel and each epoch
    ch_type : str
        Type of the channel: 'mag', 'grad'
    what_data : str
        Type of the data: 'peaks' or 'stds'

    Returns
    -------
    fig_deriv : QC_derivative 
        derivative containing plotly figure
    
    """

    epochs_names = df_std_ptp.columns.tolist()
    

    ch_tit, unit = get_tit_and_unit(ch_type)

    if what_data=='peaks':
        hover_tit='PtP Amplitude'
        y_ax_and_fig_title='Peak-to-peak amplitude'
        fig_name='PP_manual_epoch_per_channel_'+ch_tit
    elif what_data=='stds':
        hover_tit='STD'
        y_ax_and_fig_title='Standard deviation'
        fig_name='STD_epoch_per_channel_'+ch_tit
    else:
        print('what_data should be either peaks or stds')

    x_axis_boxes = 'channels'
    if x_axis_boxes=='channels':
        hovertemplate='Epoch: %{text}<br>'+hover_tit+': %{y: .2e}'
    elif x_axis_boxes=='epochs':
        #legend_title = 'Epochs'
        hovertemplate='%{text}<br>'+hover_tit+': %{y: .2e}'
    else:
        print('x_axis_boxes should be either channels or epochs')


    fig = go.Figure()

    #Here each trace is 1 box representing 1 channel. Epochs inside the box are automatically plotted given argument boxpoints="all":
    #Boxes are groupped by lobe. So first each channel fo lobe 1 is plotted, then each of lobe 2, etc..
    boxes_names = []
    for lobe,  ch_list in chs_by_lobe.items():
        for ch in ch_list:
            if what_data == 'stds':
                data = ch.std_epoch
            elif what_data == 'peaks':
                data = ch.ptp_epoch
            
            boxes_names += [ch.name]

            fig.add_trace(go.Box(y=data, 
            name=ch.name, 
            opacity=0.7, 
            boxpoints="all", 
            pointpos=0,
            marker_color=ch.lobe_color,
            marker_size=3,
            legendgroup=ch.lobe, 
            legendgrouptitle=dict(text=lobe.upper()),
            line_width=0.8,
            line_color=ch.lobe_color,
            text=epochs_names))

    fig.update_traces(hovertemplate=hovertemplate)

    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [v for v in range(0, len(boxes_names))],
            ticktext = boxes_names,
            rangeslider=dict(visible=True)),
        yaxis = dict(
            showexponent = 'all',
            exponentformat = 'e'),
        yaxis_title=y_ax_and_fig_title+' in '+unit,
        title={
            'text': y_ax_and_fig_title+' over epochs for '+ch_tit,
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},)
        #legend_title=legend_title)
        

    fig_deriv = QC_derivative(content=fig, name=fig_name, content_type='plotly')

    return fig_deriv


def boxplot_epoched_xaxis_channels_csv(std_csv_path: str, ch_type: str, what_data: str):

    """
    Creates representation of calculated data as multiple boxplots. Used in STD and PtP_manual measurements. 
    Color tagged channels by lobes. 
    One box is one channel, boxes are on x axis. Epoch are inside as dots. Y axis shows the STD/PtP value.

    On base of the data from tsv file.
    
    Parameters
    ----------
    std_csv_path: str
        Path to the tsv file with std data
    ch_type : str
        Type of the channel: 'mag', 'grad'
    what_data : str
        Type of the data: 'peaks' or 'stds'

    Returns
    -------
    fig_deriv : QC_derivative 
        derivative containing plotly figure
    
    """
    df = pd.read_csv(std_csv_path, sep='\t')

    ch_tit, unit = get_tit_and_unit(ch_type)

    if what_data=='peaks':
        hover_tit='PtP Amplitude'
        y_ax_and_fig_title='Peak-to-peak amplitude'
        fig_name='PP_manual_epoch_per_channel_'+ch_tit
        data_prefix = 'PtP epoch_'
    elif what_data=='stds':
        hover_tit='STD'
        y_ax_and_fig_title='Standard deviation'
        fig_name='STD_epoch_per_channel_'+ch_tit
        data_prefix = 'STD epoch_'
    else:
        print('what_data should be either peaks or stds')
        return []


    #Check if df has relevant data for plotting:
    #find columns with epochs:
    relevant_columns = [col for col in df.columns if data_prefix in col]

    # Filter rows where 'Type' is the one we need: mag, grad
    filtered_df = df[df['Type'] == ch_type]

    # Check if all relevant cells are empty
    all_empty = filtered_df[relevant_columns].isnull().all().all()

    if all_empty:
        return []


    # Figure column names:
    # Create a list of columns that start with 'STD epoch_'
    epoch_columns = [col for col in df.columns if col.startswith('STD epoch_') or col.startswith('PtP epoch_')]

    # Get the number of these columns
    num_epoch_columns = len(epoch_columns)

    # Create a list of numbers from 0 to that length
    epochs_names = [i for i in range(num_epoch_columns)]


    x_axis_boxes = 'channels'
    if x_axis_boxes=='channels':
        hovertemplate='Epoch: %{text}<br>'+hover_tit+': %{y: .2e}'
    elif x_axis_boxes=='epochs':
        #legend_title = 'Epochs'
        hovertemplate='%{text}<br>'+hover_tit+': %{y: .2e}'
    else:
        print('x_axis_boxes should be either channels or epochs')
        return []


    fig = go.Figure()

    #Here each trace is 1 box representing 1 channel. Epochs inside the box are automatically plotted given argument boxpoints="all":
    #Boxes are groupped by lobe. So first each channel fo lobe 1 is plotted, then each of lobe 2, etc..
    boxes_names = []


    for index, row in df.iterrows():
        if row['Type'] == ch_type: #plot only mag/grad
            
            data = [row[data_prefix+str(n)] for n in epochs_names]

            boxes_names += [row['Name']]

            fig.add_trace(go.Box(y=data, 
            name=row['Name'], 
            opacity=0.7, 
            boxpoints="all", 
            pointpos=0,
            marker_color=row['Lobe Color'],
            marker_size=3,
            legendgroup=row['Lobe'], 
            legendgrouptitle=dict(text=row['Lobe'].upper()),
            line_width=0.8,
            line_color=row['Lobe Color'],
            text=epochs_names))

    
    fig.update_traces(hovertemplate=hovertemplate)

    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [v for v in range(0, len(boxes_names))],
            ticktext = boxes_names,
            rangeslider=dict(visible=True)),
        yaxis = dict(
            showexponent = 'all',
            exponentformat = 'e'),
        yaxis_title=y_ax_and_fig_title+' in '+unit,
        title={
            'text': y_ax_and_fig_title+' over epochs for '+ch_tit,
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},)
        #legend_title=legend_title)

    fig_deriv = [QC_derivative(content=fig, name=fig_name, content_type='plotly')]

    return fig_deriv


def add_log_buttons(fig: go.Figure):

    """
    Add buttons to switch scale between log and linear. For some reason only swithcing the Y scale works so far.

    Parameters
    ----------
    fig : go.Figure
        The figure to be modified withot buttons
        
    Returns
    -------
    fig : go.Figure
        The modified figure with the buttons
        
    """

    updatemenus = [
    {
        "buttons": [
            {
                "args": [{"xaxis.type": "linear"}],
                "label": "X linear",
                "method": "relayout"
            },
            {
                "args": [{"xaxis.type": "log"}],
                "label": "X log",
                "method": "relayout"
            }
        ],
        "direction": "right",
        "showactive": True,
        "type": "buttons",
        "x": 0.15,
        "y": -0.1
    },
    {
        "buttons": [
            {
                "args": [{"yaxis.type": "linear"}],
                "label": "Y linear",
                "method": "relayout"
            },
            {
                "args": [{"yaxis.type": "log"}],
                "label": "Y log",
                "method": "relayout"
            }
        ],
        "direction": "right",
        "showactive": True,
        "type": "buttons",
        "x": 1,
        "y": -0.1
    }]

    fig.update_layout(updatemenus=updatemenus)

    return fig


def figure_x_axis(df, metric):

    """
    Figure out the x axis for plotting based on the metric.

    Parameters
    ----------
    df : pd.DataFrame
        Data Frame with the data to be plotted.
    metric : str
        The metric of the data: 'psd', 'eog', 'ecg', 'muscle', 'head'.

    Returns
    -------
    freqs : np.array
        Array of frequencies for the PSD data.
    time_vec : np.array
        Array of time values for the EOG, ECG, muscle, or head data.
    
    """
     
    if metric.lower() == 'psd':
        # Figure out frequencies:
        freq_cols = [column for column in df if column.startswith('PSD_Hz_')]
        freqs = np.array([float(x.replace('PSD_Hz_', '')) for x in freq_cols])
        return freqs
    
    elif metric.lower() == 'eog' or metric.lower() == 'ecg' or metric.lower() == 'muscle' or metric.lower() == 'head':
        if metric.lower() == 'ecg':
            prefix = 'mean_ecg_sec_'
        elif metric.lower() == 'smoothed_ecg':
            prefix = 'smoothed_mean_ecg_sec_'
        elif metric.lower() == 'smoothed_eog':
            prefix = 'smoothed_mean_eog_sec_'
        elif metric.lower() == 'eog': 
            prefix = 'mean_eog_sec_'
        elif metric.lower() == 'muscle':
            prefix = 'Muscle_sec_'
        elif metric.lower() == 'head':
            prefix = 'Head_sec_'
        
        time_cols = [column for column in df if column.startswith(prefix)]
        time_vec = np.array([float(x.replace(prefix, '')) for x in time_cols])

        return time_vec
    
    else:
        print('Wrong metric! Cant figure out xaxis for plotting.')
        return None


def Plot_psd_csv(m_or_g:str, f_path: str, method: str):

    """
    Plotting Power Spectral Density for all channels based on dtaa from tsv file.

    Parameters
    ----------
    m_or_g : str
        'mag' or 'grad'
    f_path : str
        Path to the tsv file with PSD data.
    method : str
        'welch' or 'multitaper' or other method

    Returns
    -------
    QC_derivative
        QC_derivative object with plotly figure as content
        
    """

    # First, get the epochs from csv and convert back into object.
    df = pd.read_csv(f_path, sep='\t') 

    if 'Name' not in df.columns:
        return []

    # Figure out frequencies:
    freqs = figure_x_axis(df, metric='psd')

    #TODO: DF with freqs still has redundand columns with names of frequencies like column.startswith('Freq_')
    # Remove them!

    channels = []
    for index, row in df.iterrows():
        channels.append(row['Name'])

    fig = plot_df_of_channels_data_as_lines_by_lobe_csv(f_path, 'psd', freqs, m_or_g)

    if fig is None:
        return []

    tit, unit = get_tit_and_unit(m_or_g)
    fig.update_layout(
    title={
    'text': method[0].upper()+method[1:]+" periodogram for all "+tit,
    'y':0.85,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'},
    yaxis_title="Amplitude, "+unit,
    yaxis = dict(
        showexponent = 'all',
        exponentformat = 'e'),
    xaxis_title="Frequency (Hz)")

    fig.update_traces(hovertemplate='Frequency: %{x} Hz<br>Amplitude: %{y: .2e} T/Hz')

    #Add buttons to switch scale between log and linear:
    fig = add_log_buttons(fig)
    
    fig_name='PSD_all_data_'+tit

    qc_derivative = [QC_derivative(content=fig, name=fig_name, content_type='plotly')]

    return qc_derivative



def plot_pie_chart_freq(amplitudes_relative: list, amplitudes_abs: list, total_amplitude: float, m_or_g: str, bands_names: list, fig_tit: str, fig_name: str):
    
    """
    OLD VERSION, no csv 

    Plot pie chart representation of relative amplitude of each frequency band over the entire 
    times series of mags or grads, not separated by individual channels.

    Parameters
    ----------
    freq_amplitudes_relative : list
        list of relative amplitudes of each frequency band
    freq_amplitudes_absolute : list
        list of absolute amplitudes of each frequency band 
    total_freq_ampl : float
        total amplitude of all frequency bands. It might be diffrent from simple sum of mean_abs_values. In this case 'unknown' band will be added in this fucntion
    m_or_g : str
        'mag' or 'grad'
    bands_names : list
        list of names of frequency bands
    fig_tit : str
        extra title to be added to the plot
    fig_name : str
        name of the figure to be saved
    
    Returns
    -------
    QC_derivative
        QC_derivative object with plotly figure as content

    """
    all_bands_names=bands_names.copy() 
    #the lists change in this function and this change is tranfered outside the fuction even when these lists are not returned explicitly. 
    #To keep them in original state outside the function, they are copied here.
    all_mean_abs_values=amplitudes_abs.copy()
    ch_type_tit, unit = get_tit_and_unit(m_or_g, psd=True)

    #If mean relative percentages dont sum up into 100%, add the 'unknown' part.
    all_mean_relative_values=[v * 100 for v in amplitudes_relative]  #in percentage
    relative_unknown=100-(sum(amplitudes_relative))*100
    if relative_unknown>0:
        all_mean_relative_values.append(relative_unknown)
        all_bands_names.append('other frequencies')
        all_mean_abs_values.append(total_amplitude - sum(amplitudes_abs))

    labels=[None]*len(all_bands_names)
    for n, name in enumerate(all_bands_names):
        labels[n]=name + ': ' + str("%.2e" % all_mean_abs_values[n]) + ' ' + unit # "%.2e" % removes too many digits after coma

    fig = go.Figure(data=[go.Pie(labels=labels, values=all_mean_relative_values)])
    fig.update_layout(
    title={
    'text': fig_tit + ch_type_tit,
    'y':0.85,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})


    fig_name=fig_name+ch_type_tit

    qc_derivative = QC_derivative(content=fig, name=fig_name, content_type='plotly')

    return qc_derivative


def edit_legend_pie_SNR(noisy_freqs: list, noise_ampl: list, total_amplitude: float, noise_ampl_relative_to_signal: list):

    """
    Edit the legend for pie chart of signal to noise ratio.

    Parameters
    __________

    noisy_freqs: list
        list of noisy frequencies
    noise_ampl: list
        list of their amplitudes
    total_amplitude: float
        Total amplitude of all frequencies
    noise_ampl_relative_to_signal: list
        list of relative (to entire signal) values of noise freq's amplitude

    Returns
    -------
    noise_and_signal_ampl:
        list of amplitudes of noise freqs + total signal amplitude
    noise_ampl_relative_to_signal:
        list of relative noise freqs + amplitude of clean signal
    bands_names:
        names of freq bands 
    
    """
    

    #Legend for the pie chart:

    bands_names=[]
    if noisy_freqs == [0]:
        noisy_freqs, noise_ampl, noise_ampl_relative_to_signal = [], [], []
        #empty lists so they dont show up on pie chart
    else:
        for fr_n, fr in enumerate(noisy_freqs):
            bands_names.append(str(round(fr,1))+' Hz noise')

    bands_names.append('Main signal')
    
    noise_and_signal_ampl = noise_ampl.copy()
    noise_and_signal_ampl.append(total_amplitude-sum(noise_ampl)) #adding main signal ampl in the list

    noise_ampl_relative_to_signal.append(1-sum(noise_ampl_relative_to_signal)) #adding main signal relative ampl in the list

    return  noise_and_signal_ampl, noise_ampl_relative_to_signal, bands_names


def plot_pie_chart_freq_csv(tsv_pie_path: str, m_or_g: str, noise_or_waves: str):
    
    """
    Plot pie chart representation of relative amplitude of each frequency band over the entire 
    times series of mags or grads, not separated by individual channels.

    Parameters
    ----------
    tsv_pie_path: str
        Path to the tsv file with pie chart data
    m_or_g : str
        'mag' or 'grad'
    noise_or_waves: str
        do we plot SNR or brain waves percentage (alpha, beta, etc)
    
    Returns
    -------
    QC_derivative
        QC_derivative object with plotly figure as content

    """

    #if it s not the right ch kind in the file
    base_name = os.path.basename(tsv_pie_path) #name of the final file
    
    if m_or_g not in base_name.lower():
        return []
    
    # Read the data from the TSV file into a DataFrame
    df = pd.read_csv(tsv_pie_path, sep='\t')

    if noise_or_waves == 'noise' and 'PSDnoise' in base_name:
        #check that we input tsv file with the right data

        fig_tit = "Ratio of signal and noise in the data: " 
        fig_name = 'PSD_SNR_all_channels_'

        # Extract the data
        total_amplitude = df['total_amplitude_'+m_or_g].dropna().iloc[0]  # Get the first non-null value
        noisy_freqs = df['noisy_freqs_'+m_or_g].tolist()

        noise_ampl = df['noise_ampl_'+m_or_g].tolist()
        amplitudes_relative = df['noise_ampl_relative_to_signal_'+m_or_g].tolist()

        amplitudes_abs, amplitudes_relative, bands_names = edit_legend_pie_SNR(noisy_freqs, noise_ampl, total_amplitude, amplitudes_relative)

    elif noise_or_waves == 'waves' and 'PSDwaves' in base_name:

        fig_tit = "Relative area under the amplitude spectrum: " 
        fig_name = 'PSD_Relative_band_amplitude_all_channels_'


        # Set the first column as the index
        df.set_index(df.columns[0], inplace=True)

        # Extract total_amplitude into a separate variable
        total_amplitude = df['total_amplitude'].loc['absolute_'+m_or_g]

        #drop total ampl:
        df_no_total = copy.deepcopy(df.drop('total_amplitude', axis=1))

        # Extract rows into lists
        amplitudes_abs = df_no_total.loc['absolute_'+m_or_g].tolist()
        amplitudes_relative = df_no_total.loc['relative_'+m_or_g].tolist()

        # Extract column names into a separate list
        bands_names = df_no_total.columns.tolist()

    else:
        return []

    all_bands_names=bands_names.copy() 
    #the lists change in this function and this change is tranfered outside the fuction even when these lists are not returned explicitly. 
    #To keep them in original state outside the function, they are copied here.
    all_mean_abs_values=amplitudes_abs.copy()
    ch_type_tit, unit = get_tit_and_unit(m_or_g, psd=True)

    #If mean relative percentages dont sum up into 100%, add the 'unknown' part.
    all_mean_relative_values=[v * 100 for v in amplitudes_relative]  #in percentage
    relative_unknown=100-(sum(amplitudes_relative))*100

    if relative_unknown>0:
        all_mean_relative_values.append(relative_unknown)
        all_bands_names.append('other frequencies')
        all_mean_abs_values.append(total_amplitude - sum(all_mean_abs_values))


    if not all_mean_relative_values:
        return []
    
    labels=[None]*len(all_bands_names)
    for n, name in enumerate(all_bands_names):
        labels[n]=name + ': ' + str("%.2e" % all_mean_abs_values[n]) + ' ' + unit # "%.2e" % removes too many digits after coma

        #if some of the all_mean_abs_values are zero - they should not be shown in pie chart:

    fig = go.Figure(data=[go.Pie(labels=labels, values=all_mean_relative_values)])
    fig.update_layout(
    title={
    'text': fig_tit + ch_type_tit,
    'y':0.85,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})

    fig_name=fig_name+ch_type_tit

    qc_derivative = [QC_derivative(content=fig, name=fig_name, content_type='plotly')]

    return qc_derivative


def assign_epoched_std_ptp_to_channels(what_data, chs_by_lobe, df_std_ptp):

    """
    Assign std or ptp values of each epoch as list to each channel. 
    This is done for easier plotting when need to plot epochs per channel and also color coded by lobes.
    
    Parameters
    ----------
    what_data : str
        'peaks' for peak-to-peak amplitudes or 'stds'
    chs_by_lobe : dict
        dictionary with channel objects sorted by lobe.
    df_std_ptp : pd.DataFrame
        Data Frame containing std or ptp value for each chnnel and each epoch
    
        
    Returns
    -------
    chs_by_lobe : dict
        updated dictionary with channel objects sorted by lobe - with info about std or ptp of epochs.
    """

    if what_data=='peaks':
        #Add the data about std of each epoch (as a list, 1 std for 1 epoch) into each channel object inside the chs_by_lobe dictionary:
        for lobe in chs_by_lobe:
            for ch in chs_by_lobe[lobe]:
                ch.ptp_epoch = df_std_ptp.loc[ch.name].values
    elif what_data=='stds':
        for lobe in chs_by_lobe:
            for ch in chs_by_lobe[lobe]:
                ch.std_epoch = df_std_ptp.loc[ch.name].values
    else:
        print('what_data should be either peaks or stds')

    return chs_by_lobe


def boxplot_epoched_xaxis_epochs(chs_by_lobe: dict, df_std_ptp: pd.DataFrame, ch_type: str, what_data: str):

    """
    Represent std of epochs for each channel as box plots, where each box on x axis is 1 epoch. Dots inside the box are channels.
    
    Process: 
    Each box need to be plotted as a separate trace first.
    Each channels inside each box has to be plottted as separate trace to allow diffrenet color coding
    
    For each box_representing_epoch:
        box trace
        For each color coded lobe:
            For each dot_representing_channel in lobe:
                dot trace

    Add all traces to plotly figure


    Parameters
    ----------
    chs_by_lobe : dict
        dictionary with channel objects sorted by lobe.
    df_std_ptp : pd.DataFrame
        Data Frame containing std or ptp value for each chnnel and each epoch
    ch_type : str
        'mag' or 'grad'
    what_data : str
        'peaks' for peak-to-peak amplitudes or 'stds'

    Returns
    -------
    QC_derivative
        QC_derivative object with plotly figure as content

    """

    epochs_names = df_std_ptp.columns.tolist()

    ch_tit, unit = get_tit_and_unit(ch_type)

    if what_data=='peaks':
        hover_tit='PtP Amplitude'
        y_ax_and_fig_title='Peak-to-peak amplitude'
        fig_name='PP_manual_epoch_per_channel_2_'+ch_tit
    elif what_data=='stds':
        hover_tit='STD'
        y_ax_and_fig_title='Standard deviation'
        fig_name='STD_epoch_per_channel_2_'+ch_tit
    else:
        print('what_data should be either peaks or stds')


    boxwidth=0.5 #the area around which the data dots are scattered depends on the width of the box.

    # For this plot have to separately create a box (no data points plotted) as 1 trace
    # Then separately create for each cannel (dot) a separate trace. It s the only way to make them all different lobe colors.
    # Additionally, the dots are scattered along the x axis inside each box, this is done for visualisation only, x position does not hold information.
    
    # Put all data dots in a list of traces groupped by lobe:
    
    dot_traces = []
    box_traces = []

    for ep_number, ep_name in enumerate(epochs_names):
        dots_in_1_box=[]
        for lobe,  ch_list in chs_by_lobe.items():
            for ch in ch_list:
                if what_data == 'stds':
                    data = ch.std_epoch[ep_number]
                elif what_data == 'peaks':
                    data = ch.ptp_epoch[ep_number]
                dots_in_1_box += [data]

                x = ep_number + random.uniform(-0.2*boxwidth, 0.2*boxwidth) 
                #here create random y values for data dots, they dont have a meaning, just used so that dots are scattered around the box plot and not in 1 line.
                
                dot_traces += [go.Scatter(x=[x], y=[data], mode='markers', marker=dict(size=4, color=ch.lobe_color), opacity=0.8, name=ch.name, text=str(ep_name), legendgroup=ch.lobe, legendgrouptitle=dict(text=lobe.upper()), hovertemplate='Epoch: '+str(ep_name)+'<br>'+hover_tit+': %{y: .2e}')]

        # create box plot trace
        box_traces += [go.Box(x0=ep_number, y=dots_in_1_box, orientation='v', name=ep_name, line_width=1.8, opacity=0.8, boxpoints=False, width=boxwidth, showlegend=False)]
    
    #Collect all traces and add them to the figure:

    all_traces = box_traces+dot_traces
    fig = go.Figure(data=all_traces)
        
    #more settings:
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [v for v in range(0, len(epochs_names))],
            ticktext = epochs_names,
            rangeslider=dict(visible=True)
        ),
        xaxis_title='Experimental epochs',
        yaxis = dict(
            showexponent = 'all',
            exponentformat = 'e'),
        yaxis_title=y_ax_and_fig_title+' in '+unit,
        title={
            'text': y_ax_and_fig_title+' over epochs for '+ch_tit,
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        legend_groupclick='togglegroup') #this setting allowes to select the whole group when clicking on 1 element of the group. But then you can not select only 1 element.

    qc_derivative = QC_derivative(content=fig, name=fig_name, content_type='plotly')

    return qc_derivative


def boxplot_epoched_xaxis_epochs_csv(std_csv_path: str, ch_type: str, what_data: str):

    """
    Represent std of epochs for each channel as box plots, where each box on x axis is 1 epoch. Dots inside the box are channels.
    On base of the data from tsv file
    
    Process: 
    Each box need to be plotted as a separate trace first.
    Each channels inside each box has to be plottted as separate trace to allow diffrenet color coding
    
    For each box_representing_epoch:
        box trace
        For each color coded lobe:
            For each dot_representing_channel in lobe:
                dot trace

    Add all traces to plotly figure


    Parameters
    ----------
    std_csv_path: str
        Path to the tsv file with std data
    ch_type : str
        'mag' or 'grad'
    what_data : str
        'peaks' for peak-to-peak amplitudes or 'stds'

    Returns
    -------
    QC_derivative
        QC_derivative object with plotly figure as content

    """

    # First, get the epochs from csv and convert back into object.
    df = pd.read_csv(std_csv_path, sep='\t')  

    # Figure column names:
    # Create a list of columns that start with 'STD epoch_'
    epoch_columns = [col for col in df.columns if col.startswith('STD epoch_') or col.startswith('PtP epoch_')]

    # Get the number of these columns
    num_epoch_columns = len(epoch_columns)

    # Create a list of numbers from 0 to that length
    epochs_names = [i for i in range(num_epoch_columns)]

    #TODO: here better use the actual epoch names, not recreate their numeration

    ch_tit, unit = get_tit_and_unit(ch_type)

    if what_data=='peaks':
        hover_tit='PtP Amplitude'
        y_ax_and_fig_title='Peak-to-peak amplitude'
        fig_name='PP_manual_epoch_per_channel_2_'+ch_tit
    elif what_data=='stds':
        hover_tit='STD'
        y_ax_and_fig_title='Standard deviation'
        fig_name='STD_epoch_per_channel_2_'+ch_tit
    else:
        print('what_data should be either peaks or stds')


    boxwidth=0.5 #the area around which the data dots are scattered depends on the width of the box.

    # For this plot have to separately create a box (no data points plotted) as 1 trace
    # Then separately create for each cannel (dot) a separate trace. It s the only way to make them all different lobe colors.
    # Additionally, the dots are scattered along the x axis inside each box, this is done for visualisation only, x position does not hold information.
    
    # Put all data dots in a list of traces groupped by lobe:
    
    dot_traces = []
    box_traces = []    

    for ep in epochs_names:
        dots_in_1_box=[]
        for index, row in df.iterrows():

            if row['Type'] == ch_type: #plot only mag/grad

                if what_data == 'stds':
                    data = row['STD epoch_' + str(ep)]
                elif what_data == 'peaks':
                    data = row['PtP epoch_'+ str(ep)]
                else:
                    raise ValueError('what_data should be either peaks or stds')    

                dots_in_1_box += [data]

                x = ep + random.uniform(-0.2*boxwidth, 0.2*boxwidth) 
                #here create random y values for data dots, they dont have a meaning, just used so that dots are scattered around the box plot and not in 1 line.
                
                dot_traces += [go.Scatter(x=[x], y=[data], mode='markers', marker=dict(size=4, color=row['Lobe Color']), opacity=0.8, name=row['Name'], text=str(ep), legendgroup=row['Lobe'], legendgrouptitle=dict(text=row['Lobe'].upper()), hovertemplate='Epoch: '+str(ep)+'<br>'+hover_tit+': %{y: .2e}')]

        # create box plot trace
        box_traces += [go.Box(x0=ep, y=dots_in_1_box, orientation='v', name=ep, line_width=1.8, opacity=0.8, boxpoints=False, width=boxwidth, showlegend=False)]
    
    #Collect all traces and add them to the figure:

    all_traces = box_traces+dot_traces

    if not dot_traces:
        return []
    
    fig = go.Figure(data=all_traces)
        
    #more settings:
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [v for v in range(0, len(epochs_names))],
            ticktext = epochs_names,
            rangeslider=dict(visible=True)
        ),
        xaxis_title='Experimental epochs',
        yaxis = dict(
            showexponent = 'all',
            exponentformat = 'e'),
        yaxis_title=y_ax_and_fig_title+' in '+unit,
        title={
            'text': y_ax_and_fig_title+' over epochs for '+ch_tit,
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        legend_groupclick='togglegroup') #this setting allowes to select the whole group when clicking on 1 element of the group. But then you can not select only 1 element.

    qc_derivative = [QC_derivative(content=fig, name=fig_name, content_type='plotly')]

    return qc_derivative


def boxplot_epochs_old(df_mg: pd.DataFrame, ch_type: str, what_data: str):

    """
    Create representation of calculated data as multiple boxplots: 
    each box represents 1 channel, each dot is std of 1 epoch in this channel
    Implemented with plotly: https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Box.html
    The figure will be saved as an interactive html file.

    Old version, not used.

    Parameters
    ----------
    df_mg : pd.DataFrame
        data frame containing data (stds, peak-to-peak amplitudes, etc) for each epoch, each channel, mags OR grads, not together
    ch_type : str 
        title, like "Magnetometers", or "Gradiometers", 
    what_data : str
        'peaks' for peak-to-peak amplitudes or 'stds'

    Returns
    -------
    QC_derivative
        QC_derivative object with plotly figure as content

    """

    ch_tit, unit = get_tit_and_unit(ch_type)

    if what_data=='peaks':
        hover_tit='Amplitude'
        y_ax_and_fig_title='Peak-to-peak amplitude'
        fig_name='PP_manual_epoch_per_channel_'+ch_tit
    elif what_data=='stds':
        hover_tit='STD'
        y_ax_and_fig_title='Standard deviation'
        fig_name='STD_epoch_per_channel_'+ch_tit

    #collect all names of original df into a list to use as tick labels:
    epochs = df_mg.columns.tolist()

    fig = go.Figure()

    for col in df_mg:
        fig.add_trace(go.Box(y=df_mg[col].values, 
        name=str(df_mg[col].name), 
        opacity=0.7, 
        boxpoints="all", 
        pointpos=0,
        marker_size=3,
        line_width=1,
        text=df_mg[col].index,
        ))
        fig.update_traces(hovertemplate='%{text}<br>'+hover_tit+': %{y: .2e}')

    
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [v for v in range(0, len(epochs))],
            ticktext = epochs,
            rangeslider=dict(visible=True)
        ),
        yaxis = dict(
            showexponent = 'all',
            exponentformat = 'e'),
        yaxis_title=y_ax_and_fig_title+' in '+unit,
        title={
            'text': y_ax_and_fig_title+' of epochs for '+ch_tit,
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        legend_title="Epochs")

    qc_derivative = QC_derivative(content=fig, name=fig_name, content_type='plotly')

    return qc_derivative


def boxplot_all_time_OLD(std_data_named: dict, ch_type: str, channels: list, what_data: str):

    """
    Create representation of calculated std data as a boxplot (box containd magnetometers or gradiomneters, not together): 
    each dot represents 1 channel: name: std value over whole data of this channel. Too high/low stds are outliers.
    OLD but still working version, currently not used. Other principal than the current one so left for reference.

    Parameters
    ----------
    std_data_named : dict
        std values for each channel
    ch_type : str
        'mag' or 'grad'
    channels : list
        list of channel names
    what_data : str
        'peaks' for peak-to-peak amplitudes or 'stds'

    Returns
    -------
    QC_derivative
        QC_derivative object with plotly figure as content

    """
    # Put all values in 1 array from the dictionsry:
    std_data = np.array(list(std_data_named.values()))

    ch_tit, unit = get_tit_and_unit(ch_type)

    if what_data=='peaks':
        hover_tit='PP_Amplitude'
        y_ax_and_fig_title='Peak-to-peak amplitude'
        fig_name='PP_manual_all_data_'+ch_tit
    elif what_data=='stds':
        hover_tit='STD'
        y_ax_and_fig_title='Standard deviation'
        fig_name='STD_epoch_all_data_'+ch_tit

    df = pd.DataFrame (std_data, index=channels, columns=[hover_tit])

    fig = go.Figure()

    fig.add_trace(go.Box(x=df[hover_tit],
    name="",
    text=df[hover_tit].index, 
    opacity=0.7, 
    boxpoints="all", 
    pointpos=0,
    marker_size=5,
    line_width=1))
    fig.update_traces(hovertemplate='%{text}<br>'+hover_tit+': %{x: .0f}')
        

    fig.update_layout(
        yaxis={'visible': False, 'showticklabels': False},
        xaxis = dict(
        showexponent = 'all',
        exponentformat = 'e'),
        xaxis_title=y_ax_and_fig_title+" in "+unit,
        title={
        'text': y_ax_and_fig_title+' of the data for '+ch_tit+' over the entire time series',
        'y':0.85,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
        

    qc_derivative = QC_derivative(content=fig, name=fig_name, content_type='plotly')

    return qc_derivative


def boxplot_all_time(chs_by_lobe: dict, ch_type: str, what_data: str):

    """
    Create representation of calculated std data as a boxplot over the whoe time series, not epoched.
    (box contains magnetometers or gradiomneters, not together): 
    each dot represents 1 channel (std value over whole data of this channel). Too high/low stds are outliers.

    Old version.

    Parameters
    ----------
    chs_by_lobe : dict
        dictionary with channel objects sorted by lobe.
    ch_type : str
        'mag' or 'grad'
    what_data : str
        'peaks' for peak-to-peak amplitudes or 'stds'

    Returns
    -------
    QC_derivative
        QC_derivative object with plotly figure as content

    """

    ch_tit, unit = get_tit_and_unit(ch_type)

    if what_data=='peaks':
        hover_tit='PP_Amplitude'
        y_ax_and_fig_title='Peak-to-peak amplitude'
        fig_name='PP_manual_all_data_'+ch_tit
    elif what_data=='stds':
        hover_tit='STD'
        y_ax_and_fig_title='Standard deviation'
        fig_name='STD_epoch_all_data_'+ch_tit
    else:
        raise ValueError('what_data must be set to "stds" or "peaks"')

    boxwidth=0.4 #the area around which the data dots are scattered depends on the width of the box.

    # For this plot have to separately create a box (no data points plotted) as 1 trace
    # Then separately create for each cannel (dot) a separate trace. It s the only way to make them all different lobe colors.
    # Additionally, the dots are scattered along the y axis, this is done for visualisation only, y position does not hold information.
    
    # Put all data dots in a list of traces groupped by lobe:
    values_all=[]
    traces = []

    for lobe,  ch_list in chs_by_lobe.items():
        for ch in ch_list:
            if what_data == 'stds':
                data = ch.std_overall
            elif what_data == 'peaks':
                data = ch.ptp_overall
            values_all += [data]

            y = random.uniform(-0.2*boxwidth, 0.2*boxwidth) 
            #here create random y values for data dots, they dont have a meaning, just used so that dots are scattered around the box plot and not in 1 line.
            
            traces += [go.Scatter(x=[data], y=[y], mode='markers', marker=dict(size=5, color=ch.lobe_color), name=ch.name, legendgroup=ch.lobe, legendgrouptitle=dict(text=lobe.upper()))]


    # create box plot trace
    box_trace = go.Box(x=values_all, y0=0, orientation='h', name='box', line_width=1, opacity=0.7, boxpoints=False, width=boxwidth, showlegend=False)
    
    #Colllect all traces and add them to the figure:
    all_traces = [box_trace]+traces
    fig = go.Figure(data=all_traces)

    #Add hover text to the dots, remove too many digits after coma.
    fig.update_traces(hovertemplate=hover_tit+': %{x: .2e}')
        
    #more settings:
    fig.update_layout(
        yaxis_range=[-0.5,0.5],
        yaxis={'visible': False, 'showticklabels': False},
        xaxis = dict(
        showexponent = 'all',
        exponentformat = 'e'),
        xaxis_title=y_ax_and_fig_title+" in "+unit,
        title={
        'text': y_ax_and_fig_title+' of the data for '+ch_tit+' over the entire time series',
        'y':0.85,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        legend_groupclick='togglegroup') #this setting allowes to select the whole group when clicking on 1 element of the group. But then you can not select only 1 element.
    

    description_for_user = 'Positions of points on the Y axis do not hold information, made for visialisation only.'
    qc_derivative = QC_derivative(content=fig, name=fig_name, content_type='plotly', description_for_user = description_for_user)

    return qc_derivative


def boxplot_all_time_csv(std_csv_path: str, ch_type: str, what_data: str):

    """
    Create representation of calculated std data as a boxplot over the whoe time series, not epoched.
    (box contains magnetometers or gradiomneters, not together): 
    each dot represents 1 channel (std value over whole data of this channel). Too high/low stds are outliers.

    On base of the data from tsv file.

    Parameters
    ----------
    std_csv_path: str
        Path to the tsv file with std data.
    ch_type : str
        'mag' or 'grad'
    what_data : str
        'peaks' for peak-to-peak amplitudes or 'stds'

    Returns
    -------
    QC_derivative
        QC_derivative object with plotly figure as content

    """

    #First, convert scv back into dict with MEG_channels objects:

    df = pd.read_csv(std_csv_path, sep='\t')  

    ch_tit, unit = get_tit_and_unit(ch_type)

    if what_data=='peaks':
        hover_tit='PP_Amplitude'
        y_ax_and_fig_title='Peak-to-peak amplitude'
        fig_name='PP_manual_all_data_'+ch_tit
    elif what_data=='stds':
        hover_tit='STD'
        y_ax_and_fig_title='Standard deviation'
        fig_name='STD_epoch_all_data_'+ch_tit
    else:
        raise ValueError('what_data must be set to "stds" or "peaks"')

    boxwidth=0.4 #the area around which the data dots are scattered depends on the width of the box.

    # For this plot have to separately create a box (no data points plotted) as 1 trace
    # Then separately create for each cannel (dot) a separate trace. It s the only way to make them all different lobe colors.
    # Additionally, the dots are scattered along the y axis, this is done for visualisation only, y position does not hold information.
    
    # Put all data dots in a list of traces groupped by lobe:
    values_all=[]
    traces = []

    for index, row in df.iterrows():

        if row['Type'] == ch_type: #plot only mag/grad

            if what_data == 'stds':
                data = row['STD all']
            elif what_data == 'peaks':
                data = row['PtP all']

            values_all += [data]

            y = random.uniform(-0.2*boxwidth, 0.2*boxwidth) 
            #here create random y values for data dots, they dont have a meaning, just used so that dots are scattered around the box plot and not in 1 line.
            
            traces += [go.Scatter(x=[data], y=[y], mode='markers', marker=dict(size=5, color=row['Lobe Color']), name=row['Name'], legendgroup=row['Lobe'], legendgrouptitle=dict(text=row['Lobe'].upper()))]


    # create box plot trace
    box_trace = go.Box(x=values_all, y0=0, orientation='h', name='box', line_width=1, opacity=0.7, boxpoints=False, width=boxwidth, showlegend=False)
    
    #Colllect all traces and add them to the figure:
    all_traces = [box_trace]+traces

    if not traces:
        return []
    
    fig = go.Figure(data=all_traces)

    #Add hover text to the dots, remove too many digits after coma.
    fig.update_traces(hovertemplate=hover_tit+': %{x: .2e}')
        
    #more settings:
    fig.update_layout(
        yaxis_range=[-0.5,0.5],
        yaxis={'visible': False, 'showticklabels': False},
        xaxis = dict(
        showexponent = 'all',
        exponentformat = 'e'),
        xaxis_title=y_ax_and_fig_title+" in "+unit,
        title={
        'text': y_ax_and_fig_title+' of the data for '+ch_tit+' over the entire time series',
        'y':0.85,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        legend_groupclick='togglegroup') #this setting allowes to select the whole group when clicking on 1 element of the group. But then you can not select only 1 element.


    description_for_user = 'Positions of points on the Y axis do not hold information, made for visialisation only.'
    qc_derivative = [QC_derivative(content=fig, name=fig_name, content_type='plotly', description_for_user = description_for_user)]

    return qc_derivative


def plot_muscle_csv(f_path: str, m_or_g: str):

    """
    Plot the muscle events with the z-scores and the threshold.
    On base of the data from tsv file.
    
    Parameters
    ----------
    f_path: str
        Path to tsv file with data.
    m_or_g : str
        The channel type used for muscle detection: 'mag' or 'grad'.
    
        
    Returns
    -------
    fig_derivs : list
        A list of QC_derivative objects with plotly figures for muscle events.

    """
    print('___MEGqc___: ', 'f_path', f_path, 'm_or_g', m_or_g)
    df = pd.read_csv(f_path, sep='\t')  

    if df['scores_muscle'].empty or df['scores_muscle'].isna().all():
        return []

    fig_derivs = []

    fig=go.Figure()
    tit, _ = get_tit_and_unit(m_or_g)
    # fig.add_trace(go.Scatter(x=raw.times, y=scores_muscle, mode='lines', name='high freq (muscle scores)'))
    # fig.add_trace(go.Scatter(x=muscle_times, y=high_scores_muscle, mode='markers', name='high freq (muscle) events'))
    
    fig.add_trace(go.Scatter(x=df['data_times'], y=df['scores_muscle'], mode='lines', name='high freq (muscle scores)'))
    fig.add_trace(go.Scatter(x=df['high_scores_muscle_times'], y=df['high_scores_muscle'], mode='markers', name='high freq (muscle) events'))
    
    # #removed threshold, so this one is not plotted now:
    #fig.add_trace(go.Scatter(x=raw.times, y=[threshold_muscle]*len(raw.times), mode='lines', name='z score threshold: '+str(threshold_muscle)))
    fig.update_layout(xaxis_title='time, (s)', yaxis_title='zscore', title={
    'text': "Muscle z scores (high fequency artifacts) over time based on "+tit,
    'y':0.85,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})

    fig_derivs += [QC_derivative(fig, 'muscle_z_scores_over_time_based_on_'+tit, 'plotly', 'Calculation is done using MNE function annotate_muscle_zscore(). It requires a z-score threshold, which can be changed in the settings file. (by defaults 5). Values over this threshold are marked in red.')]
    
    return fig_derivs



def plot_muscle_annotations_mne(raw: mne.io.Raw, m_or_g: str, annot_muscle: mne.Annotations = None, interactive_matplot:bool = False):

    '''
    Currently not used since cant be added into HTML report

    '''
    # View the annotations (interactive_matplot)

    tit, _ = get_tit_and_unit(m_or_g)
    fig_derivs = []
    if interactive_matplot is True:
        order = np.arange(144, 164)
        raw.set_annotations(annot_muscle)
        fig2=raw.plot(start=5, duration=20, order=order)
        #Change settings to show all channels!

        # No suppressing of plots should be done here. This one is matplotlib interactive plot, so it ll only work with %matplotlib qt.
        # Makes no sense to suppress it. Also, adding to QC_derivative is just formal, cos whe extracting to html it s not interactive any more. 
        # Should not be added to report. Kept here in case mne will allow to extract interactive later.

        fig_derivs += [QC_derivative(fig2, 'muscle_annotations_'+tit, 'matplotlib')]
    
    return fig_derivs


def make_head_pos_plot_old(raw: mne.io.Raw, head_pos: np.ndarray):

    """ 
    Plot positions and rotations of the head.
    
    Parameters
    ----------
    raw : mne.io.Raw
        Raw data.
    head_pos : np.ndarray
        Head positions and rotations.
        
    Returns
    -------
    head_derivs : list 
        List of QC_derivative objects containing figures with head positions and rotations.
    head_pos_baselined : np.ndarray
        Head positions and rotations starting from 0 instead of the mne detected starting point. Can be used for plotting.
    """

    head_derivs = []

    original_head_dev_t = mne.transforms.invert_transform(
        raw.info['dev_head_t'])
    average_head_dev_t = mne.transforms.invert_transform(
        compute_average_dev_head_t(raw, head_pos))


    matplotlib.use('Agg') #this command will suppress showing matplotlib figures produced by mne. They will still be saved for use in report but not shown when running the pipeline

    #plot using MNE:
    fig1 = mne.viz.plot_head_positions(head_pos, mode='traces')
    #fig1 = mne.viz.plot_head_positions(head_pos_degrees)
    for ax, val, val_ori in zip(fig1.axes[::2], average_head_dev_t['trans'][:3, 3],
                        original_head_dev_t['trans'][:3, 3]):
        ax.axhline(1000*val, color='r')
        ax.axhline(1000*val_ori, color='g')
        #print('___MEGqc___: ', 'val', val, 'val_ori', val_ori)
    # The green horizontal lines represent the original head position, whereas the
    # Red lines are the new head position averaged over all the time points.


    head_derivs += [QC_derivative(fig1, 'Head_position_rotation_average_mne', 'matplotlib', description_for_user = 'The green horizontal lines - original head position. Red lines - the new head position averaged over all the time points.')]


    #plot head_pos using PLOTLY:

    # First, for each head position subtract the first point from all the other points to make it always deviate from 0:
    head_pos_baselined=head_pos.copy()
    #head_pos_baselined=head_pos_degrees.copy()
    for i, pos in enumerate(head_pos_baselined.T[1:7]):
        pos -= pos[0]
        head_pos_baselined.T[i]=pos

    t = head_pos.T[0]

    average_head_pos=average_head_dev_t['trans'][:3, 3]
    original_head_pos=original_head_dev_t['trans'][:3, 3]

    fig1p = make_subplots(rows=3, cols=2, subplot_titles=("Position (mm)", "Rotation (quat)"))

    # head_pos ndarray of shape (n_pos, 10): [t, q1, q2, q3, x, y, z, gof, err, v]
    # https://mne.tools/stable/generated/mne.chpi.compute_head_pos.html
    indexes=[4, 5, 6, 1, 2,3]
    names=['x', 'y', 'z', 'q1', 'q2', 'q3']
    for counter in [0, 1, 2]:
        position=1000*-head_pos.T[indexes][counter]
        #position=1000*-head_pos_baselined.T[indexes][counter]
        name_pos=names[counter]
        fig1p.add_trace(go.Scatter(x=t, y=position, mode='lines', name=name_pos), row=counter+1, col=1)
        fig1p.update_yaxes(title_text=name_pos, row=counter+1, col=1)
        #print('name', name_pos, 'position', position)
        rotation=head_pos.T[indexes][counter+3]
        #rotation=head_pos_baselined.T[indexes][counter+3]
        name_rot=names[counter+3]
        fig1p.add_trace(go.Scatter(x=t, y=rotation, mode='lines', name=name_rot), row=counter+1, col=2)
        fig1p.update_yaxes(title_text=name_rot, row=counter+1, col=2)
        #print('name', name_rot, 'rotation', rotation)

        # fig1p.add_hline(y=1000*average_head_pos[counter], line_dash="dash", line_color="red", row=counter+1, col=1)
        # fig1p.add_hline(y=1000*original_head_pos[counter], line_dash="dash", line_color="green", row=counter+1, col=1)

    fig1p.update_xaxes(title_text='Time (s)', row=3, col=1)
    fig1p.update_xaxes(title_text='Time (s)', row=3, col=2)

    head_derivs += [QC_derivative(fig1p, 'Head_position_rotation_average_plotly', 'plotly', description_for_user = 'The green horizontal lines - original head position. Red lines - the new head position averaged over all the time points.')]

    return head_derivs, head_pos_baselined

    
def make_head_pos_plot_csv(f_path: str):

    """ 
    Plot positions and rotations of the head. On base of data from tsv file.
    
    Parameters
    ----------
    f_path: str
        Path to a file with data.
        
    Returns
    -------
    head_derivs : list 
        List of QC_derivative objects containing figures with head positions and rotations.
    head_pos_baselined : np.ndarray
        Head positions and rotations starting from 0 instead of the mne detected starting point. Can be used for plotting.
    """

    head_pos = pd.read_csv(f_path, sep='\t') 

    #drop first column. cos index is being created as an extra column when transforming from csv back to df:
    head_pos.drop(columns=head_pos.columns[0], axis=1, inplace=True)

    # Check if all specified columns are empty or contain only NaN values
    columns_to_check = ['x', 'y', 'z', 'q1', 'q2', 'q3']
    if head_pos[columns_to_check].isna().all().all() or head_pos[columns_to_check].empty:
        return [],[]

    #plot head_pos using PLOTLY:

    # First, for each head position subtract the first point from all the other points to make it always deviate from 0:
    head_pos_baselined=head_pos.copy()
    #head_pos_baselined=head_pos_degrees.copy()
    for column in ['x', 'y', 'z', 'q1', 'q2', 'q3']:
        head_pos_baselined[column] -= head_pos_baselined[column][0]

    t = head_pos['t']

    fig1p = make_subplots(rows=3, cols=2, subplot_titles=("Position (mm)", "Rotation (quat)"))

    names_pos=['x', 'y', 'z']
    names_rot=['q1', 'q2', 'q3']
    for counter in [0, 1, 2]:
        position=1000*-head_pos[names_pos[counter]]
        #position=1000*-head_pos_baselined[names_pos[counter]]
        fig1p.add_trace(go.Scatter(x=t, y=position, mode='lines', name=names_pos[counter]), row=counter+1, col=1)
        fig1p.update_yaxes(title_text=names_pos[counter], row=counter+1, col=1)
        rotation=head_pos[names_rot[counter]]
        #rotation=head_pos_baselined[names_rot[counter]]
        fig1p.add_trace(go.Scatter(x=t, y=rotation, mode='lines', name=names_rot[counter]), row=counter+1, col=2)
        fig1p.update_yaxes(title_text=names_rot[counter], row=counter+1, col=2)

    fig1p.update_xaxes(title_text='Time (s)', row=3, col=1)
    fig1p.update_xaxes(title_text='Time (s)', row=3, col=2)

    head_derivs = [QC_derivative(fig1p, 'Head_position_rotation_average_plotly', 'plotly', description_for_user = 'The green horizontal lines - original head position. Red lines - the new head position averaged over all the time points.')]

    return head_derivs, head_pos_baselined


def make_head_pos_plot_mne(raw: mne.io.Raw, head_pos: np.ndarray):

    """

    Currently not used if we wanna plot solely from csv. 
    This function requires also raw as input and cant be only from csv.

    TODO: but we can calculate these inputs earlier and add them to csv as well.

    """

    original_head_dev_t = mne.transforms.invert_transform(
        raw.info['dev_head_t'])
    average_head_dev_t = mne.transforms.invert_transform(
        compute_average_dev_head_t(raw, head_pos))
    
    matplotlib.use('Agg') #this command will suppress showing matplotlib figures produced by mne. They will still be saved for use in report but not shown when running the pipeline

    #plot using MNE:
    fig1 = mne.viz.plot_head_positions(head_pos, mode='traces')
    #fig1 = mne.viz.plot_head_positions(head_pos_degrees)
    for ax, val, val_ori in zip(fig1.axes[::2], average_head_dev_t['trans'][:3, 3],
                        original_head_dev_t['trans'][:3, 3]):
        ax.axhline(1000*val, color='r')
        ax.axhline(1000*val_ori, color='g')
        #print('___MEGqc___: ', 'val', val, 'val_ori', val_ori)
    # The green horizontal lines represent the original head position, whereas the
    # Red lines are the new head position averaged over all the time points.


    head_derivs = [QC_derivative(fig1, 'Head_position_rotation_average_mne', 'matplotlib', description_for_user = 'The green horizontal lines - original head position. Red lines - the new head position averaged over all the time points.')]

    return head_derivs


def make_head_annots_plot(raw: mne.io.Raw, head_pos: np.ndarray):

    """
    Plot raw data with annotated head movement. Currently not used.

    
    Parameters
    ----------
    raw : mne.io.Raw
        Raw data.
    head_pos : np.ndarray
        Head positions and rotations.
        
    Returns
    -------
    head_derivs : list
        List of QC derivatives with annotated figures.
        
    """

    head_derivs = []

    mean_distance_limit = 0.0015  # in meters
    annotation_movement, hpi_disp = annotate_movement(
        raw, head_pos, mean_distance_limit=mean_distance_limit)
    raw.set_annotations(annotation_movement)
    fig2=raw.plot(n_channels=100, duration=20)
    head_derivs += [QC_derivative(fig2, 'Head_position_annot', 'matplotlib')]

    return head_derivs

#__________ECG/EOG__________#

def plot_ECG_EOG_channel(ch_data: np.ndarray or list, peaks: np.ndarray or list, ch_name: str, fs: float):

    """
    Plot the ECG channel data and detected peaks
    
    Parameters
    ----------
    ch_data : list or np.ndarray
        Data of the channel
    peaks : list or np.ndarray
        Indices of the peaks in the data
    ch_name : str
        Name of the channel
    fs : int
        Sampling frequency of the data
        
    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plot of the channel data and detected peaks
        
    """

    time = np.arange(len(ch_data))/fs
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=ch_data, mode='lines', name=ch_name,
        hovertemplate='Time: %{x} s<br>Amplitude: %{y} V<br>'))
    fig.add_trace(go.Scatter(x=time[peaks], y=ch_data[peaks], mode='markers', name='peaks',
        hovertemplate='Time: %{x} s<br>Amplitude: %{y} V<br>'))
    fig.update_layout(xaxis_title='time, s', 
                yaxis = dict(
                showexponent = 'all',
                exponentformat = 'e'),
                yaxis_title='Amplitude, V',
                title={
                'text': ch_name,
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})


    return fig


def plot_ECG_EOG_channel_csv(f_path):

    """
    Plot the ECG channel data and detected peaks
    
    Parameters
    ----------
    f_path : str
        Path to the tsv file with the derivs to plot
        
    Returns
    -------
    ch_deriv : list
        List of QC_derivative objects with plotly figures of the ECG/EOG channels
        
    """

    #if its not the right file, skip:
    base_name = os.path.basename(f_path) #name of the fimal file
    
    if 'ecgchannel' not in base_name.lower() and 'eogchannel' not in base_name.lower():
        return []

    df = pd.read_csv(f_path, sep='\t', dtype={6: str}) 

    #name of the first column if it starts with 'ECG' or 'EOG':
    ch_name = df.columns[1]
    ch_data = df[ch_name].values

    if not ch_data.any():  # Check if all values are falsy (0, False, or empty)
        return []
    
    peaks = df['event_indexes'].dropna()
    peaks = [int(x) for x in peaks]
    fs = int(df['fs'].dropna().iloc[0])

    time = np.arange(len(ch_data))/fs
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=ch_data, mode='lines', name=ch_name,
                             hovertemplate='Time: %{x} s<br>Amplitude: %{y} V<br>'))
    fig.add_trace(go.Scatter(x=time[peaks], y=ch_data[peaks], mode='markers', name='peak',
                             hovertemplate='Time: %{x} s<br>Amplitude: %{y} V<br>'))
    fig.update_layout(xaxis_title='time, s', 
                yaxis = dict(
                showexponent = 'all',
                exponentformat = 'e'),
                yaxis_title='Amplitude, V',
                title={
                'text': ch_name,
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
    
    ch_deriv = [QC_derivative(fig, ch_name, 'plotly', fig_order = 1)]

    return ch_deriv


def figure_x_axis(df, metric):

    ''''
    Get the x axis for the plot based on the metric.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data frame with the data.
    metric : str
        The metric for which the x axis is needed. Can be 'PSD', 'ECG', 'EOG', 'Muscle', 'Head'.

    Returns
    -------
    freqs : np.ndarray
        Frequencies for the PSD plot.
    time_vec : np.ndarray
        Time vector for the ECG, EOG, Muscle, Head plots.
    
    '''
     
    if metric.lower() == 'psd':
        # Figure out frequencies:
        freq_cols = [column for column in df if column.startswith('PSD_Hz_')]
        freqs = np.array([float(x.replace('PSD_Hz_', '')) for x in freq_cols])
        return freqs
    
    elif metric.lower() == 'eog' or metric.lower() == 'ecg' or metric.lower() == 'muscle' or metric.lower() == 'head':
        if metric.lower() == 'ecg':
            prefix = 'mean_ecg_sec_'
        elif metric.lower() == 'eog': 
            prefix = 'mean_eog_sec_'
        elif metric.lower() == 'smoothed_ecg' or metric.lower() == 'ecg_smoothed':
            prefix = 'smoothed_mean_ecg_sec_'
        elif metric.lower() == 'smoothed_eog' or metric.lower() == 'eog_smoothed':
            prefix = 'smoothed_mean_eog_sec_'
        elif metric.lower() == 'muscle':
            prefix = 'Muscle_sec_'
        elif metric.lower() == 'head':
            prefix = 'Head_sec_'
        
        time_cols = [column for column in df if column.startswith(prefix)]
        time_vec = np.array([float(x.replace(prefix, '')) for x in time_cols])

        return time_vec
    
    else:
        print('Oh well IDK! figure_x_axis()')
        return None
    

def split_affected_into_3_groups_csv(df: pd.DataFrame, metric: str, split_by: str = 'similarity_score' or 'corr_coeff'):

    """
    Collect artif_per_ch into 3 lists - for plotting:
    - a third of all channels that are the most correlated with mean_rwave
    - a third of all channels that are the least correlated with mean_rwave
    - a third of all channels that are in the middle of the correlation with mean_rwave

    Parameters
    ----------
    df: pd.DataFrame
        Data frame with the data.
    metric : str
        The metric for which the x axis is needed. Can be 'ECG' or 'EOG'.
    split_by : str
        The metric by which the channels will be split. Can be 'corr_coeff' or 'similarity_score'.

    Returns
    -------
    artif_per_ch : list
        List of objects of class Avg_artif, ranked by correlation coefficient
    most_correlated : list
        List of objects of class Avg_artif that are the most correlated with mean_rwave
    least_correlated : list
        List of objects of class Avg_artif that are the least correlated with mean_rwave
    middle_correlated : list
        List of objects of class Avg_artif that are in the middle of the correlation with mean_rwave
    corr_val_of_last_least_correlated : float
        Correlation value of the last channel in the list of the least correlated channels
    corr_val_of_last_middle_correlated : float
        Correlation value of the last channel in the list of the middle correlated channels
    corr_val_of_last_most_correlated : float
        Correlation value of the last channel in the list of the most correlated channels


    """

    if metric.lower() != 'ecg' and metric.lower() != 'eog':
        print('Wrong metric in split_affected_into_3_groups_csv()')

    #sort the data frame by the correlation coefficient or similarity score and split into 3 groups:
    df_sorted = df.reindex(df[metric.lower()+'_'+split_by].abs().sort_values(ascending=False).index)

    total_rows = len(df_sorted)
    third = total_rows // 3

    most_affected = df_sorted.copy()[:third]
    middle_affected = df_sorted.copy()[third:2*third]
    least_affected = df_sorted.copy()[2*third:]

    #find the correlation value of the last channel in the list of the most correlated channels:
    # this is needed for plotting correlation values, to know where to put separation rectangles.
    val_of_last_most_affected = max(most_affected[metric.lower()+'_'+split_by].abs().tolist())
    val_of_last_middle_affected = max(middle_affected[metric.lower()+'_'+split_by].abs().tolist())
    val_of_last_least_affected = max(least_affected[metric.lower()+'_'+split_by].abs().tolist())

    return most_affected, middle_affected, least_affected, val_of_last_most_affected, val_of_last_middle_affected, val_of_last_least_affected


def plot_affected_channels_csv(df, artifact_lvl: float, t: np.ndarray, m_or_g: str, ecg_or_eog: str, title: str, flip_data: bool or str = 'flip', smoothed: bool = False):

    """
    Plot the mean artifact amplitude for all affected (not affected) channels in 1 plot together with the artifact_lvl.
    Based on the data from tsv file.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data frame with the data.
    artifact_lvl : float
        The threshold for the artifact amplitude.
    t : np.ndarray
        Time vector.
    m_or_g : str
        Either 'mag' or 'grad'.
    ecg_or_eog : str
        Either 'ECG' or 'EOG'.
    title : str
        The title of the figure.
    flip_data : bool
        If True, the absolute value of the data will be used for the calculation of the mean artifact amplitude. Default to 'flip'. 
        'flip' means that the data will be flipped if the peak of the artifact is negative. 
        This is donr to get the same sign of the artifact for all channels, then to get the mean artifact amplitude over all channels and the threshold for the artifact amplitude onbase of this mean
        And also for the reasons of visualization: the artifact amplitude is always positive.
    smoothed: bool
        Plot smoothed data (true) or nonrmal (false)

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The plotly figure with the mean artifact amplitude for all affected (not affected) channels in 1 plot together with the artifact_lvl.

        
    """

    fig_tit=ecg_or_eog.upper()+title

    if df is not None:
        if smoothed is True:
            metric = ecg_or_eog+'_smoothed'
        elif smoothed is False:
            metric = ecg_or_eog
        fig = plot_df_of_channels_data_as_lines_by_lobe_csv(None, metric, t, m_or_g, df)

        if fig is None:
            return go.Figure()

        #decorate the plot:
        ch_type_tit, unit = get_tit_and_unit(m_or_g)
        fig.update_layout(
            xaxis_title='Time in seconds',
            yaxis = dict(
                showexponent = 'all',
                exponentformat = 'e'),
            yaxis_title='Mean magnitude in '+unit,
            title={
                'text': fig_tit+str(len(df))+' '+ch_type_tit,
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})


    else:
        fig=go.Figure()
        ch_type_tit, _ = get_tit_and_unit(m_or_g)
        title=fig_tit+'0 ' +ch_type_tit
        fig.update_layout(
            title={
            'text': title,
            'x': 0.5,
            'y': 0.9,
            'xanchor': 'center',
            'yanchor': 'top'})
        
    #in any case - add the threshold on the plot
    #TODO: remove threshold?
    fig.add_trace(go.Scatter(x=t, y=[(artifact_lvl)]*len(t), line=dict(color='red'), name='Thres=mean_peak/norm_lvl')) #add threshold level

    if flip_data is False and artifact_lvl is not None: 
        fig.add_trace(go.Scatter(x=t, y=[(-artifact_lvl)]*len(t), line=dict(color='black'), name='-Thres=mean_peak/norm_lvl'))

    return fig


def plot_mean_rwave_csv(f_path: str, ecg_or_eog: str):

    """
    Plon mean rwave(ECG) or mean blink (EOG) from data in CSV file.


    Parameters
    ----------
    f_path: str
        Path to csv file
    ecg_or_eog: str
        plot ECG or EOG data

    Returns
    -------
    fig_derivs : list
        list with one QC_derivative object, which contains the plot.


    """

    #if it s not the right ch kind in the file
    base_name = os.path.basename(f_path) #name of the final file
    if ecg_or_eog.lower() + 'channel' not in base_name.lower():
        return []

    # Load the data from the .tsv file into a DataFrame
    df = pd.read_csv(f_path, sep='\t', dtype={6: str})

    if df['mean_rwave'].empty or df['mean_rwave'].isna().all():
        return []

    # Set the plot's title and labels
    if 'recorded' in df['recorded_or_reconstructed'][0].lower():
        which = ' recorded'
    elif 'reconstructed' in df['recorded_or_reconstructed'][0].lower():
        which = ' reconstructed'
    else:
        which = ''
    
    #TODO: can there be the case that no shift was done and column is empty? should not be...
    # Create a scatter plot
    fig = go.Figure()
    fig.add_trace(go.Scatter (x=df['mean_rwave_time'], y=df['mean_rwave'], mode='lines', name='Original '+ ecg_or_eog.upper(),
        hovertemplate='Time: %{x} s<br>Amplitude: %{y} V<br>'))
    if ecg_or_eog.lower() == 'ecg':
        fig.add_trace(go.Scatter (x=df['mean_rwave_time'], y=df['mean_rwave_shifted'], mode='lines', name='Shifted ' + ecg_or_eog.upper(),
        hovertemplate='Time: %{x} s<br>Amplitude: %{y} V<br>'))

    if ecg_or_eog.lower() == 'ecg':
        plot_tit = 'Mean' + which + ' R wave was shifted to align with the ' + ecg_or_eog.upper() + ' signal found on MEG channels.'
        annot_text = "The alignment is necessary for performing Pearson correlation between ECG signal found in each channel and reference mean signal of the ECG recording."
    elif ecg_or_eog.lower() == 'eog':
        plot_tit = 'Mean' + which + ' blink signal'
        annot_text = ""

    fig.update_layout(
            xaxis_title='Time, s',
            yaxis = dict(
                showexponent = 'all',
                exponentformat = 'e'),
            yaxis_title='Amplitude, V',
            title={
                'text': plot_tit,
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            annotations=[
                dict(
                x=0.5,
                y=-0.25,
                showarrow=False,
                text=annot_text,
                xref="paper",
                yref="paper",
                font=dict(size=12),
                align="center"
        )])

    mean_ecg_eog_ch_deriv = [QC_derivative(fig, ecg_or_eog+'mean_ch_data', 'plotly', fig_order = 2)]

    return mean_ecg_eog_ch_deriv


def plot_artif_per_ch_correlated_lobes_csv(f_path: str, m_or_g: str, ecg_or_eog: str, flip_data: bool):

    """
    This is the final function.
    Plot average artifact for each channel, colored by lobe, 
    channels are split into 3 separate plots, based on their correlation with mean_rwave: equal number of channels in each group.
    Based on the data from tsv file.

    Parameters
    ----------
    f_path : str
        Path to the tsv file with data.
    m_or_g : str
        Type of the channel: mag or grad
    ecg_or_eog : str
        Type of the artifact: ECG or EOG
    flip_data : bool
        Use True or False, doesnt matter here. It is only passed into the plotting function and influences the threshold presentation. But since treshold is not used in correlation method, this is not used.

    Returns
    -------
    artif_per_ch : list
        List of objects of class Avg_artif
    affected_derivs : list
        List of objects of class QC_derivative (plots)
    

    """

    #if its not the right file, skip:
    base_name = os.path.basename(f_path) #name of the fimal file
    
    if 'desc-ecgs' not in base_name.lower() and 'desc-eogs' not in base_name.lower():
        return []


    ecg_or_eog = ecg_or_eog.lower()

    df = pd.read_csv(f_path, sep='\t') #TODO: maybe remove reading csv and pass directly the df here?
    
    df = df.drop(df[df['Type'] != m_or_g].index) #remove non needed channel kind

    artif_time_vector = figure_x_axis(df, metric=ecg_or_eog)

    most_similar, mid_similar, least_similar, _, _, _ = split_affected_into_3_groups_csv(df, ecg_or_eog, split_by='similarity_score')

    smoothed = True
    fig_most_affected = plot_affected_channels_csv(most_similar, None, artif_time_vector, m_or_g, ecg_or_eog, title = ' most affected channels (smoothed): ', flip_data=flip_data, smoothed = smoothed)
    fig_middle_affected = plot_affected_channels_csv(mid_similar, None, artif_time_vector, m_or_g, ecg_or_eog, title = ' moderately affected channels (smoothed): ', flip_data=flip_data, smoothed = smoothed)
    fig_least_affected = plot_affected_channels_csv(least_similar, None, artif_time_vector, m_or_g, ecg_or_eog, title = ' least affected channels (smoothed): ', flip_data=flip_data, smoothed = smoothed)


    #set the same Y axis limits for all 3 figures for clear comparison:

    if ecg_or_eog.lower() == 'ecg' and smoothed is False:
        prefix = 'mean_ecg_sec_'
    elif ecg_or_eog.lower() == 'ecg' and smoothed is True:
        prefix = 'smoothed_mean_ecg_sec_'
    elif ecg_or_eog.lower() == 'eog' and smoothed is False:
        prefix = 'mean_eog_sec_'
    elif ecg_or_eog.lower() == 'eog' and smoothed is True:
        prefix = 'smoothed_mean_eog_sec_'

    cols = [column for column in df if column.startswith(prefix)]
    cols = ['Name']+cols

    limits_df = df[cols]

    ymax = limits_df.loc[:, limits_df.columns != 'Name'].max().max()
    ymin = limits_df.loc[:, limits_df.columns != 'Name'].min().min()

    ylim = [ymin*.95, ymax*1.05]

    # update the layout of all three figures with the same y-axis limits
    fig_most_affected.update_layout(yaxis_range=ylim)
    fig_middle_affected.update_layout(yaxis_range=ylim)
    fig_least_affected.update_layout(yaxis_range=ylim)
    
    m_or_g_order = 0.1 if m_or_g == 'mag' else 0.2
    affected_derivs = []
    affected_derivs += [QC_derivative(fig_most_affected, ecg_or_eog+'most_affected_channels_'+m_or_g, 'plotly', fig_order = 3.01+m_or_g_order)] #for exaple for mage we get: 3.11
    affected_derivs += [QC_derivative(fig_middle_affected, ecg_or_eog+'middle_affected_channels_'+m_or_g, 'plotly', fig_order = 3.02+m_or_g_order)]
    affected_derivs += [QC_derivative(fig_least_affected, ecg_or_eog+'least_affected_channels_'+m_or_g, 'plotly', fig_order = 3.03+m_or_g_order)]

   
    return affected_derivs


def plot_correlation_csv(f_path: str, ecg_or_eog: str, m_or_g: str):

    """
    Plot correlation coefficient and p-value between mean R wave and each channel in artif_per_ch.
    Based on the data from tsv file.

    Parameters
    ----------
    f_path : str
        Path to the tsv file with data.
    ecg_or_eog : str
        Either 'ECG' or 'EOG'.
    m_or_g : str
        Either 'mag' or 'grad'.

    Returns
    -------
    corr_derivs : list
        List with 1 QC_derivative instance: Figure with correlation coefficient and p-value between mean R wave and each channel in artif_per_ch.
    
    """

    #if its not the right file, skip:
    base_name = os.path.basename(f_path) #name of the fimal file
    
    if 'desc-ecgs' not in base_name.lower() and 'desc-eogs' not in base_name.lower():
        return []

    ecg_or_eog = ecg_or_eog.lower()

    df = pd.read_csv(f_path, sep='\t') #TODO: maybe remove reading csv and pass directly the df here?
    df = df.drop(df[df['Type'] != m_or_g].index) #remove non needed channel kind

    _, _, _, corr_val_of_last_most_correlated, corr_val_of_last_middle_correlated, corr_val_of_last_least_correlated = split_affected_into_3_groups_csv(df, ecg_or_eog, split_by='corr_coeff')

    traces = []

    tit, _ = get_tit_and_unit(m_or_g)

    # for index, row in df.iterrows():
    #     traces += [go.Scatter(x=[abs(row[ecg_or_eog.lower()+'_corr_coeff'])], y=[row[ecg_or_eog.lower()+'_pval']], mode='markers', marker=dict(size=5, color=row['Lobe Color']), name=row['Name'], legendgroup=row['Lobe Color'], legendgrouptitle=dict(text=row['Lobe'].upper()), hovertemplate='Corr coeff: '+str(row[ecg_or_eog.lower()+'_corr_coeff'])+'<br>p-value: '+str(abs(row[ecg_or_eog.lower()+'_pval'])))]


    for index, row in df.iterrows():
        traces += [go.Scatter(x=[abs(row[ecg_or_eog.lower()+'_corr_coeff'])], y=[row[ecg_or_eog.lower()+'_pval']], mode='markers', marker=dict(size=5, color=row['Lobe Color']), name=row['Name'], legendgroup=row['Lobe Color'], legendgrouptitle=dict(text=row['Lobe'].upper()), hovertemplate='Corr coeff: '+str(row[ecg_or_eog.lower()+'_corr_coeff'])+'<br>p-value: '+str(abs(row[ecg_or_eog.lower()+'_pval'])))]

    if not traces:
        return []
    
    # Create the figure with the traces
    fig = go.Figure(data=traces)

    # # Reverse the x and y axes
    # fig.update_xaxes(autorange="reversed")
    # fig.update_yaxes(autorange="reversed")


    fig.add_shape(type="rect", xref="x", yref="y", x0=0, y0=-0.1, x1=corr_val_of_last_least_correlated, y1=1.1, line=dict(color="Green", width=2), fillcolor="Green", opacity=0.1)
    fig.add_shape(type="rect", xref="x", yref="y", x0=corr_val_of_last_least_correlated, y0=-0.1, x1=corr_val_of_last_middle_correlated, y1=1.1, line=dict(color="Yellow", width=2), fillcolor="Yellow", opacity=0.1)
    fig.add_shape(type="rect", xref="x", yref="y", x0=corr_val_of_last_middle_correlated, y0=-0.1, x1=1, y1=1.1, line=dict(color="Red", width=2), fillcolor="Red", opacity=0.1)

    fig.update_layout(
        title={
            'text': tit+': Pearson correlation between reference '+ecg_or_eog.upper()+' epoch and '+ecg_or_eog.upper()+' epoch in each channel',
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title='Correlation coefficient',
        yaxis_title = 'P-value')

    m_or_g_order = 0.1 if m_or_g == 'mag' else 0.2
    corr_derivs = [QC_derivative(fig, 'Corr_values_'+ecg_or_eog, 'plotly', description_for_user='Absolute value of the correlation coefficient is shown here. The sign would only represent the position of the channel towards magnetic field. <p>- Green: 33% of all channels that have the weakest correlation with mean ' +ecg_or_eog +'; </p> <p>- Yellow: 33% of all channels that have mild correlation with mean ' +ecg_or_eog +';</p> <p>- Red: 33% of all channels that have the stronges correlation with mean ' +ecg_or_eog +'. </p>', fig_order = 4+m_or_g_order)]

    return corr_derivs


def plot_mean_rwave_shifted(mean_rwave_shifted: np.ndarray, mean_rwave: np.ndarray, ecg_or_eog: str, tmin: float, tmax: float):
    
    """
    Only for demonstartion while running the pipeline. Dpesnt go into final report.

    Plots the mean ECG wave and the mean ECG wave shifted to align with the ECG artifacts found on meg channels.
    Probably will not be included into the report. Just for algorythm demosntration.
    The already shifted mean ECG wave is plotted in the report.

    Parameters
    ----------
    mean_rwave_shifted : np.ndarray
        The mean ECG wave shifted to align with the ECG artifacts found on meg channels.
    mean_rwave : np.ndarray
        The mean ECG wave, not shifted, original.
    ecg_or_eog : str
        'ECG' or 'EOG'
    tmin : float
        The start time of the epoch.
    tmax : float
        The end time of the epoch.

    Returns
    -------
    fig_derivs : list
        list with one QC_derivative object, which contains the plot. (in case want to input intot he report)
    
    """

    t = np.linspace(tmin, tmax, len(mean_rwave_shifted))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=mean_rwave_shifted, mode='lines', name='mean_rwave_shifted'))
    fig.add_trace(go.Scatter(x=t, y=mean_rwave, mode='lines', name='mean_rwave'))

    fig.show()

    #fig_derivs = [QC_derivative(fig, 'Mean_artifact_'+ecg_or_eog+'_shifted', 'plotly')] 
    # #activate is you want to output the shift demonstration to the report, normally dont'
    
    fig_derivs = []

    return fig_derivs