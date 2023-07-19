import sys
import os
import streamlit as st
import importlib
import inspect
import time

# Adding parent directory. If this page isn't working, delete next 3 strings.
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(parent_directory)

from run_incoder2 import docstring_to_code
from tasks_for_passak import tasks
test_num = 0

# Sidebar with input parameters to generate
with st.sidebar:
    temperature = st.slider("Temperature", min_value=0.1, value=0.2, max_value=1.0, step=0.1)
    st.caption(r"Temperature - гиперпараметр контроля случайности прогнозов модели. \
               Чем выше значение, тем более разнообразные и не точные результаты генерирует модель.\
               Чем меньше - тем более однообразные и точные ответы.")
    max_tokens = st.slider("Max tokens", min_value=128, max_value=2048, step=128)
    st.caption("Max tokens - максимальное количество генерируемых слов и символов")
    passak_k = st.slider("pass@k", min_value=1, max_value=10)

# Header and description
st.markdown("# Тестирование модели метрикой pass@k, где k={}".format(passak_k))
st.markdown("Здесь предлагается протестировать модель с помощью следующих задач:")
for key in tasks:
    st.markdown("<li>"+key + "</li>", unsafe_allow_html=True)

# start evaluation of model
keys = [key for key in tasks]
button_generate = st.button("Начать генерацию")
generation_logs = ""

if button_generate:
    text_area_generation_info = st.empty()
    solved = 0
    for key in tasks:
        input_prompt = key
        generation_logs += "[Генерация] {} Генерация запроса: {}\n".format(test_num, key)
        text_area_generation_info.text_area("Состояние", generation_logs, height=1600)
        for trial in range(passak_k):
            generated = docstring_to_code(input_prompt, st.session_state.model, st.session_state.tokenizer,
                                          max_to_generate=max_tokens, temperature=temperature)
            with open("Tests/Test{}/test_code{}.py".format(test_num, trial), "w") as file:
                file.write(generated)
            time.sleep(0.7)
            func_name = (generated[len("def "):generated.index("(")])

            request1 = tasks[key][0][0]
            request2 = tasks[key][0][1]
            request3 = tasks[key][0][2]
            answer1 = tasks[key][1][0]
            answer2 = tasks[key][1][1]
            answer3 = tasks[key][1][2]

            try:
                file = importlib.import_module("Tests.Test{}.test_code{}".format(test_num, trial))
                func_from_file = getattr(file, str(func_name))
                if len(inspect.signature(func_from_file).parameters) == 1:
                    response1 = func_from_file(request1)
                    response2 = func_from_file(request2)
                    response3 = func_from_file(request3)
                elif len(inspect.signature(func_from_file).parameters) == 2:
                    response1 = func_from_file(request1[0], request1[1])
                    response2 = func_from_file(request2[0], request2[1])
                    response3 = func_from_file(request3[0], request3[1])
                elif len(inspect.signature(func_from_file).parameters) == 3:
                    response1 = func_from_file(request1[0], request1[1], request1[2])
                    response2 = func_from_file(request2[0], request2[1], request2[2])
                    response3 = func_from_file(request3[0], request3[1], request3[2])
                if answer1 == response1 and answer2 == response2 and answer3 == response3:
                    generation_logs += "[Тест] {} Tест пройден\n".format(test_num)
                    solved += 1
                    break
                else:
                    generation_logs += "[Тест] {} Tест не пройден\n".format(test_num)
            except:
                generation_logs += "[Тест] {} Tест не пройден - исключение\n".format(test_num)
                print("Исключение")
            text_area_generation_info.text_area("Состояние", generation_logs, height=1600)
        test_num += 1
    st.text("Результаты:")
    st.markdown("pass@{}={}%".format(passak_k, solved/len(tasks)*100))
