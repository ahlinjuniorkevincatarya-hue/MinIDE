import keyword
import string

def color_syntax(txt):
    kywrd = keyword.kwlist
    for line_num in range(1, int(txt.index("end-1c").split('.')[0])+1):
        line_text = txt.get(f"{line_num}.0", f"{line_num}.end")
        txt.tag_remove("keyword", f"{line_num}.0", f"{line_num}.end")
        txt.tag_remove("string", f"{line_num}.0", f"{line_num}.end")
        txt.tag_remove("comment", f"{line_num}.0", f"{line_num}.end")
        txt.tag_remove("number", f"{line_num}.0", f"{line_num}.end")
        txt.tag_remove("punctuation", f"{line_num}.0", f"{line_num}.end")
        col = 0
        while col < len(line_text):
            char = line_text[col]
            if char in ('"', "'"):
                quote_char = char
                start_col = col
                col += 1
                while col < len(line_text) and line_text[col] != quote_char:
                    if line_text[col] == '\\':
                        col += 1
                    col += 1
                txt.tag_add("string", f"{line_num}.{start_col}", f"{line_num}.{col+1}")
            elif char == '#':
                txt.tag_add("comment", f"{line_num}.{col}", f"{line_num}.end")
                break
            if char in string.punctuation and char not in ('"', "'", '#'):
                txt.tag_add("punctuation", f"{line_num}.{col}", f"{line_num}.{col+1}")
            col += 1
        words = line_text.split()
        search_start = 0
        for word in words:
            col_index = line_text.find(word, search_start)
            if word in kywrd:
                txt.tag_add("keyword", f"{line_num}.{col_index}", f"{line_num}.{col_index+len(word)}")
            try:
                float(word)
                txt.tag_add("number", f"{line_num}.{col_index}", f"{line_num}.{col_index+len(word)}")
            except ValueError:
                pass
            search_start = col_index + len(word)