# AI Creative Studio

A Google Colab-based text-to-image project built with Stable Diffusion. Generate original artwork from text prompts directly in your browser through an interactive Gradio interface.

## Highlights

- Text-to-image generation with Stable Diffusion
- Interactive Gradio interface for prompts and generation controls
- Runs in Google Colab — no local setup required
- GPU-enabled image generation with PyTorch and CUDA
- Reproducible outputs using prompt, inference-step, guidance, and seed controls

## Quick start

1. Open the [Stable Diffusion Studio notebook in Google Colab](https://colab.research.google.com/github/NikhilChowdaryBonthu/Ai-Creative-Studio/blob/main/stable_diffusion_studio.ipynb).
2. In Colab, select **Runtime → Change runtime type** and choose a GPU.
3. Select **Runtime → Run all** and wait for the model to download.
4. Use the Gradio interface to enter a prompt, adjust settings, and select **Generate**.

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
