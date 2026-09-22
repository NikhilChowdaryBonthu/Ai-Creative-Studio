import json
import unittest
from pathlib import Path
from types import SimpleNamespace

from studio_core import MODEL_ID, prepare_request, run_pipeline


class RequestTests(unittest.TestCase):
    def test_normalizes_valid_request(self):
        request = prepare_request("  a robot cafe  ", " blurry ", 30, 7.5, 42)
        self.assertEqual(request["prompt"], "a robot cafe")
        self.assertEqual(request["negative_prompt"], "blurry")
        self.assertEqual(request["num_inference_steps"], 30)
        self.assertEqual(request["guidance_scale"], 7.5)
        self.assertEqual(request["seed"], 42)

    def test_blank_prompt_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "prompt"):
            prepare_request("  ", "", 30, 7.5, 42)

    def test_missing_negative_prompt_is_allowed(self):
        self.assertIsNone(prepare_request("dog", None, 30, 7.5, 42)["negative_prompt"])

    def test_settings_are_bounded(self):
        for steps, guidance, seed in [(9, 7.5, 42), (51, 7.5, 42),
                                      (30, 0.5, 42), (30, 16, 42),
                                      (30, 7.5, -1), (30, 7.5, 2147483648)]:
            with self.subTest(steps=steps, guidance=guidance, seed=seed):
                with self.assertRaises(ValueError):
                    prepare_request("dog", "", steps, guidance, seed)

    def test_non_numeric_settings_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "numeric"):
            prepare_request("dog", "", "many", 7.5, 42)


class PipelineTests(unittest.TestCase):
    def test_pipeline_receives_validated_settings(self):
        seen = {}
        def pipeline(**kwargs):
            seen.update(kwargs)
            return SimpleNamespace(images=["sample-image"])
        request = prepare_request("dog", "", 30, 7.5, 42)
        self.assertEqual(run_pipeline(pipeline, "seeded-generator", request), "sample-image")
        self.assertEqual(seen["prompt"], "dog")
        self.assertEqual(seen["negative_prompt"], None)
        self.assertEqual(seen["num_inference_steps"], 30)
        self.assertEqual(seen["generator"], "seeded-generator")

    def test_missing_image_is_rejected(self):
        request = prepare_request("dog", "", 30, 7.5, 42)
        with self.assertRaisesRegex(RuntimeError, "did not return an image"):
            run_pipeline(lambda **kwargs: SimpleNamespace(images=[]), None, request)


class NotebookTests(unittest.TestCase):
    def test_notebook_is_clean_and_uses_same_model(self):
        notebook = json.loads(Path("stable_diffusion_studio.ipynb").read_text())
        code = "\n".join(
            "".join(cell["source"]) for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        )
        self.assertIn(MODEL_ID, code)
        self.assertNotIn("runwayml/stable-diffusion-v1-5", code)
        self.assertNotIn("pip uninstall", code)
        self.assertNotIn("drive.mount", code)
        self.assertTrue(all(
            cell.get("execution_count") is None and not cell.get("outputs")
            for cell in notebook["cells"] if cell["cell_type"] == "code"
        ))


if __name__ == "__main__":
    unittest.main()
