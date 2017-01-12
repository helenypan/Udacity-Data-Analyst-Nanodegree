#!/usr/bin/python

import csv
import sys
sys.path.append("../tools/")
import matplotlib.pyplot as plt
import numpy as np
from feature_format import featureFormat,targetFeatureSplit
from sklearn.feature_selection import SelectKBest
import operator
from numpy import mean
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score

#export a csv file from the data dictionary
def export_csv(data_dict,csv_file):
	counter = 0
	with open(csv_file,'wb') as f:
		for key, value in data_dict.iteritems():
			if counter == 0:
				w = csv.DictWriter(f,['name']+value.keys())
				w.writeheader()
			value['name'] = key
			w.writerow(value)
			counter += 1

#plot a scatter plot of feature x, y
def scatter_plot(data_dict, x, y,poi):
    data = featureFormat(data_dict, [x, y, poi])
    for feature in data:
        x = feature[0]
        y = feature[1]
        poi = feature[2]
        color = 'red' if poi else 'green'
        plt.scatter(x, y, color=color)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()

def explore_dataset(data_dict, poi_feature,financial_features_list,email_features_list):
    print "\nInitial dataset exploration:"
    print "Total Number of data points: ", len(data_dict)
    features_list =[poi_feature] + financial_features_list + email_features_list
    number_of_poi = 0
    number_of_non_poi = 0
    miss_value_dict = {}
    for key in features_list:
        miss_value_dict[key] = 0
    for name in data_dict:
        if data_dict[name][poi_feature]:
            number_of_poi += 1
        else:
            number_of_non_poi += 1
        for key in features_list:
            if data_dict[name][key] == "NaN":
                miss_value_dict[key] += 1
    print "Total number of poi: ", number_of_poi
    print "Total number of non-poi: ", number_of_non_poi
    print "Total number of features: ", len(features_list)
    print "Number of financial features: ", len(financial_features_list)
    print "Number of email features: ", len(email_features_list)
    print "Number of labeled features(POI): ", len([poi_feature]),"\n"

    miss_value_list_sorted = sorted(miss_value_dict.items(), key=operator.itemgetter(1), reverse=True)
    print "Number of missing values in the features:"
    print "{:<30} {:<15}".format('Feature','Number of missing values')
    for key,value in miss_value_list_sorted:
        print "{:<30} {:<15}".format(key, value)

def get_num_of_missing_values(data_dict, feature):
    num_of_missing = 0
    for name in data_dict:
        if data_dict[name][feature] == "NaN":
            num_of_missing += 1
    return num_of_missing
    
def select_k_best(k_val,data_dict,features_list):
    data = featureFormat(data_dict, features_list)
    labels, features = targetFeatureSplit(data)
    k_best = SelectKBest(k=k_val).fit(features, labels)
    k_best_scores = k_best.scores_
    feature_score_dict = dict()
    index = 1 #index for features_list, index 0 is for poi, hence start from 1
    for score in k_best_scores:
        feature_score_dict[features_list[index]] = score
        index += 1
    k_best_features = sorted(feature_score_dict.items(), key=operator.itemgetter(1), reverse=True)[0:k_val]
    print "{:<25} {:<15} {:<25}".format('Feature','Score',"Number of Missing Values")
    for key,value in k_best_features:
        print "{:<25} {:<15} {:<25}".format(key, value, get_num_of_missing_values(data_dict,key))
    return dict(k_best_features)

def create_feature_poi_message_ratio(data_dict, features_list,new_feature_name):
    #create a new feature poi_message_ratio, 
    for name in data_dict:
        row = data_dict[name]
        if row["from_poi_to_this_person"] == 'NaN' or row["from_this_person_to_poi"] == "NaN" or \
        row["from_messages"] == "NaN" or row["to_messages"] == "NaN":
            data_dict[name][new_feature_name] = 'NaN'
        else:
            data_dict[name][new_feature_name] = (float(row["from_poi_to_this_person"]) + float(row["from_this_person_to_poi"])) / \
            (float(row["from_messages"]) + float(row["to_messages"]))
    features_list += [new_feature_name]
    return (data_dict, features_list)

def min_max_scale(features):
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    rescaled_features = scaler.fit_transform(features)
    return rescaled_features

def k_fold_evaluate(clf, my_dataset, features_list, num_iters=1000, test_size=0.4,k=6):
    data = featureFormat(my_dataset, features_list, sort_keys = True)
    labels, features = targetFeatureSplit(data)
    labels = np.array(labels)

    ### feature scaling using MinMaxScaler
    features = min_max_scale(features)

    print "\nValidation with KFold ( K =",k,"):"
    print clf
    accuracy = []
    precision = []
    recall = []
    feature_importances = np.zeros(len(features_list)-1)
    counter = 0
    kf_total = KFold(len(features), n_folds=k)
    for train_indices, test_indices in kf_total:
        features_train = features[train_indices]
        features_test = features[test_indices]
        labels_train = labels[train_indices]
        labels_test = labels[test_indices]
        clf.fit(features_train, labels_train)
        prediction = clf.predict(features_test)
        if hasattr(clf, 'feature_importances_'):
            feature_importances += np.array(clf.feature_importances_)
        accuracy.append(accuracy_score(labels_test, prediction))
        precision.append(precision_score(labels_test, prediction))
        recall.append(recall_score(labels_test, prediction))
        counter += 1
    if hasattr(clf, 'feature_importances_'):
        feature_importances = feature_importances/counter
        feature_importances_dict = dict()
        index = 1 #index for features_list, index 0 is for poi, hence start from 1
        for importance in feature_importances:
            feature_importances_dict[features_list[index]] = importance
            index += 1
        feature_importances_sorted = sorted(feature_importances_dict.items(), key=operator.itemgetter(1), reverse=True)
        print "{:<25} {:<15}".format('Feature','Importance')
        for key,value in feature_importances_sorted:
            print "{:<25} {:<15}".format(key, value)
    print "\nAccuracy:  {}".format(mean(accuracy))
    print "Precision: {}".format(mean(precision))
    print "Recall:    {}".format(mean(recall))

