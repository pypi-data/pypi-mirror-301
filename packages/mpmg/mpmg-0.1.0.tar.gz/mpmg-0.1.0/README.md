# Minimum Price Markov Game (MPMG) Environment

## Overview

`mpmg` is a modular environment designed for studying the Minimum Price Markov Game (MPMG), a concept in game theory and algorithmic game theory. It provides an easy-to-use framework for conducting experiments with multiple agents using collusion and cooperation dynamics. This environment is useful for researchers and developers interested in game theory, reinforcement learning, and multi-agent systems.

## Features
- **Customizable Multi-Agent Environment**: Supports different numbers of agents and heterogeneous vs. homogeneous settings.
- **Test Framework**: Visualize action frequencies and average rewards over time for custom MPMG configurations.

## Project Structure

```
mpmg/
├── mpmg/                  # Main package directory
│   ├── __init__.py        # Package initialization
│   └── mpmg_env.py        # Environment implementation
├── tests/                 # Unit and integration tests
│   ├── __init__.py        # Package initialization for tests (optional)
│   └── test_mpmg_logic.py # Tests and scenario validation
├── .gitignore             # Ignored files for git
├── README.md              # Project description and usage guide
├── requirements.txt       # Project dependencies
├── setup.py               # Installation script
└── LICENSE                # License information
```

## Installation

To install the package locally, run the following command from the root directory:

```sh
pip install -e .
```

This installs the package in "editable" mode, meaning any changes made in the source code will immediately reflect in the installed package.

### Requirements
- Python 3.6+
- NumPy

Dependencies can be installed from `requirements.txt`:

```sh
pip install -r requirements.txt
```

## Usage

To use the `mpmg` package, import the `MPMGEnv` class and create an instance of the environment:

```python
from mpmg import MPMGEnv

# Create an instance of the environment
env = MPMGEnv(n_agents=2, sigma_beta=0.0)

# Reset the environment
state = env.reset(seed=42)

# Take a step in the environment
actions = [1, 0]  # Example actions for each agent
rewards, next_state, done = env.step(actions)
```

The `MPMGEnv` class provides methods for resetting the environment, taking steps, and observing the state, rewards, and dynamics of multi-agent interactions.

## Running Tests

Unit tests are available in the `tests/` directory. You can run the tests using `pytest`:

```sh
pytest tests/
```

## Tests

The test scenarios provided in `test_mpmg_logic.py` also generate logs of action frequencies and average rewards for each agent.

## Scenarios
The environment supports the following scenarios for testing and analysis:
- **Equiprobable Actions**: Agents choose actions with equal probability.
- **Full Defection**: All agents choose to defect.
- **Full Cooperation**: All agents cooperate.

These scenarios can be run using the test script provided in `tests/test_mpmg_logic.py`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for improvements, bug fixes, or new features.

## Author

Igor Sadoune - igor.sadoune@polymtl.ca

