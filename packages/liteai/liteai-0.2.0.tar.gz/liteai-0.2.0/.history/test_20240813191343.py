chunk_size = 4096 * 10


def gen():
    with open("tests/hello.mp3", "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                return
            logger.debug(f"yielding chunk, with size {len(chunk)}")
            yield chunk


byte_stream = gen()
