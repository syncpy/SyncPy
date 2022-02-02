
import importlib, sys

sys.path.append('Methods')
sys.path.append('Methods/utils')


moduleToLoad = 'Methods.DataFrom2Persons.Univariate.Continuous.Linear.Coherence'
class_name = 'Coherence'
module = importlib.import_module(moduleToLoad)
getattr(module, class_name)