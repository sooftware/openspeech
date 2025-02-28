import unittest
import torch
import logging

from openspeech.criterion.transducer.transducer import TransducerLossConfigs
from openspeech.models import RNNTransducerModel, RNNTransducerConfigs
from openspeech.utils import DUMMY_INPUTS, DUMMY_INPUT_LENGTHS, DUMMY_TARGETS, DUMMY_TARGET_LENGTHS, \
    build_dummy_configs, WARPRNNT_IMPORT_ERROR
from openspeech.tokenizers.ksponspeech.character import KsponSpeechCharacterTokenizer

try:
    from warp_rnnt import rnnt_loss
except ImportError:
    raise ImportError(WARPRNNT_IMPORT_ERROR)

logger = logging.getLogger(__name__)


class TestRNNTransducer(unittest.TestCase):
    def test_forward(self):
        configs = build_dummy_configs(
            model_configs=RNNTransducerConfigs(),
            criterion_configs=TransducerLossConfigs(),
        )

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = RNNTransducerModel(configs, vocab)
        model.build_model()

        optimizer = torch.optim.Adam(model.parameters(), lr=1e-04)

        for i in range(3):
            outputs = model(DUMMY_INPUTS, DUMMY_INPUT_LENGTHS)

            loss = rnnt_loss(
                outputs["logits"],
                DUMMY_TARGETS,
                DUMMY_INPUT_LENGTHS,
                DUMMY_TARGET_LENGTHS,
                reduction="mean",
                blank=vocab.blank_id,
                gather=True,
            )
            loss.backward()
            optimizer.step()
            assert type(loss.item()) == float

    def test_beam_search(self):
        configs = build_dummy_configs(
            model_configs=RNNTransducerConfigs(),
            criterion_configs=TransducerLossConfigs(),
        )

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = RNNTransducerModel(configs, vocab)
        model.build_model()
        model.set_beam_decode(beam_size=3)

        for i in range(3):
            prediction = model(DUMMY_INPUTS, DUMMY_INPUT_LENGTHS)["predictions"]
            assert isinstance(prediction, torch.Tensor)

    def test_training_step(self):
        configs = build_dummy_configs(
            model_configs=RNNTransducerConfigs(),
            criterion_configs=TransducerLossConfigs(),
        )

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = RNNTransducerModel(configs, vocab)
        model.build_model()

        for i in range(3):
            outputs = model.training_step(
                batch=(DUMMY_INPUTS, DUMMY_TARGETS, DUMMY_INPUT_LENGTHS, DUMMY_TARGET_LENGTHS), batch_idx=i
            )
            assert type(outputs["loss"].item()) == float

    def test_validation_step(self):
        configs = build_dummy_configs(
            model_configs=RNNTransducerConfigs(),
            criterion_configs=TransducerLossConfigs(),
        )

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = RNNTransducerModel(configs, vocab)
        model.build_model()

        for i in range(3):
            outputs = model.validation_step(
                batch=(DUMMY_INPUTS, DUMMY_TARGETS, DUMMY_INPUT_LENGTHS, DUMMY_TARGET_LENGTHS), batch_idx=i
            )
            assert type(outputs["loss"].item()) == float

    def test_test_step(self):
        configs = build_dummy_configs(
            model_configs=RNNTransducerConfigs(),
            criterion_configs=TransducerLossConfigs(),
        )

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = RNNTransducerModel(configs, vocab)
        model.build_model()

        for i in range(3):
            outputs = model.test_step(
                batch=(DUMMY_INPUTS, DUMMY_TARGETS, DUMMY_INPUT_LENGTHS, DUMMY_TARGET_LENGTHS), batch_idx=i
            )
            assert type(outputs["loss"].item()) == float


if __name__ == '__main__':
    unittest.main()
