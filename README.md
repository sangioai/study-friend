# 📚StudyFriend

📚StudyFriend is a pool of AI tools that helps me study. 

📚StudyFriend runs AI model locally thanks to the _open-source community_ ❤

📚StudyFriend can:
-  Generate a Q&A file from pdfs and images, useful for self-evaluation of study materials.

# ⎑ Installation

To build: </br>
```text
python -m pip install .
```

# ⌖ Usage

To genrate Q&A file from pdfs: </br>
```text
python -m pip install .
```

To generate images from pdfs: </br>
```text
python -m pip install .
```

To print help: </br>
```text
python -m pip install .
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
[output.md](/tests/output.md) is a Q&A file automatically generated from the slides in [presentation.pdf](/tests/presentation.pdf) (taken from [this](https://github.com/sangioai/torchpace) repo of mine), after being transformed into [these](/tests/presentation) images. </br>
The command to do so is:</br>
```text
python -m study_friend.query -d ./test -im 700  
```

On my Mac M1, using **--image_size** of 500 it yields:</br>
> Prompt: 320 tokens, 87.693 tokens-per-sec</br>
> Generation: 9 tokens, 15.169 tokens-per-sec</br>
> Peak memory: 5.916 GB</br>

On my Mac M1, using **--image_size** of 700 it yields:</br>
> Prompt: 1145 tokens, 58.693 tokens-per-sec</br>
> Generation: 159 tokens, 11.566 tokens-per-sec</br>
> Peak memory: 7.351 GB</br>


## ☑ TODO

A brief and incomplete list of things to do or fix in this extension:
- [x] MLX support
- [ ] CUDA support
- [ ] 🤗Transformers integration
- [ ] 🤗smolagents integration

## ⍾ Credits

[mlx-vlm](https://github.com/Blaizzy/mlx-vlm) - Vision model inferencing for MLX.

[🤗Qwen2.5-VL-7B-Instruct-4bit](https://huggingface.co/mlx-community/Qwen2.5-VL-7B-Instruct-4bit) - 🤗HuggingFace 4bit-quantized version of [Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL). Visione Model.


## ☆ Collaborations

You're more than welcome to fix, add or suggest things.

Feel free to contact me.

## © Author

[Marco Sangiorgi](https://github.com/sangioai)
</br>
*2025©*
