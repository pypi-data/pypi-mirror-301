import os
import time

import torch

import numpy as np
import matplotlib.pyplot as plt
from typing import Union, Optional, TypeAlias, BinaryIO, IO


# SINDy-RL libraries
from autora.theorist.rnn_sindy_rl.resources import rnn, rnn_training, bandits, rnn_utils

FILE_LIKE: TypeAlias = Union[str, os.PathLike, BinaryIO, IO[bytes]]


def main(
    # necessary parameters
    xs: np.ndarray,  # shape: (n_sessions, n_trials_per_session, n_conditions)
    ys: np.ndarray,  # shape: (n_sessions, n_trials_per_session, n_conditions)
    model: rnn.RLRNN,

    # training parameters
    epochs: int = 100,
    n_steps_per_call: int = 8,  # None for full sequence
    batch_size: int = None,  # None for one batch per epoch
    learning_rate: float = 1e-3,
    convergence_threshold: float = 1e-6,
    analysis: bool = False,
    path: Optional[FILE_LIKE] = None,
    checkpoint: str = None,
    **kwargs,
    
) -> Union[rnn.RLRNN, rnn.EnsembleRNN]:
  
  n_actions = model._n_actions
  
  # set up dataset given conditions and observations
  if xs.shape[0] == 1:
    # repeat the same session once along the first axis
    xs = np.repeat(xs, 2, axis=0)
    ys = np.repeat(ys, 2, axis=0)
  dataset_train = rnn_utils.DatasetRNN(xs[:-1], ys[:-1], device=model.device)
  dataset_test = rnn_utils.DatasetRNN(xs[-1:], ys[-1:], device=model.device)

  model = [model]
  optimizer_rnn = [torch.optim.Adam(m.parameters(), lr=learning_rate) for m in model]

  # TODO: Check how to implement this
  # if checkpoint is not None:
  #     # load trained parameters
  #     state_dict = torch.load(checkpoint, map_location=torch.device('cpu'))
  #     state_dict_model = state_dict['model']
  #     state_dict_optimizer = state_dict['optimizer']
  #     if isinstance(state_dict_model, dict):
  #       for m, o in zip(model, optimizer_rnn):
  #         m.load_state_dict(state_dict_model)
  #         o.load_state_dict(state_dict_optimizer)
  #     elif isinstance(state_dict_model, list):
  #         print('Loading ensemble model...')
  #         for i, state_dict_model_i, state_dict_optim_i in zip(range(len(state_dict_model)), state_dict_model, state_dict_optimizer):
  #             model[i].load_state_dict(state_dict_model_i)
  #             optimizer_rnn[i].load_state_dict(state_dict_optim_i)
  #         rnn = rnn.EnsembleRNN(model, voting_type=voting_type)
  #     print('Loaded parameters.')
  
  start_time = time.time()
  
  #Fit the hybrid RNN
  print('Training the RNN...')
  for m in model:
    m.train()
  model, optimizer_rnn, _ = rnn_training.fit_model(
      model=model,
      dataset=dataset_train,
      optimizer=optimizer_rnn,
      convergence_threshold=convergence_threshold,
      epochs=epochs,
      batch_size=batch_size,
      # n_submodels=n_submodels,
      # ensemble_type=ensemble,
      # voting_type=voting_type,
      # sampling_replacement=sampling_replacement,
      # evolution_interval=evolution_interval,
      n_steps_per_call=n_steps_per_call,
  )
  
  # evaluate model
  print('Test the trained RNN on a test dataset...')
  if isinstance(model, (list, rnn.EnsembleRNN)):
    for m in model:
      m.eval()
  else:
    model.eval()  
  with torch.no_grad():
    rnn_training.fit_model(
        model=model,
        dataset=dataset_test,
        n_steps_per_call=1,
    )

  print(f'RNN training took {time.time() - start_time:.2f} seconds.')
  
  # save trained parameters  
  state_dict = {
    'model': model.state_dict() if isinstance(model, torch.nn.Module) else [model_i.state_dict() for model_i in model],
    'optimizer': optimizer_rnn.state_dict() if isinstance(optimizer_rnn, torch.optim.Adam) else [optim_i.state_dict() for optim_i in optimizer_rnn],
  }

  if path:
    torch.save(state_dict, path)
  
    print(f'Saved RNN parameters to file {path}.')

  # Analysis
  if analysis:
    # Synthesize a dataset using the fitted network
    session_id = 0

    experiment_list_test = bandits.BanditSession(xs[session_id, :, 0], xs[session_id, :, 1], xs[session_id, :, 2], None, xs.shape[1])
    model.set_device(torch.device('cpu'))
    model.to(torch.device('cpu'))
    rnn_agent = bandits.AgentNetwork(model, n_actions=n_actions, deterministic=True)
    
    choices = experiment_list_test.choices
    rewards = experiment_list_test.rewards

    list_probs = []
    list_qs = []

    # get q-values from trained rnn
    qs_rnn, probs_rnn = bandits.get_update_dynamics(experiment_list_test, rnn_agent)
    list_probs.append(np.expand_dims(probs_rnn, 0))
    list_qs.append(np.expand_dims(qs_rnn, 0))

    colors = ['tab:blue', 'tab:orange', 'tab:pink', 'tab:grey']

    # concatenate all choice probs and q-values
    probs = np.concatenate(list_probs, axis=0)
    qs = np.concatenate(list_qs, axis=0)

    # normalize q-values
    def normalize(qs):
      return (qs - np.min(qs, axis=1, keepdims=True)) / (np.max(qs, axis=1, keepdims=True) - np.min(qs, axis=1, keepdims=True))

    qs = normalize(qs)
    fig, axs = plt.subplots(4, 1, figsize=(20, 10))

    reward_probs = np.stack([experiment_list_test.timeseries[:, i] for i in range(n_actions)], axis=0)
    bandits.plot_session(
        compare=True,
        choices=choices,
        rewards=rewards,
        timeseries=reward_probs,
        timeseries_name='Reward Probs',
        labels=[f'Arm {a}' for a in range(n_actions)],
        color=['tab:purple', 'tab:cyan'],
        binary=True,
        fig_ax=(fig, axs[0]),
        )

    bandits.plot_session(
        compare=True,
        choices=choices,
        rewards=rewards,
        timeseries=probs[:, :, 0],
        timeseries_name='Choice Probs',
        color=colors,
        labels=['RNN'],
        binary=True,
        fig_ax=(fig, axs[1]),
        )

    bandits.plot_session(
        compare=True,
        choices=choices,
        rewards=rewards,
        timeseries=qs[:, :, 0],
        timeseries_name='Q-Values',
        color=colors,
        binary=True,
        fig_ax=(fig, axs[2]),
        )

    dqs_arms = normalize(-1*np.diff(qs, axis=2))

    bandits.plot_session(
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
    
  return model
