import unittest
import torch
import torch.nn as nn
import logging

from openspeech.criterion.ctc.ctc import CTCLossConfigs
from openspeech.models import ConformerConfigs, ConformerModel
from openspeech.utils import DUMMY_INPUTS, DUMMY_INPUT_LENGTHS, DUMMY_TARGETS, DUMMY_TARGET_LENGTHS, build_dummy_configs
from openspeech.tokenizers.ksponspeech.character import KsponSpeechCharacterTokenizer

logger = logging.getLogger(__name__)


class TestConformer(unittest.TestCase):
    def test_forward(self):
        configs = build_dummy_configs(model_configs=ConformerConfigs(), criterion_configs=CTCLossConfigs())

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = ConformerModel(configs, vocab)
        model.build_model()

        criterion = nn.CTCLoss(blank=3, reduction='mean', zero_infinity=True)
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-04)

        for i in range(10):
            outputs = model(DUMMY_INPUTS, DUMMY_INPUT_LENGTHS)

            loss = criterion(
                outputs["logits"].transpose(0, 1),
                DUMMY_TARGETS[:, 1:],
                outputs["output_lengths"],
                DUMMY_TARGET_LENGTHS,
            )
            loss.backward()
            optimizer.step()
            assert type(loss.item()) == float

    def test_training_step(self):
        configs = build_dummy_configs(model_configs=ConformerConfigs(), criterion_configs=CTCLossConfigs())

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = ConformerModel(configs, vocab)
        model.build_model()

        for i in range(5):
            outputs = model.training_step(
                batch=(DUMMY_INPUTS, DUMMY_TARGETS, DUMMY_INPUT_LENGTHS, DUMMY_TARGET_LENGTHS), batch_idx=i
            )
            assert type(outputs["loss"].item()) == float

    def test_validation_step(self):
        configs = build_dummy_configs(model_configs=ConformerConfigs(), criterion_configs=CTCLossConfigs())

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = ConformerModel(configs, vocab)
        model.build_model()

        for i in range(5):
            outputs = model.validation_step(
                batch=(DUMMY_INPUTS, DUMMY_TARGETS, DUMMY_INPUT_LENGTHS, DUMMY_TARGET_LENGTHS), batch_idx=i
            )
            assert type(outputs["loss"].item()) == float

    def test_test_step(self):
        configs = build_dummy_configs(model_configs=ConformerConfigs(), criterion_configs=CTCLossConfigs())

        vocab = KsponSpeechCharacterTokenizer(configs)
        model = ConformerModel(configs, vocab)
        model.build_model()

        for i in range(5):
            outputs = model.test_step(
                batch=(DUMMY_INPUTS, DUMMY_TARGETS, DUMMY_INPUT_LENGTHS, DUMMY_TARGET_LENGTHS), batch_idx=i
            )
            assert type(outputs["loss"].item()) == float


if __name__ == '__main__':
    unittest.main()
