#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Simone Boglio
"""

import os, pickle
import pandas as pd
import Data_manager.Utility as ut
import numpy as np

from Data_manager.DataReader_utils import downloadFromURL
from Data_manager.load_and_save_data import save_data_dict, load_data_dict

from Data_manager.IncrementalSparseMatrix import IncrementalSparseMatrix
from Data_manager.split_functions.split_train_validation import split_train_validation_percentage_user_wise


class AmazonInstantVideoReader:
    DATASET_URL = "http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Amazon_Instant_Video.csv"
    DATASET_SPLIT_ROOT_FOLDER = "Data_manager_split_datasets/"
    DATASET_SUBFOLDER = "AmazonInstantVideo/"

    def __init__(self):

        test_percentage = 0.2
        validation_percentage = 0.2

        pre_splitted_path = "Data_manager_split_datasets/AmazonInstantVideo/RecSys/SpectralCF_our_interface/"
        pre_splitted_filename = "splitted_data"

        ratings_file_name = "ratings_Amazon_Instant_Video.csv"

        # If directory does not exist, create
        if not os.path.exists(pre_splitted_path):
            os.makedirs(pre_splitted_path)

        try:
            print("Dataset_AmazonInstantVideo: Attempting to load pre-splitted data")

            for attrib_name, attrib_object in load_data_dict(pre_splitted_path, pre_splitted_filename).items():
                self.__setattr__(attrib_name, attrib_object)


        except FileNotFoundError:

            print("Dataset_AmazonInstantVideo: Pre-splitted data not found, building new one")

            folder_path = self.DATASET_SPLIT_ROOT_FOLDER + self.DATASET_SUBFOLDER

            downloadFromURL(self.DATASET_URL, folder_path, ratings_file_name)

            # read Amazon Instant Video
            df = pd.read_csv(folder_path + ratings_file_name, sep=',', header=None,
                             names=['user', 'item', 'rating', 'timestamp'])[
                ['user', 'item', 'rating']]

            # keep only ratings = 5
            URM_train_builder = IncrementalSparseMatrix(auto_create_col_mapper=True, auto_create_row_mapper=True)
            URM_train_builder.add_data_lists(df['user'].values, df['item'].values, df['rating'].values)
            URM_all = URM_train_builder.get_SparseMatrix()

            URM_all.data = URM_all.data == 5
            URM_all.eliminate_zeros()

            # keep only users with at least 5 ratings
            URM_all = ut.filter_urm(URM_all, user_min_number_ratings=5, item_min_number_ratings=1)

            # create train - test - validation

            URM_train_original, self.URM_test = split_train_validation_percentage_user_wise(URM_all,
                                                                                            train_percentage=1 - test_percentage,
                                                                                            verbose=False)

            self.URM_train, self.URM_validation = split_train_validation_percentage_user_wise(URM_train_original,
                                                                                              train_percentage=1 - validation_percentage,
                                                                                              verbose=False)

            data_dict = {
                "URM_train": self.URM_train,
                "URM_test": self.URM_test,
                "URM_validation": self.URM_validation,
            }

            save_data_dict(data_dict, pre_splitted_path, pre_splitted_filename)

        print("Dataset_AmazonInstantVideo: Dataset loaded")

        ut.print_stat_datareader(self)
