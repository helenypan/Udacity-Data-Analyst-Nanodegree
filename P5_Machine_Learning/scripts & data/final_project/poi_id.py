#!/usr/bin/python

import sys
import pickle
import final_tools
import numpy as np
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
poi_feature = 'poi' # You will need to use more features
financial_features_list =  [
	'salary', 
	'deferral_payments', 
	'total_payments', 
	'loan_advances', 
	'bonus', 
	'restricted_stock_deferred', 
	'deferred_income', 
	'total_stock_value', 
	'expenses', 
	'exercised_stock_options', 
	'other', 
	'long_term_incentive', 
	'restricted_stock', 
	'director_fees'
	]
email_features_list = [
	'to_messages', 
	'email_address', 
	'from_poi_to_this_person', 
	'from_messages', 
	'from_this_person_to_poi', 
	'shared_receipt_with_poi'
	]

features_list = [poi_feature] + financial_features_list + email_features_list


### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Write the dictionary data to a csv
#final_tools.export_csv(data_dict,"dataset.csv")

### visualise features and color poi, help to identify outliers.
final_tools.scatter_plot(data_dict,"salary","total_payments","poi")

### Explore the dataset
final_tools.explore_dataset(data_dict, poi_feature,financial_features_list,email_features_list)

### Task 2: Remove outliers, and remove feature "email address" which is not float value and has no help identifying.
outliers_key_list = ['LOCKHART EUGENE E','THE TRAVEL AGENCY IN THE PARK','TOTAL']
feature_to_remove = 'email_address'
for outliers_key in outliers_key_list:
	data_dict.pop(outliers_key, None)
for name in data_dict:
	data_dict[name].pop(feature_to_remove,None)
features_list.remove(feature_to_remove)
print "\nOutlier keys removed:", outliers_key_list
print "\nFeature removed: ", feature_to_remove,"\n"

### Task 3: Create new feature(s)
new_feature = "poi_message_ratio"
(data_dict, features_list) = final_tools.create_feature_poi_message_ratio(data_dict,features_list,new_feature)
print "New feature created: ", new_feature,"\n"

final_tools.export_csv(data_dict,"dataset.csv")

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing

k_best_val = 8;
print k_best_val," best features (used in SVM):"
my_best_features = final_tools.select_k_best(k_best_val,my_dataset,features_list)   # best 12 features selected by SelectKBest.
features_list_all = [poi_feature] + my_best_features.keys()  + [new_feature]  #poi should always be the first feature in the feature list.

k_best_val_for_dt = 3;
print "\n",k_best_val_for_dt," best features selected for DecisionTreeClassifier:"
my_best_features = final_tools.select_k_best(k_best_val_for_dt,my_dataset,features_list)   # best 12 features selected by SelectKBest.
features_list_for_dt = [poi_feature] + my_best_features.keys() #poi should always be the first feature in the feature list.

### Choose final feature list for the final algorithm
features_list = features_list_for_dt

# data = featureFormat(my_dataset, features_list, sort_keys = True)
# labels, features = targetFeatureSplit(data)
# labels = np.array(labels)

# ### feature scaling using MinMaxScaler
# features = final_tools.min_max_scale(features)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
#from sklearn.naive_bayes import GaussianNB
#clf = GaussianNB()

### DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier
# clf_dt = DecisionTreeClassifier(max_features=3)
clf_dt = DecisionTreeClassifier()

### SVM
from sklearn.svm import SVC
svr = SVC()

### GridSearchCV to tune SVM, DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV
param_grid = {'C': [1000,5000,50000],  'kernel': ['rbf','linear']}
clf_svm = GridSearchCV(svr, param_grid)

# param_dt = {'criterion':['gini','entropy'],'max_features':np.arange(1,5),'max_depth':[None,2,3,4,5,6,7]}
# clf_dt = GridSearchCV(clf_dt, param_dt)

from sklearn.ensemble import RandomForestClassifier
clf_rf = RandomForestClassifier()

from sklearn.neighbors import KNeighborsClassifier
clf_kn = KNeighborsClassifier()

from sklearn.linear_model import LogisticRegression
clf_lr = LogisticRegression(C=10**18, tol=10**-21)

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!

# final_tools.k_fold_evaluate(clf_svm,my_dataset,features_list_all)
final_tools.k_fold_evaluate(clf_dt,my_dataset,features_list_for_dt)

### Final chosen algorithm for the tester
clf = clf_dt

print "\nValidation with test_classifier in tester.py: "
test_classifier(clf, my_dataset, features_list)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)