import warnings
import numpy as np
import matplotlib.pyplot as plt
from typing import Union
import pysindy as ps

# SINDy-RL libraries
from autora.theorist.rnn_sindy_rl.resources.rnn import RLRNN, EnsembleRNN
from autora.theorist.rnn_sindy_rl.resources.bandits import AgentNetwork, AgentSindy, plot_session, get_update_dynamics, BanditSession
from autora.theorist.rnn_sindy_rl.resources.sindy_utils import create_dataset, constructor_update_rule_sindy
from autora.theorist.rnn_sindy_rl.resources.rnn_utils import DatasetRNN
from autora.theorist.rnn_sindy_rl.resources.sindy_training import fit_model

warnings.filterwarnings("ignore")

def main(
    # necessary parameters
    xs: np.ndarray,
    ys: np.ndarray,
    rnn_model: Union[RLRNN, EnsembleRNN],
    sindy_model: AgentSindy,
    library_setup: dict,
    datafilter_setup: dict,

    # sindy parameters
    library: ps.PolynomialLibrary = None,
    threshold = 0.03,
    polynomial_degree = 1,
    regularization = 1e-1,
    sindy_ensemble = False,
    library_ensemble = False,

    # training parameters
    analysis = False,
    
    **kwargs,
    ) -> AgentSindy:
    
    # tracked variables in the RNN
    z_train_list = ['xQf','xQr', 'xQc', 'xH']
    control_list = ['ca','ca[k-1]', 'cr', 'cQr']
    sindy_feature_list = z_train_list + control_list

    # data setup
    # set up dataset given conditions and observations
    if xs.shape[0] == 1:
        # repeat the same session once along the first axis
        xs = np.repeat(xs, 2, axis=0)
        ys = np.repeat(ys, 2, axis=0)
    dataset_train = DatasetRNN(xs[:-1], ys[:-1])
    dataset_test = DatasetRNN(xs[-1:], ys[-1:])
    n_actions = rnn_model._n_actions
    
    # set up rnn agent and expose q-values to train sindy
    agent_rnn = AgentNetwork(rnn_model, n_actions)

    # create dataset for sindy training, fit sindy, set up sindy agent
    if library is None:
        library = ps.PolynomialLibrary(degree=2, include_interaction=True)
    x_train, control, feature_names, beta = create_dataset(agent_rnn, dataset_train, -1, -1, normalize=True, shuffle=False, verbose=False)
    sindy_models = fit_model(x_train, control, feature_names, library, library_setup, datafilter_setup, True, False, threshold, regularization, sindy_ensemble, library_ensemble)
    sindy_model.set_models(sindy_models)
    sindy_model.set_update_rule(*constructor_update_rule_sindy(sindy_model))
    
    print(f'Beta for SINDy: {beta}')
    sindy_model._beta = beta

    # --------------------------------------------------------------
    # Analysis
    # --------------------------------------------------------------
    if analysis:
        labels = ['RNN', 'SINDy']
        experiment_test = BanditSession(xs[-1, :, 0], xs[-1, :, 1], xs[-1, :, 2], None, xs.shape[1])
        choices = experiment_test.choices
        rewards = experiment_test.rewards

        list_probs = []
        list_qs = []

        # get q-values from trained rnn
        qs_rnn, probs_rnn = get_update_dynamics(experiment_test, agent_rnn)
        list_probs.append(np.expand_dims(probs_rnn, 0))
        list_qs.append(np.expand_dims(qs_rnn, 0))

        # get q-values from trained sindy
        qs_sindy, probs_sindy = get_update_dynamics(experiment_test, sindy_model)
        list_probs.append(np.expand_dims(probs_sindy, 0))
        list_qs.append(np.expand_dims(qs_sindy, 0))

        colors = ['tab:blue', 'tab:orange', 'tab:pink', 'tab:grey']

        # concatenate all choice probs and q-values
        probs = np.concatenate(list_probs, axis=0)
        qs = np.concatenate(list_qs, axis=0)

        # normalize q-values
        def normalize(qs):
            return (qs - np.min(qs, axis=1, keepdims=True)) / (np.max(qs, axis=1, keepdims=True) - np.min(qs, axis=1, keepdims=True))

        qs = normalize(qs)

        fig, axs = plt.subplots(4, 1, figsize=(20, 10))
        # turn the x labels off for all but the last subplot
        for i in range(3):
            axs[i].set_xticklabels([])
            axs[i].set_xlabel('')
            axs[i].set_xlim(0, xs.shape[1])
            # axs[i].set_ylim(0, 1)    

        reward_probs = np.stack([experiment_test.timeseries[:, i] for i in range(n_actions)], axis=0)
        plot_session(
            compare=True,
            choices=choices,
            rewards=rewards,
            timeseries=reward_probs,
            timeseries_name='Reward Probs',
            labels=[f'Arm {a}' for a in range(n_actions)],
            color=['tab:purple', 'tab:cyan'],
            binary=True,
            fig_ax=(fig, axs[0]),
            x_label='',
            )

        plot_session(
            compare=True,
            choices=choices,
            rewards=rewards,
            timeseries=probs[:, :, 0],
            timeseries_name='Choice Probs',
            color=colors,
            labels=labels,
            binary=True,
            fig_ax=(fig, axs[1]),
            x_label='',
            )

        plot_session(
            compare=True,
            choices=choices,
            rewards=rewards,
            timeseries=qs[:, :, 0],
            timeseries_name='Q-Values',
            color=colors,
            binary=True,
            fig_ax=(fig, axs[2]),
            x_label='',
            )

        dqs_arms = -1*np.diff(qs, axis=2)
        dqs_arms = normalize(dqs_arms)

        plot_session(
            compare=True,
            choices=choices,
            rewards=rewards,
            timeseries=dqs_arms[:, :, 0],
            timeseries_name='dQ/dActions',
            color=colors,
            binary=True,
            fig_ax=(fig, axs[3]),
            )

        plt.show()

    return sindy_model
