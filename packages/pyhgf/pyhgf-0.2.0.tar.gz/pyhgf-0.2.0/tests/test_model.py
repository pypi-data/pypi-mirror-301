# Author: Nicolas Legrand <nicolas.legrand@cas.au.dk>

import jax.numpy as jnp
import numpy as np

from pyhgf import load_data
from pyhgf.model import HGF, Network
from pyhgf.response import total_gaussian_surprise


def test_network():
    """Test the network class"""

    #####################
    # Creating networks #
    #####################

    custom_hgf = (
        Network()
        .add_nodes(kind="continuous-state")
        .add_nodes(kind="binary-state")
        .add_nodes(value_children=0)
        .add_nodes(
            value_children=1,
        )
        .add_nodes(value_children=[2, 3])
        .add_nodes(value_children=4)
        .add_nodes(volatility_children=[2, 3])
        .add_nodes(volatility_children=2)
        .add_nodes(volatility_children=7)
    )

    custom_hgf.create_belief_propagation_fn(overwrite=False)
    custom_hgf.create_belief_propagation_fn(overwrite=True)

    custom_hgf.input_data(input_data=np.ones((10, 2)))


def test_continuous_hgf():
    """Test the continuous HGF"""
    ##############
    # Continuous #
    ##############
    timeserie = load_data("continuous")

    # two-level
    # ---------
    two_level_continuous_hgf = HGF(
        n_levels=2,
        model_type="continuous",
        initial_mean={"1": timeserie[0], "2": 0.0},
        initial_precision={"1": 1e4, "2": 1e1},
        tonic_volatility={"1": -3.0, "2": -3.0},
        tonic_drift={"1": 0.0, "2": 0.0},
        volatility_coupling={"1": 1.0},
    )

    two_level_continuous_hgf.input_data(input_data=timeserie)

    surprise = two_level_continuous_hgf.surprise()  # Sum the surprise for this model
    assert jnp.isclose(surprise.sum(), -1141.0911)
    assert len(two_level_continuous_hgf.node_trajectories[1]["mean"]) == 614

    # three-level
    # -----------
    three_level_continuous_hgf = HGF(
        n_levels=3,
        model_type="continuous",
        initial_mean={"1": 1.04, "2": 1.0, "3": 1.0},
        initial_precision={"1": 1e4, "2": 1e1, "3": 1e1},
        tonic_volatility={"1": -13.0, "2": -2.0, "3": -2.0},
        tonic_drift={"1": 0.0, "2": 0.0, "3": 0.0},
        volatility_coupling={"1": 1.0, "2": 1.0},
    )
    three_level_continuous_hgf.input_data(input_data=timeserie)
    surprise = three_level_continuous_hgf.surprise()
    assert jnp.isclose(surprise.sum(), -892.82227)

    # test an alternative response function
    sp = total_gaussian_surprise(three_level_continuous_hgf)
    assert jnp.isclose(sp.sum(), -2545.4248)


def test_binary_hgf():
    """Test the binary HGF"""

    ##########
    # Binary #
    ##########
    u, _ = load_data("binary")

    # two-level
    # ---------
    two_level_binary_hgf = HGF(
        n_levels=2,
        model_type="binary",
        initial_mean={"1": 0.0, "2": 0.5},
        initial_precision={"1": 0.0, "2": 1e4},
        tonic_volatility={"1": None, "2": -6.0},
        tonic_drift={"1": None, "2": 0.0},
        volatility_coupling={"1": None},
        eta0=0.0,
        eta1=1.0,
        binary_precision=jnp.inf,
    )

    # Provide new observations
    two_level_binary_hgf = two_level_binary_hgf.input_data(u)
    surprise = two_level_binary_hgf.surprise()
    assert jnp.isclose(surprise.sum(), 215.58821)

    # three-level
    # -----------
    three_level_binary_hgf = HGF(
        n_levels=3,
        model_type="binary",
        initial_mean={"1": 0.0, "2": 0.5, "3": 0.0},
        initial_precision={"1": 0.0, "2": 1e4, "3": 1e1},
        tonic_volatility={"1": None, "2": -6.0, "3": -2.0},
        tonic_drift={"1": None, "2": 0.0, "3": 0.0},
        volatility_coupling={"1": None, "2": 1.0},
        eta0=0.0,
        eta1=1.0,
        binary_precision=jnp.inf,
    )
    three_level_binary_hgf.input_data(input_data=u)
    surprise = three_level_binary_hgf.surprise()
    assert jnp.isclose(surprise.sum(), 215.59067)


def test_custom_sequence():
    """Test the continuous HGF"""

    ############################
    # dynamic update sequences #
    ############################
    u, _ = load_data("binary")

    three_level_binary_hgf = HGF(
        n_levels=3,
        model_type="binary",
        initial_mean={"1": 0.0, "2": 0.5, "3": 0.0},
        initial_precision={"1": 0.0, "2": 1e4, "3": 1e1},
        tonic_volatility={"1": None, "2": -6.0, "3": -2.0},
        tonic_drift={"1": None, "2": 0.0, "3": 0.0},
        volatility_coupling={"1": None, "2": 1.0},
        eta0=0.0,
        eta1=1.0,
        binary_precision=jnp.inf,
    )

    # create a custom update series
    update_sequence1 = three_level_binary_hgf.update_sequence
    update_sequence2 = update_sequence1[:2]
    update_branches = (update_sequence1, update_sequence2)
    branches_idx = np.random.binomial(n=1, p=0.5, size=len(u))

    three_level_binary_hgf.input_custom_sequence(
        update_branches=update_branches,
        branches_idx=branches_idx,
        input_data=u,
    )
