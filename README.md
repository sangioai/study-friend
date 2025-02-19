# 📚StudyFriend

📚StudyFriend is a pool of AI tools that helps me study. 

📚StudyFriend runs AI model locally thanks to the _open-source community_ ❤

📚StudyFriend can: </br>
- Generate a Q&A file from pdfs and images, useful for self-evaluation of study materials.
- Convert pdfs into images.

# ⌰ Collaborations

**❗You're more than welcome to fix, add or suggest study tools.❗**

# ⎑ Installation

To build: </br>
```text
python -m pip install .
```

# ⌖ Usage

To genrate Q&A file from pdfs: </br>
```text
python -m study_friend.query -d ./test  
```

> [!Note]
> **~6GB** of GPU VRAM of unified RAM are required. 


To generate images from pdfs: </br>
```text
python -m study_friend.convert -d ./test
```

To print help: </br>
```text
python -m study_friend.query -h
python -m study_friend.convert -h
```

> [!Tip]
> Use **--image_size** to control the size of converted images.</br>
> The smaller the image size the smoller the amount of memory needed to store the prompt tokens, at the cost of less intepretability of the images.

> [!Tip]
> Use **--title_prompt**, **--question_prompt**, **--answer_prompt** to control the prompts used to query the AI model.</br>
> You can find the default prompts in [utils.py](study_friend/utils.py).

> [!Warning]
> Markdown beatufier heavily depends on prompts templates, change it accordingly or disable it.

# ⏃ Example
[output.md](/tests/output.md) is a Q&A file automatically generated from the slides in [presentation.pdf](/tests/presentation.pdf) (taken from [this](https://github.com/sangioai/torchpace) repo of mine), after being transformed into [these](/tests/presentation) images.

This command was used:</br>
```text
python -m study_friend.query -d ./samples -im 700  
```

On my Mac M1, using default **🤗Qwen2.5-VL-7B-Instruct-4bit** and **--image_size** of 500 it yields:</br>
> Prompt: 69.904 tokens-per-sec </br>
> Generation: 12.865 tokens-per-sec </br>
> Peak memory: 6.206 GB </br>

On my Mac M1, using default **🤗Qwen2.5-VL-7B-Instruct-4bit** and **--image_size** of 700 it yields:</br>
> Prompt: 58.693 tokens-per-sec </br>
> Generation: 11.566 tokens-per-sec </br>
> Peak memory: 7.351 GB </br>


# ⎷ TODO

A brief and incomplete list of things to do or fix in this extension:
- [x] MLX support
- [ ] CUDA support
- [ ] 🤗Transformers integration
- [ ] 🤗smolagents integration

# ☆ Credits

Thanks go to the open-source community that makes this possible.

[mlx-vlm](https://github.com/Blaizzy/mlx-vlm) - Vision model inferencing for MLX.</br>
[🤗Qwen2.5-VL-7B-Instruct-4bit](https://huggingface.co/mlx-community/Qwen2.5-VL-7B-Instruct-4bit) - 🤗HuggingFace 4bit quantized version of [Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL).



# © Author

[Marco Sangiorgi](https://github.com/sangioai)
</br>
*2025©*
