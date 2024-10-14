from hypothesis import given
from hypothesis import strategies as st

from autora.experiment_runner.synthetic.abstract.template_experiment import (
    template_experiment,
)
from autora.experiment_runner.synthetic.economics.expected_value_theory import (
    expected_value_theory,
)
from autora.experiment_runner.synthetic.economics.prospect_theory import prospect_theory
from autora.experiment_runner.synthetic.neuroscience.task_switching import (
    task_switching,
)
from autora.experiment_runner.synthetic.psychology.exp_learning import exp_learning
from autora.experiment_runner.synthetic.psychology.luce_choice_ratio import (
    luce_choice_ratio,
)
from autora.experiment_runner.synthetic.psychophysics.stevens_power_law import (
    stevens_power_law,
)
from autora.experiment_runner.synthetic.psychophysics.weber_fechner_law import (
    weber_fechner_law,
)
from autora.experiment_runner.synthetic.utilities import describe, register, retrieve

all_bundled_models = [
    ("expected_value_theory", expected_value_theory),
    ("prospect_theory", prospect_theory),
    ("luce_choice_ratio", luce_choice_ratio),
    ("template_experiment", template_experiment),
    ("weber_fechner_law", weber_fechner_law),
    ("stevens_power_law", stevens_power_law),
    ("task_switching", task_switching),
    ("exp_learning", exp_learning),
]

all_bundled_model_names = [b[0] for b in all_bundled_models]

for name, func in all_bundled_models:
    register(name, func)


@given(name=st.sampled_from(all_bundled_model_names))
def test_bundled_models_can_be_retrieved_by_name(name):
    model = retrieve(name)
    assert model is not None


@given(name=st.sampled_from(all_bundled_model_names))
def test_bundled_models_can_be_described_by_name(name):
    description = describe(name)
    assert isinstance(description, str)


@given(name=st.sampled_from(all_bundled_model_names))
def test_bundled_models_can_be_described_by_model(name):
    model = retrieve(name)
    description = describe(model)
    assert isinstance(description, str)


@given(name=st.sampled_from(all_bundled_model_names))
def test_model_descriptions_from_name_model_closure_are_the_same(name):
    description_from_name = describe(name)
    description_from_model = describe(retrieve(name))
    description_from_closure = describe(retrieve(name).factory_function)

    assert description_from_name == description_from_model
    assert description_from_model == description_from_closure
    assert description_from_closure == description_from_name
