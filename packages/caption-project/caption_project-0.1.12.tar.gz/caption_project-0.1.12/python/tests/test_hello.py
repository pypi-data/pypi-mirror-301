def test_hello():
    from caption_project._lowlevel import hello

    assert hello() == "Hello from caption-project!"
