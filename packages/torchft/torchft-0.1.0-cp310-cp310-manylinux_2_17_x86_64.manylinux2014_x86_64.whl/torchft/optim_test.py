from torchft.optim import OptimizerWrapper
from torchft.manager import Manager
from torch.nn import Linear
from torch.optim import AdamW

from unittest import TestCase
from unittest.mock import MagicMock, create_autospec


class TestOptim(TestCase):
    def test_optimizer_wrapper(self) -> None:
        manager = create_autospec(Manager)

        m = Linear(3, 4)
        base_optim = AdamW(m.parameters())
        optim = OptimizerWrapper(manager, base_optim)
        optim.add_param_group(
            {
                "params": [],
                "lr": 1e-4,
            }
        )

        # test state_dict handling
        optim.load_state_dict(optim.state_dict())

        optim.zero_grad()
        self.assertEqual(manager.step.call_count, 1)

        manager.should_commit.return_value = True
        optim.step()
        manager.should_commit.return_value = False
        optim.step()

        self.assertEqual(manager.should_commit.call_count, 2)
