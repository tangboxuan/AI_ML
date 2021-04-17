import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from sklearn.impute import KNNImputer #Import K-Nearest Neighbour Imputer

df = pd.read_csv("Covid-19-UK.csv", index_col=0)

# Fill missing values using K-Nearest Neighbour
imputer = KNNImputer(n_neighbors=2, weights="uniform")
idf = pd.DataFrame(imputer.fit_transform(df))
idf.columns = df.columns # Copy column names
idf.index = df.index # Copy index names
df = idf # Copy dataframe

yname = "newDeaths" # Name of y column

xnames = list(df)
xnames.remove(yname)
X = df[xnames]
df[yname] = df[yname].astype(int)
dfcopy = df

n = 10 # Max number of categories for y column

storage = []
for i in range(1, n+1):
    # Segment y column into i discrete groups
    df = dfcopy
    df['yGroup'], bins = pd.qcut(df[yname], i, labels=False, retbins=True)
    y = df['yGroup']
    yclasses = [str(int(bins[j])) + " to " + str(int(bins[j+1])) for j in range(i)]

    # Split dataset into training set and test set 70% training and 30% test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) 

    clf = DecisionTreeClassifier(min_samples_leaf=10) # Create Decision Tree classifer object
    clf = clf.fit(X_train,y_train) # Train Decision Tree Classifer
    y_pred = clf.predict(X_test) # Predict the response for test dataset
    accuracy = metrics.accuracy_score(y_test, y_pred) # Calculate accuracy score

    print(str(i) + " categories for " + yname + " gives an accuracy of "+str(accuracy))
    storage.append([clf, yclasses])

cat = int(input("How many categories to choose: ")) - 1

from printer import printTree
printTree(xnames, storage[cat][0], storage[cat][1])