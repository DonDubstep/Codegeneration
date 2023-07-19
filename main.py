import streamlit as st
from run_incoder2 import docstring_to_code
from transformers import AutoModelForCausalLM, AutoTokenizer
from settings import CUDA, cache_dir, MODEL_NAME

@st.cache_resource
def initializing_model():
    """
    Download and initialization model InCoder-1.3B from HuggingFace.
    A folder "cache_dir" will be created in this directory and model will be loaded into it
    :return: model InCoder-1.3B
    """
    model_name = MODEL_NAME
    kwargs = {}
    model = AutoModelForCausalLM.from_pretrained(model_name, **kwargs, cache_dir=cache_dir)
    if CUDA:
        model = model.half().cuda()
    return model

@st.cache_resource
def initializing_tokenizer():
    """
    Download tokenizer into the "cache_dir" folder and initialization
    :return: tokenizer
    """
    model_name = MODEL_NAME
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
    return tokenizer

# Sidebar with input parameters to generate
with st.sidebar:
    temperature = st.slider("Temperature", min_value=0.1, max_value=1.0, value=0.2, step=0.1)
    st.caption(r"Temperature - гиперпараметр контроля случайности прогнозов. \
               Чем выше значение, тем более разнообразные и не точные результаты генерирует модель.\
               Чем меньше - тем более однообразные и точные ответы.")
    max_tokens = st.slider("Max tokens", min_value=128, max_value=2048, step=128)
    st.caption("Max tokens - максимальное количество генерируемых слов и символов")
    clear_button = st.button("Очистить")
    if clear_button:
        with open("test_code.py", "w") as file:
            file.write("")


# Initialization model and tokenizer
progress_text = st.text("Загрузка модели...")
st.session_state.model = initializing_model()
progress_text.text("Загрузка токенизатора...")
st.session_state.tokenizer = initializing_tokenizer()
progress_text.text("Модель загружена успешно!")
st.markdown("<hr>", unsafe_allow_html=True)

# Testing requests
test1_button = st.button("Сгенерировать первый запрос")
check_button1 = st.button("Проверить первый запрос")
test2_button = st.button("Сгенерировать второй запрос")
check_button2 = st.button("Проверить второй запрос")
input_prompt_text = st.empty()
generate_progress_text = st.empty()
result_area = st.empty()

if test1_button:
    st.session_state.input_prompt = "is string is palindrome"
    input_prompt_text.text_input("Запрос", st.session_state.input_prompt)
    with open("test_code.py", "w") as file:
        file.write("")
    generated_text = docstring_to_code(st.session_state.input_prompt , st.session_state.model, st.session_state.tokenizer, max_tokens,
                                       temperature)
    result_area.text_area("Сгенерированный код", generated_text)
    st.session_state.func_name = generated_text[len("def "):generated_text.index("(")]
    with open("test_code.py", "w") as file:
        file.write(generated_text)

if check_button1:
    try:
        import test_code
    except:
        state_of_file = st.text("Сгенерирован некорректный код!")
    result = getattr(test_code, st.session_state.func_name)
    test_inputs = ["palindrome", "qwertytrewq", "ef33fe"]
    answers = [False, True, True]
    passed = 0
    n_test = 0
    for test_generate_input in test_inputs:
        answer = answers[n_test]
        n_test += 1
        response = result(test_generate_input)
        st.text("Запрос: \"{}\", ответ: {}".format(test_generate_input, response))
        if response == answer:
            passed += 1
    if passed == 3:
        st.text("Тест пройден")
    else:
        st.text("Тест не пройден")


if test2_button:
    st.session_state.input_prompt = "String To Lower Case"
    input_prompt_text.text_input("Запрос", st.session_state.input_prompt)
    with open("test_code.py", "w") as file:
        file.write("")
    generated_text = docstring_to_code(st.session_state.input_prompt , st.session_state.model, st.session_state.tokenizer, max_tokens,
                                       temperature)
    result_area.text_area("Сгенерированный код", generated_text)
    st.session_state.func_name = generated_text[len("def "):generated_text.index("(")]
    with open("test_code.py", "w") as file:
        file.write(generated_text)

if check_button2:
    try:
        import test_code
    except:
        state_of_file = st.text("Сгенерирован некорректный код!")
    result = getattr(test_code, st.session_state.func_name)
    test_inputs = ["Hello","here","LOVELY"]
    answers = ["hello","here","lovely"]
    passed = 0
    n_test = 0
    for test_generate_input in test_inputs:
        answer = answers[n_test]
        n_test += 1
        response = result(test_generate_input)
        st.text("Запрос: \"{}\", ответ: {}".format(test_generate_input, response))
        if response == answer:
            passed += 1
    if passed == 3:
        st.text("Тест пройден")
    else:
        st.text("Тест не пройден")

st.markdown("<hr>", unsafe_allow_html=True)

# Generation based on user requests
input_prompt = st.text_input("Введите запрос", "Number of words in string")
generate_button = st.button("Сгенерировать код")
if generate_button:
    with open("test_code.py", "w") as file:
        file.write("")
    generate_progress_text.text("Генерация кода...")
    generated_text = docstring_to_code(input_prompt, st.session_state.model, st.session_state.tokenizer, max_tokens,
                                       temperature)
    st.session_state.func_name = generated_text[len("def "):generated_text.index("(")]
    generate_progress_text.empty()
    with open("test_code.py", "w") as file:
        file.write(generated_text)
with open("test_code.py", "r") as file:
    generated_text = file.read()
result_area = st.text_area("Сгенерированный код", generated_text, height=200)

# Checking the code
number_of_args = st.radio("Количество аргументов:", (1, 2, 3))
if number_of_args > 1:
    st.text("Вводите аргументы через пробел")
type_of_args = st.radio("Тип передаваемых аргументов:", ("строка", "целый", "вещественный"))
test_generate_input = st.text_input("Аргументы для проверки:")
check_code_button = st.button("Проверить код")
state_of_file = st.empty()
if check_code_button:
    try:
        import test_code
    except:
        state_of_file = st.text("Сгенерирован некорректный код!")
    result = getattr(test_code, st.session_state.func_name) #
    st.text("Результат работы сгененрированного кода:")
    try:
        if number_of_args == 1:
            test_area = st.text(result(eval(test_generate_input)))
        elif number_of_args == 2:
            arg1 = test_generate_input.split()[0]
            arg2 = test_generate_input.split()[1]
            if type_of_args == "целый":
                test_area = st.text(result(int(arg1), int(arg2)))
            elif type_of_args == "строка":
                test_area = st.text(result(eval(arg1), eval(arg2)))
            elif type_of_args == "вещественный":
                test_area = st.text(result(float(arg1), float(arg2)))
        elif number_of_args == 3:
            arg1 = test_generate_input.split()[0]
            arg2 = test_generate_input.split()[1]
            arg3 = test_generate_input.split()[2]
            if type_of_args == "целый":
                test_area = st.text(result(int(arg1), int(arg2), int(arg3)))
            elif type_of_args == "строка":
                test_area = st.text(result(eval(arg1), eval(arg2), eval(arg3)))
            elif type_of_args == "вещественный":
                test_area = st.text(result(float(arg1), float(arg2), float(arg3)))
    except:
        test_area = st.text("Неправильно введены аргументы!\nВозможно вы забыли заключить строку в кавычки")
