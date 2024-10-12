from autora.theorist.rnn_sindy_rl.resources.bandits import AgentQ, EnvironmentBanditsDrift, create_dataset
from autora.theorist.rnn_sindy_rl import RNNSindy
import numpy as np

def test_basic():
    theorist = RNNSindy()
    assert theorist is not None

def test_predict_from_conditions():

    rnnsindy = RNNSindy(n_actions=2)

    conditions = [np.array([[0, 1], [0, 1], [0, 1], [1, 0], [1, 0], [1, 0]])]
    observations = [np.array([[0, 1], [0, 1], [0, 1], [1, 0], [1, 0], [1, 0]])]

    rnnsindy = rnnsindy.fit(conditions, observations, epochs=20)

    predictions = rnnsindy.predict(conditions)

    assert len(predictions) == len(conditions)
    assert predictions[0].shape == (len(conditions[0]), 2)


def test_predict_from_conditions_and_observations():
    rnnsindy = RNNSindy(n_actions=2)

    conditions = [np.array([[0, 1], [0, 1], [0, 1], [1, 0], [1, 0], [1, 0]])]
    observations = [np.array([[0, 1], [0, 1], [0, 1], [1, 0], [1, 0], [1, 0]])]

    rnnsindy = rnnsindy.fit(conditions, observations, epochs=20)

    predictions = rnnsindy.predict(conditions, observations=observations)

    assert len(predictions) == len(conditions)
    assert predictions[0].shape == (len(conditions[0]), 2)





