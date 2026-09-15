from electricity_rag.hashing import compute_content_hash


def test_compute_content_hash_same_inputs():
    text = "Hello, my dog is cute"
    hash1 = compute_content_hash(text)
    hash2 = compute_content_hash(text)
    assert hash1 == hash2


def test_compute_content_hash_different_inputs():
    text1 = "Hello, my dog is cute"
    text2 = "Hello, my dog is cute!"
    hash1 = compute_content_hash(text1)
    hash2 = compute_content_hash(text2)
    assert hash1 != hash2


def test_compute_content_hash_length():
    text = "Hello, my dog is cute"
    hash1 = compute_content_hash(text)
    assert len(hash1) == 64  # SHA-256 produces a 64-character hexadecimal string