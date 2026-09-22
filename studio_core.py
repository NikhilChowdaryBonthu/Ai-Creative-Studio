"""GPU-independent request validation and pipeline invocation."""

MODEL_ID = "stable-diffusion-v1-5/stable-diffusion-v1-5"


def prepare_request(prompt, negative_prompt, steps, guidance_scale, seed):
    """Validate Gradio inputs before loading the large model."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Please enter a prompt before generating an image.")

    try:
        steps = int(steps)
        guidance_scale = float(guidance_scale)
        seed = int(seed)
    except (TypeError, ValueError) as exc:
        raise ValueError("Generation settings must be numeric.") from exc

    if not 10 <= steps <= 50:
        raise ValueError("Inference steps must be between 10 and 50.")
    if not 1.0 <= guidance_scale <= 15.0:
        raise ValueError("Guidance scale must be between 1 and 15.")
    if not 0 <= seed <= 2_147_483_647:
        raise ValueError("Seed must be between 0 and 2147483647.")

    return {
        "prompt": prompt.strip(),
        "negative_prompt": negative_prompt.strip() or None
        if isinstance(negative_prompt, str) else None,
        "num_inference_steps": steps,
        "guidance_scale": guidance_scale,
        "seed": seed,
    }


def run_pipeline(pipeline, generator, request):
    """Invoke an injected pipeline; this can be unit-tested without a GPU."""
    result = pipeline(
        prompt=request["prompt"],
        negative_prompt=request["negative_prompt"],
        num_inference_steps=request["num_inference_steps"],
        guidance_scale=request["guidance_scale"],
        generator=generator,
    )
    if not getattr(result, "images", None):
        raise RuntimeError("The model did not return an image.")
    return result.images[0]
