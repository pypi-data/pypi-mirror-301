"""Define the architecture for a TMS"""

from abc import ABC
from tms_kit.data import DataGenerator
from tms_kit.loss import LossCalculator
from tms_kit.model import Model


class TMS(ABC):
    """A TMS bundles a model architecture, data generator, and loss calculator."""

    model: Model
    data_gen: DataGenerator
    loss_calc: LossCalculator
