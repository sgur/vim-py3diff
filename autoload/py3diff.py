import difflib
import os.path


def _format_range_ed(start, stop):
    beginning = start + 1     # lines start numbering with one
    length = stop - start
    if not length:
        beginning -= 1        # empty ranges begin at line just before the range
    if length <= 1:
        return '{}'.format(beginning)
    return '{},{}'.format(beginning, beginning + length - 1)


def ed_diff(old, new, ignore_case, ignore_whitespaces, lineterm='\n'):
    started = False
    old_lines = [x.lower() for x in old] if ignore_case else old
    new_lines = [x.lower() for x in new] if ignore_case else new
    isJunk = difflib.IS_CHARACTER_JUNK if ignore_whitespaces else None
    for group in difflib.SequenceMatcher(isJunk, old_lines, new_lines).get_grouped_opcodes(0):
        if not started:
            started = True

        first, last = group[0], group[-1]
        file1_range = _format_range_ed(first[1], last[2])
        file2_range = _format_range_ed(first[3], last[4])

        for tag, i1, i2, j1, j2 in group:
            if tag == 'delete':
                yield '{}d{}{}'.format(file1_range, file2_range, lineterm)
                for line in old[i1:i2]:
                    yield '< ' + line
                continue
            if tag == 'insert':
                yield '{}a{}{}'.format(file1_range, file2_range, lineterm)
                for line in new[j1:j2]:
                    yield '> ' + line
                continue
            if tag == 'replace':
                replaced = False
                yield '{}c{}{}'.format(file1_range, file2_range, lineterm)
                for line in old[i1:i2]:
                    yield '< ' + line
                    replaced = True
                for line in new[j1:j2]:
                    if replaced:
                        yield '---' + lineterm
                    yield '> ' + line


def diff_files(fname_in, fname_new, fname_out, ignore_case=False, ignore_whitespaces=False):
    oldfname = os.path.expanduser(fname_in)
    newfname = os.path.expanduser(fname_new)
    outfname = os.path.expandvars(fname_out)
    with open(oldfname, encoding='utf-8', errors='surrogateescape') as oldf, open(newfname, encoding='utf-8', errors='surrogateescape') as newf:
        oldlines, newlines = list(oldf), list(newf)
    diff = ed_diff(oldlines, newlines, ignore_case, ignore_whitespaces)
    with open(outfname, mode='w', encoding='utf-8', errors='surrogateescape') as outf:
        outf.writelines(diff)
