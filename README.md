# 📚StudyFriend

📚StudyFriend is a pool of AI tools that helps me study. 

📚StudyFriend runs AI model locally thanks to the _open-source community_ ❤

📚StudyFriend can: </br>
- Generate a Q&A file from pdfs and images, useful for self-evaluation of study materials.
- Convert pdfs into images.

# ⌰ Collaborations

**❗You're more than welcome to fix, add or suggest study tools.❗**

# ⎑ Installation

To build use python>=3.10: </br>
```text
python -m pip install .
```

> [!Important]
> On Windows: be sure to have [poppler](https://github.com/oschwartz10612/poppler-windows/releases/) /bin in you PATH, as stated in [pdf2image](https://github.com/Belval/pdf2image).


# ⌖ Usage

To genrate Q&A file from pdfs: </br>
```text
python -m study_friend.query -d ./samples  
```

> [!Note]
> On MAC: **~6GB** of unified RAM are required. </br>
> On Windows/Linux: **4GB** of GPU VRAM are required


To generate images from pdfs: </br>
```text
python -m study_friend.convert -d ./samples
```

To print help: </br>
```text
python -m study_friend.query -h
python -m study_friend.convert -h
```

> [!Tip]
> Use `--image_size` to control the size of converted images.</br>
> The smaller the image size the smoller the amount of memory needed to store the prompt tokens, at the cost of less intepretability of the images.

> [!Tip]
> Use `--title_prompt`, `--question_prompt`, `--answer_prompt` to control the prompts used to query the AI model.</br>
> You can find the default prompts in [utils.py](study_friend/utils.py).

> [!Warning]
> Markdown beatufier heavily depends on prompts templates, change it accordingly or disable it.

# ⏃ Example
[output.md](/samples/output.md) is a Q&A file automatically generated from the slides in [presentation.pdf](/samples/presentation.pdf) (taken from [this](https://github.com/sangioai/torchpace) repo of mine), after being transformed into [these](/samples/presentation) images.

This command was used:</br>
```text
python -m study_friend.query -d ./samples -im 700  
```

On my Mac M1, using default `🤗Qwen2.5-VL-7B-Instruct-4bit` and `--image_size` of 500 it yields:</br>
> Prompt: 69.904 tokens-per-sec </br>
> Generation: 12.865 tokens-per-sec </br>
> Peak memory: 6.206 GB </br>

On my Mac M1, using default `🤗Qwen2.5-VL-7B-Instruct-4bit` and `--image_size` of 700 it yields:</br>
> Prompt: 58.693 tokens-per-sec </br>
> Generation: 11.566 tokens-per-sec </br>
> Peak memory: 7.351 GB </br>


# ⎷ TODO

A brief and incomplete list of things to do or fix in this extension:
- [x] MLX support
- [x] CUDA support
- [x] 🤗Transformers integration
- [ ] 🤗smolagents integration

# ☆ Credits

Thanks go to the open-source community that makes this possible.

[mlx-vlm](https://github.com/Blaizzy/mlx-vlm) - Vision model inferencing for MLX.</br>
[mlx-community/Qwen2.5-VL-7B-Instruct-4bit](https://huggingface.co/mlx-community/Qwen2.5-VL-7B-Instruct-4bit) - 🤗HuggingFace quantized version of [Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL) from MLX-community.</br>
[unsloth/Qwen2.5-VL-7B-Instruct-unsloth-bnb-4bit](https://huggingface.co/mlx-community/Qwen2.5-VL-7B-Instruct-4bit) - 🤗HuggingFace quantized version of [Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL) from [unsloth](https://github.com/unslothai/unsloth/).

# ⍰ FAQs

- **I cannot load the model with the following error in the 🤗Transformers library: `ValueError: Unrecognized image processor ...`** </br>
Try installing this commit of 🤗Transformers v4.49.0 as stated [here](https://github.com/huggingface/transformers/issues/36193).</br>
Alternatively, avoid installing 🤗Transformers on build:<br/>
```text
python -m pip install git+https://github.com/huggingface/transformers.git@1931a351408dbd1d0e2c4d6d7ee0eb5e8807d7bf
python -m pip install . --no-dependencies
```

- **I cannot load the model with the following error: `... CUDAOutOfMemory ...` or similar.** </br>
Try playing with the `--group_size` argument starting from 1 upwards, eventually play with the `--image_size` argument:<br/>
```text
python -m study_friend.query -d ./samples -g 1 -im 250 
```

- **How can I make the model generate faster?** </br>
Lower the computational burden by lowering `--image_size` and `--group_size` arguments, eventually use `--max_tokens` to limit output generation at a specified length.

# © Author

[Marco Sangiorgi](https://github.com/sangioai)
</br>
*2025©*
