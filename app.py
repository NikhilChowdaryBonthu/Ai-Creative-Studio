"""Gradio entry point for the GPU-backed image generator."""

import os
from functools import lru_cache

import gradio as gr
import torch
from diffusers import StableDiffusionPipeline

from studio_core import MODEL_ID as DEFAULT_MODEL_ID
from studio_core import prepare_request, run_pipeline

MODEL_ID = os.getenv("MODEL_ID", DEFAULT_MODEL_ID)


@lru_cache(maxsize=1)
def load_pipeline():
    """Load the model once, on demand, after checking GPU availability."""
    if not torch.cuda.is_available():
        raise RuntimeError(
            "A CUDA GPU is required. Select a GPU runtime in Colab or your host."
        )

    pipeline = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        use_safetensors=True,
    )
    pipeline = pipeline.to("cuda")
    pipeline.enable_attention_slicing()
    return pipeline


def generate_image(prompt, negative_prompt, steps, guidance_scale, seed):
    try:
        request = prepare_request(
            prompt, negative_prompt, steps, guidance_scale, seed
        )
    except ValueError as exc:
        raise gr.Error(str(exc)) from exc

    try:
        pipeline = load_pipeline()
        generator = torch.Generator(device="cuda").manual_seed(request["seed"])
        with torch.inference_mode():
            return run_pipeline(pipeline, generator, request)
    except RuntimeError as exc:
        raise gr.Error(str(exc)) from exc
    except Exception as exc:
        raise gr.Error(
            "Generation failed. Check the GPU runtime, model access, and logs."
        ) from exc


with gr.Blocks(title="AI Creative Studio") as demo:
    gr.Markdown(
        """
        # 🎨 AI Creative Studio
        Generate images from text with Stable Diffusion v1.5.
        A CUDA GPU is required. Model loading can take several minutes on the first run.
        """
    )

    with gr.Row():
        with gr.Column():
            prompt = gr.Textbox(
                label="Prompt",
                placeholder="A futuristic city at sunset, cinematic lighting",
                lines=4,
            )
            negative_prompt = gr.Textbox(
                label="Negative prompt (optional)",
                placeholder="blurry, low quality, distorted",
                lines=2,
            )
            with gr.Row():
                steps = gr.Slider(10, 50, value=30, step=1, label="Inference steps")
                guidance = gr.Slider(1.0, 15.0, value=7.5, step=0.5, label="Guidance scale")
            seed = gr.Slider(0, 2147483647, value=42, step=1, label="Seed")
            generate = gr.Button("Generate image", variant="primary")

        with gr.Column():
            output = gr.Image(label="Generated image", type="pil")

    generate.click(
        fn=generate_image,
        inputs=[prompt, negative_prompt, steps, guidance, seed],
        outputs=output,
    )

    gr.Examples(
        examples=[
            ["cyberpunk city with neon lights, rainy streets", "blurry, low quality", 30, 7.5, 42],
            ["a cozy robot cafe, warm lighting, digital art", "blurry, low quality", 30, 7.5, 123],
        ],
        inputs=[prompt, negative_prompt, steps, guidance, seed],
    )

    gr.Markdown(
        "Model: [Stable Diffusion v1.5](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5). "
        "Outputs are AI-generated and should be reviewed before sharing."
    )


if __name__ == "__main__":
    demo.launch()
