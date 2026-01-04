def generate_dorks(email):
    return {
        "Exact match": f'https://www.google.com/search?q="{email}"',
        "Paste sites": f'https://www.google.com/search?q="{email}"+paste',
        "PDF files": f'https://www.google.com/search?q="{email}"+filetype:pdf',
    }
