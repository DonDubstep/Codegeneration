from typing import List
import torch
from settings import CUDA

# signals the start of a document
BOS = "<|endoftext|>"
# signals the end of a generated infill
EOM = "<|endofmask|>"

def make_sentinel(i):
    """
    Signals (1) a location to insert an infill and (2) the start of the infill generation
    """
    return f"<|mask:{i}|>"

def del_EOM(completion):
    """
    Remove signals "<|endofmask|>"
    """
    while EOM in completion:
        completion = completion[:completion.find(EOM)] + completion[completion.find(EOM)+len(EOM):]
    return completion

def del_extra_returns(completion):
    """
    Remove everything after first "return"
    """
    arr = completion.split('\n')
    res = ""
    for i in range(len(arr)):
        if "return" in arr[i]:
            for el in range(i+1):
                res += arr[el]
                res += "\n"
            break
    return res

def generate(model, tokenizer, input: str, max_to_generate: int = 128, temperature: float = 0.2):
    """
    Do standard left-to-right completion of the prefix `input` by sampling from the model
    """
    input_ids = tokenizer(input, return_tensors="pt").input_ids
    if CUDA:
        input_ids = input_ids.cuda()
    max_length = max_to_generate + input_ids.flatten().size(0)
    if max_length > 2048:
        print("warning: max_length {} is greater than the context window {}".format(max_length, 2048))
    with torch.no_grad():
        output = model.generate(input_ids=input_ids, do_sample=True, top_p=0.95, temperature=temperature,
                                max_length=max_length)
    detok_hypo_str = tokenizer.decode(output.flatten(), clean_up_tokenization_spaces=False)
    if detok_hypo_str.startswith(BOS):
        detok_hypo_str = detok_hypo_str[len(BOS):]
    return detok_hypo_str


def infill(parts: List[str], model, tokenizer, max_to_generate: int = 128, temperature: float = 0.2, extra_sentinel: bool = True):
    """
    In this func, the request is masked and sent to generation func.
    The cycle repeats until an acceptable code is generated
    """
    assert isinstance(parts, list)
    while (1):
        if len(parts) == 1:
            prompt = parts[0]
        else:
            prompt = ""
            # encode parts separated by sentinel
            for sentinel_ix, part in enumerate(parts):
                prompt += part
                if extra_sentinel or (sentinel_ix < len(parts) - 1):
                    prompt += make_sentinel(sentinel_ix)
        prompt += make_sentinel(0)
        completion = generate(model, tokenizer, prompt, max_to_generate, temperature)
        completion = completion[len(prompt):]
        complete = "def " + del_EOM(completion)
        complete = del_extra_returns(complete)
        try:
            complete[len("def "):complete.index("(")]
            if EOM not in completion:
                continue
            break
        except ValueError:
            print(" ")
    text = ''.join(complete)
    return text

def docstring_to_code(input_prompt, model, tokenizer, max_to_generate=128, temperature=0.6):
    """
    Creating prompt for the model and sent it to generation func
    :param input_prompt: user request
    :param model: code-generation model
    :param tokenizer: tokenizer for code-generation model
    :param max_to_generate: max length of generated code
    :param temperature: variability
    :return: generated code
    """
    example = '''\
def <insert>
    """''' + input_prompt + '''"""
    <insert>
<|/ file |>'''
    parts = example.split("<insert>")
    result = infill(parts, model, tokenizer, max_to_generate=max_to_generate, temperature=temperature)
    return result
