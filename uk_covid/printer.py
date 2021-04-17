from sklearn.tree import export_graphviz
from six import StringIO  
from IPython.display import Image  
import pydotplus

def printTree(xnames, clf, yclasses):
    dot_data = StringIO()
    export_graphviz(clf, out_file=dot_data,  
                    filled=True, rounded=True,
                    special_characters=True,feature_names = xnames,
                    class_names=[str(a) for a in yclasses],)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
    graph.write_png('uk-covid.png')