import pytest

from rotational_placement.experiment_class import Experiment

def test_experiment_initialization():
    exp = Experiment("1.1",1,1,10,"num")
    assert exp.alias == "1.1"
    assert exp.get_seed_data() is None
    
