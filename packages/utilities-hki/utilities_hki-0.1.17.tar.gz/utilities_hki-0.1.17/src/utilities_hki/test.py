# -*- coding: utf-8 -*-
"""
DO NOT FORGET to change back the relative import of db_utils in analy_utils

@author: FranciscoPena
"""

import pandas as pd, numpy as np
import db_utils

# GET CREDENTIALS ++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os, sys, git
git_root = git.Repo(os.path.abspath(__file__),
                    search_parent_directories=True).git.rev_parse('--show-toplevel')
cred_path = os.path.join(git_root, '../credentials')
sys.path.append(cred_path)
import credentials as cred

db_dict = cred.humankind_datascience

#%% get data

query = """
SELECT *
FROM ips
"""
df = db_utils.get_data('hkiproc', db_dict, query)