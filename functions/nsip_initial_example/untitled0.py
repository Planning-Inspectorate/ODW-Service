# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:37:21 2023

@author: JonesZofia
"""

import pandas as pd

df=pd.read_csv(r'C:\Users\JonesZofia\OneDrive - Planning Inspectorate\Documents\fact_timesheet_combined_07092023.csv')

df['appeal_reference_number_prefix'] = df['appeal_reference_number'].str.replace('[0-9]','')

df['unmapped_timesheet_job_reference_prefix'] = df['unmapped_timesheet_job_reference'].str.replace('[0-9]','')