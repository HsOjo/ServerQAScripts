def str_compare_head_tail(text, head, tail=None):
    if tail is None:
        tail = head
    return text[:len(head)] == head and text[-len(tail):] == tail
