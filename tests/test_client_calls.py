import pytest


def test_client1():
    from tests.utils import call_subprocess_onetask
    call_subprocess_onetask(run_client1)


def run_client1():
    from generate import main
    main(base_model='h2oai/h2ogpt-oig-oasst1-512-6.9b', prompt_type='human_bot', chat=False,
         stream_output=False, gradio=True, num_beams=1, block_gradio_exit=False)

    from client_test import test_client_basic
    res_dict = test_client_basic()
    assert res_dict['prompt'] == 'Who are you?'
    assert res_dict['iinput'] == ''
    assert 'I am h2oGPT' in res_dict['response'] or "I'm h2oGPT" in res_dict['response'] or 'I’m h2oGPT' in res_dict[
        'response']


def test_client_chat_nostream():
    from tests.utils import call_subprocess_onetask
    res_dict = call_subprocess_onetask(run_client_chat, kwargs=dict(stream_output=False))
    assert 'I am h2oGPT' in res_dict['response'] or "I'm h2oGPT" in res_dict['response'] or 'I’m h2oGPT' in res_dict[
        'response']


def run_client_chat(prompt='Who are you?', stream_output=False, max_new_tokens=256):
    from generate import main
    main(base_model='h2oai/h2ogpt-oig-oasst1-512-6.9b', prompt_type='human_bot', chat=True,
         stream_output=stream_output, gradio=True, num_beams=1, block_gradio_exit=False,
         max_new_tokens=max_new_tokens)

    from client_test import run_client_chat
    res_dict = run_client_chat(prompt=prompt, prompt_type='human_bot', stream_output=stream_output,
                               max_new_tokens=max_new_tokens)
    assert res_dict['prompt'] == prompt
    assert res_dict['iinput'] == ''
    return res_dict


def test_client_chat_stream():
    from tests.utils import call_subprocess_onetask
    call_subprocess_onetask(run_client_chat, kwargs=dict(stream_output=True))


def test_client_chat_stream_long():
    from tests.utils import call_subprocess_onetask
    prompt = 'Tell a very long story about cute birds for kids.'
    res_dict = call_subprocess_onetask(run_client_chat,
                                       kwargs=dict(prompt=prompt, stream_output=True, max_new_tokens=1024))
    assert 'Once upon a time' in res_dict['response']


@pytest.mark.skip(reason="Local file required")
def test_client_long():
    from tests.utils import call_subprocess_onetask
    call_subprocess_onetask(run_client_long)


def run_client_long():
    from generate import main
    main(base_model='mosaicml/mpt-7b-storywriter', prompt_type='plain', chat=False,
         stream_output=False, gradio=True, num_beams=1, block_gradio_exit=False)

    with open("/home/jon/Downloads/Gatsby_PDF_FullText.txt") as f:
        prompt = f.readlines()

    from client_test import run_client_nochat
    res_dict = run_client_nochat(prompt=prompt, prompt_type='plain')
    print(res_dict['response'])
