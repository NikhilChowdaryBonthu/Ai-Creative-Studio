# AI Creative Studio

A Google Colab-based text-to-image project built with Stable Diffusion. Generate original artwork from text prompts directly in your browser through an interactive Gradio interface.

## Highlights

- Text-to-image generation with Stable Diffusion
- Interactive Gradio interface for prompts, negative prompts, and generation controls
- Runs in Google Colab — no local setup required
- Includes a deployable web-app entry point for Hugging Face Spaces
- GPU-enabled image generation with PyTorch and CUDA
- Reproducible outputs using prompt, inference-step, guidance, and seed controls

## Quick start

1. Open the [Stable Diffusion Studio notebook in Google Colab](https://colab.research.google.com/github/NikhilChowdaryBonthu/Ai-Creative-Studio/blob/main/stable_diffusion_studio.ipynb).
2. In Colab, select **Runtime → Change runtime type** and choose a GPU.
3. Select **Runtime → Run all** and wait for the model to download.
4. Use the Gradio interface to enter a prompt, adjust settings, and select **Generate**.

## Deploy as a web app

The repository includes `app.py`, which is ready for a Hugging Face Space.

1. Create a new **Gradio** Space with a GPU runtime.
2. Upload `app.py`, `requirements.txt`, and the contents of `huggingface-space.md` as the Space's `README.md`.
3. The Space will install dependencies and launch the app automatically.

> Stable Diffusion needs a GPU for a practical public demo. Choose hardware in Hugging Face that matches your budget and availability.

## Example generations

### Cyberpunk City

![Cyberpunk City](https://github.com/NikhilChowdaryBonthu/Ai-Creative-Studio/blob/main/Cyberpunk%20City.jpg?raw=true)

### Robot Cafe

![Robot Cafe](https://github.com/NikhilChowdaryBonthu/Ai-Creative-Studio/blob/main/Robot%20Cafe.jpg?raw=true)

## Tech stack

- Python 3.10
- PyTorch and CUDA
- Hugging Face Diffusers
- Gradio
- Google Colab

## Notes

- A GPU-backed Colab runtime is required; the notebook checks for CUDA before loading the model.
- Download time and GPU availability may affect the first run.
- Results depend on the prompt and model configuration.

## License

This project is available under the [MIT License](LICENSE).

## Contact

For questions, contact [nikhilbonthu2@gmail.com](mailto:nikhilbonthu2@gmail.com).
