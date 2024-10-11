# test/test_mpmg_logic.py

from mpmg_env import MPMGEnv
import numpy as np
import logging
import itertools
import os

# Create a 'logs' directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

def configure_logging(scenario_name):
    # Remove all handlers associated with the root logger object
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    log_filename = f'logs/{scenario_name}.log'
    logging.basicConfig(
        filename=log_filename,
        filemode='w',  # Overwrite the log file each time
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def test_equiprobable_actions(env: MPMGEnv, num_plays: int, scenario_name: str):
    """
    Test with joint actions occurring equiprobably.
    """
    configure_logging(scenario_name)
    logging.info(f'--- Starting Scenario: {scenario_name} ---')

    # Log initial hyperparameters
    logging.info(f'Hyperparameters: n_agents={env.n_agents}, action_size={env.action_size}, '
                 f'sigma_beta={env.sigma_beta}, alpha={env.alpha}, beta_parameters={env.beta_parameters}')

    # Generate equiprobable joint actions
    joint_actions = list(itertools.product(range(env.action_size), repeat=env.n_agents))
    actions_sequence = (joint_actions * (num_plays // len(joint_actions) + 1))[:num_plays]
    np.random.shuffle(actions_sequence)  # Randomize the order

    # Run episodes
    for episode, actions in enumerate(actions_sequence, start=1):
        rewards, next_state, done = env.step(list(actions))
        logging.info(f'Episode {episode}: Actions={actions}, Rewards={rewards}, '
                     f'Action Frequencies={env.action_frequencies}, '
                     f'Joint Action Frequencies={env.joint_action_frequencies}, '
                     f'Iteration={env.iteration}')

    logging.info(f'--- Ending Scenario: {scenario_name} ---')

def test_full_defection(env: MPMGEnv, num_plays: int, scenario_name: str):
    """
    Test with all agents always defecting.
    """
    configure_logging(scenario_name)
    logging.info(f'--- Starting Scenario: {scenario_name} ---')

    # Log initial hyperparameters
    logging.info(f'Hyperparameters: n_agents={env.n_agents}, action_size={env.action_size}, '
                 f'sigma_beta={env.sigma_beta}, alpha={env.alpha}, beta_parameters={env.beta_parameters}')

    actions = [0] * env.n_agents  # All agents defect

    # Run episodes
    for episode in range(1, num_plays + 1):
        rewards, next_state, done = env.step(actions)
        logging.info(f'Episode {episode}: Actions={actions}, Rewards={rewards}, '
                     f'Action Frequencies={env.action_frequencies}, '
                     f'Joint Action Frequencies={env.joint_action_frequencies}, '
                     f'Iteration={env.iteration}')

    logging.info(f'--- Ending Scenario: {scenario_name} ---')

def test_full_cooperation(env: MPMGEnv, num_plays: int, scenario_name: str):
    """
    Test with all agents always cooperating.
    """
    configure_logging(scenario_name)
    logging.info(f'--- Starting Scenario: {scenario_name} ---')

    # Log initial hyperparameters
    logging.info(f'Hyperparameters: n_agents={env.n_agents}, action_size={env.action_size}, '
                 f'sigma_beta={env.sigma_beta}, alpha={env.alpha}, beta_parameters={env.beta_parameters}')

    actions = [1] * env.n_agents  # All agents cooperate

    # Run episodes
    for episode in range(1, num_plays + 1):
        rewards, next_state, done = env.step(actions)
        logging.info(f'Episode {episode}: Actions={actions}, Rewards={rewards}, '
                     f'Action Frequencies={env.action_frequencies}, '
                     f'Joint Action Frequencies={env.joint_action_frequencies}, '
                     f'Iteration={env.iteration}')

    logging.info(f'--- Ending Scenario: {scenario_name} ---')

if __name__ == '__main__':

    SEED = 42
    NUM_EPISODE = 100  # Number of episodes for each scenario

    # 2-player homogeneous MPMG
    env = MPMGEnv(n_agents=2, sigma_beta=0.0)

    # Scenario 1: Equiprobable Actions
    env.reset(seed=SEED)
    test_equiprobable_actions(env, NUM_EPISODE, scenario_name='2_player_homogeneous_equiprobable_actions')

    # Scenario 2: Full Defection
    env.reset(seed=SEED)
    test_full_defection(env, NUM_EPISODE, scenario_name='2_player_homogeneous_full_defection')

    # Scenario 3: Full Cooperation
    env.reset(seed=SEED)
    test_full_cooperation(env, NUM_EPISODE, scenario_name='2_player_homogeneous_full_cooperation')

    # 5-player homogeneous MPMG
    env = MPMGEnv(n_agents=5, sigma_beta=0.0)

    # Scenario 1: Equiprobable Actions
    env.reset(seed=SEED)
    test_equiprobable_actions(env, NUM_EPISODE, scenario_name='5_player_homogeneous_equiprobable_actions')

    # Scenario 2: Full Defection
    env.reset(seed=SEED)
    test_full_defection(env, NUM_EPISODE, scenario_name='5_player_homogeneous_full_defection')

    # Scenario 3: Full Cooperation
    env.reset(seed=SEED)
    test_full_cooperation(env, NUM_EPISODE, scenario_name='5_player_homogeneous_full_cooperation')

    # 2-player heterogeneous MPMG
    env = MPMGEnv(n_agents=2, sigma_beta=0.5)

    # Scenario 1: Equiprobable Actions
    env.reset(seed=SEED)
    test_equiprobable_actions(env, NUM_EPISODE, scenario_name='2_player_heterogeneous_equiprobable_actions')

    # Scenario 2: Full Defection
    env.reset(seed=SEED)
    test_full_defection(env, NUM_EPISODE, scenario_name='2_player_heterogeneous_full_defection')

    # Scenario 3: Full Cooperation
    env.reset(seed=SEED)
    test_full_cooperation(env, NUM_EPISODE, scenario_name='2_player_heterogeneous_full_cooperation')

    # 5-player heterogeneous MPMG
    env = MPMGEnv(n_agents=5, sigma_beta=0.5)

    # Scenario 1: Equiprobable Actions
    env.reset(seed=SEED)
    test_equiprobable_actions(env, NUM_EPISODE, scenario_name='5_player_heterogeneous_equiprobable_actions')

    # Scenario 2: Full Defection
    env.reset(seed=SEED)
    test_full_defection(env, NUM_EPISODE, scenario_name='5_player_heterogeneous_full_defection')

    # Scenario 3: Full Cooperation
    env.reset(seed=SEED)
    test_full_cooperation(env, NUM_EPISODE, scenario_name='5_player_heterogeneous_full_cooperation')


