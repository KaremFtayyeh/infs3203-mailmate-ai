def generate_email_reply(original_email, tone, reply_length):
    return (
        f"This is a sample {tone} reply with {reply_length} length.\n\n"
        f"Thank you for your email. I appreciate your message and will reply soon."
    )


def improve_email_reply(reply_text):
    return f"Improved version:\n\n{reply_text}"