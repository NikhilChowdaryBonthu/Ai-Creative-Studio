import os
from functools import lru_cache

import gradio as gr
import torch
from diffusers import StableDiffusionPipeline

MODEL_ID = os.getenv("MODEL_ID", "runwayml/stable-diffusion-v1-5")


@lru_cache(maxsize=1)
def load_pipeline():
    """Load Stable Diffusion once and reuse it for subsequent requests."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    pipeline = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        use_safetensors=True,
    )
    pipeline = pipeline.to(device)
    pipeline.enable_attention_slicing()
    return pipeline, device


def generate_image(prompt, negative_prompt, steps, guidance_scale, seed):
    if not prompt or not prompt.strip():
        raise gr.Error("Please enter a prompt before generating an image.")

    pipeline, device = load_pipeline()
    generator = torch.Generator(device=device).manual_seed(int(seed))

    with torch.inference_mode():
        image = pipeline(
            prompt=prompt.strip(),
            negative_prompt=negative_prompt.strip() or None,
            num_inference_steps=int(steps),
            guidance_scale=float(guidance_scale),
            generator=generator,
        ).images[0]

    return image


with gr.Blocks(title="AI Creative Studio") as demo:
    gr.Markdown(
        """
        # 🎨 AI Creative Studio
        Create images from text prompts with Stable Diffusion.
        Choose a prompt, tune the settings, and select **Generate image**.
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

if __name__ == "__main__":
    demo.launch()
