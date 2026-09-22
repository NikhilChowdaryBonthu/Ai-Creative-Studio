# AI Creative Studio

[![Quality checks](https://github.com/NikhilChowdaryBonthu/Ai-Creative-Studio/actions/workflows/quality.yml/badge.svg)](https://github.com/NikhilChowdaryBonthu/Ai-Creative-Studio/actions/workflows/quality.yml)

A text-to-image portfolio project using Stable Diffusion v1.5, PyTorch, Diffusers, and Gradio. It offers a self-contained Google Colab notebook and a separate GPU-hosted Gradio entry point. Prompts, negative prompts, inference steps, guidance, and seed are adjustable.

**Project status:** verified on 2026-09-22 in a Google Colab Tesla T4 runtime. The current notebook loaded the model, generated an example image, and its Gradio interface generated a second image. There is no permanent public hosted demo.

## Verified demo screenshot

The Gradio interface below generated the robot-cafe image during the Colab T4 smoke test. This is a screenshot, not a permanent live demo.

![AI Creative Studio Gradio interface generating a robot cafe image on a Colab T4 GPU](https://github.com/user-attachments/assets/90dc5346-5daf-4d4a-9131-ae9ebf44e465)

[Open full-size screenshot](https://github.com/user-attachments/assets/90dc5346-5daf-4d4a-9131-ae9ebf44e465)

## Try it in Google Colab

1. Open the [notebook in Colab](https://colab.research.google.com/github/NikhilChowdaryBonthu/Ai-Creative-Studio/blob/main/stable_diffusion_studio.ipynb).
2. Choose **Runtime → Change runtime type → GPU**. GPU availability depends on your account and current capacity.
3. Run the cells in order. The notebook keeps Colab's PyTorch installation instead of replacing it with a fixed CUDA wheel.
4. Generate one image, then use the interactive Gradio panel. No Google Drive mount is required.
5. Download an image through Colab's Files panel if you want to keep it.

The first model download can take several minutes. If CUDA is unavailable, the notebook stops with a clear message before downloading the model.

## Run the Gradio app on a CUDA GPU

This path is for a machine or host with a CUDA-compatible GPU and Python 3.10 or newer. Install the appropriate PyTorch build for your hardware first, then:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

The app loads the model on the first generation request and reuses it for later requests. If no CUDA GPU is available, it reports that requirement instead of silently starting a very slow CPU generation. The default model is [Stable Diffusion v1.5](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5); set `MODEL_ID` to use another compatible Diffusers model only after testing it.

## Example images

These example assets are included in the repository. The screenshot above shows a separate, verified run of the current notebook.

| Cyberpunk City | Robot Cafe |
| --- | --- |
| ![Cyberpunk City example](Cyberpunk%20City.jpg) | ![Robot Cafe example](Robot%20Cafe.jpg) |

## Tests and verification

Run the fast checks without a GPU or model download:

```bash
python -m compileall -q app.py studio_core.py tests
python -m unittest discover -s tests -v
```

[GitHub Actions](https://github.com/NikhilChowdaryBonthu/Ai-Creative-Studio/actions/workflows/quality.yml) runs these checks on pushes and pull requests. They cover input validation, generation arguments with a fake pipeline, and notebook integrity. They **do not** execute Stable Diffusion inference.

GPU smoke test completed on 2026-09-22 with a Tesla T4: model loading, one notebook image, and a second Gradio-generated image succeeded. Colab printed dependency warnings about unrelated preinstalled packages, but generation completed. Repeat this test after changing model or dependency versions.

## How it works

- `stable_diffusion_studio.ipynb`: standalone Colab workflow with a single-image example and an interactive panel.
- `app.py`: GPU-backed Gradio web app that loads the model lazily.
- `studio_core.py`: model-independent validation and pipeline invocation.
- `tests/`: fast tests that do not require GPU hardware.
- `huggingface-space.md`: metadata template for a possible Hugging Face Space; it is not a deployment record.

## Hosting and cost

This repository does **not** automatically deploy a Space. A standard GPU Space may incur charges, and a new standard Gradio Space may require a paid plan. An eligible free personal account may be able to host a ZeroGPU Space, but this app would need ZeroGPU-specific integration and a real deployment test first. Do not select paid hardware just to run the portfolio demo.

See the current [Hugging Face Spaces overview](https://huggingface.co/docs/hub/spaces-overview) and [ZeroGPU requirements](https://huggingface.co/docs/hub/spaces-zerogpu) before deploying.

## Responsible use and licenses

This repository's code is MIT-licensed. The model weights have a separate [CreativeML OpenRAIL-M license and model card](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5). Review model limitations, generated outputs, and applicable license terms before publishing or using images.

## Next milestone

A short screen recording could make the project easier to explore, but it is optional. A permanent hosted demo is also optional; the temporary Gradio link created by Colab expires and depends on the runtime.

## Contact

[nikhilbonthu2@gmail.com](mailto:nikhilbonthu2@gmail.com)
