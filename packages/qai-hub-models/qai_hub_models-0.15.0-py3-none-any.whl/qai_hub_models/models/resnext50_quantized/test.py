# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from qai_hub_models.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
)
from qai_hub_models.models.resnext50_quantized.demo import main as demo_main
from qai_hub_models.models.resnext50_quantized.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    ResNeXt50Quantizable,
)


def test_task():
    run_imagenet_classifier_test(
        ResNeXt50Quantizable.from_pretrained(),
        MODEL_ID,
        probability_threshold=0.46,
        diff_tol=0.005,
        rtol=0.02,
        atol=0.2,
        asset_version=MODEL_ASSET_VERSION,
    )


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
