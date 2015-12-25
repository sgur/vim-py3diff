import difflib
import os.path


class Py3Diff(object):

    def __init__(self, ignore_case, ignore_whitespaces):
        self._ignore_case = ignore_case
        self._ignore_whitespaces = ignore_whitespaces

    def format_range_ed(self, start, stop):
        beginning = start + 1     # lines start numbering with one
        length = stop - start
        if not length:
            beginning -= 1        # empty ranges begin at line just before the range
        if length <= 1:
            return '{}'.format(beginning)
        return '{},{}'.format(beginning, beginning + length - 1)

    def ed_diff(self, old, new, lineterm='\n'):
        old_lines = [x.lower() for x in old] if self._ignore_case else old
        new_lines = [x.lower() for x in new] if self._ignore_case else new
        isJunk = difflib.IS_CHARACTER_JUNK if self._ignore_whitespaces else None
        for group in difflib.SequenceMatcher(isJunk, old_lines, new_lines).get_grouped_opcodes(0):
            yield from self.convert_lines(old, new, group, lineterm)

    def convert_lines(self, old, new, group, lineterm):
        first, last = group[0], group[-1]
        file1_range = self.format_range_ed(first[1], last[2])
        file2_range = self.format_range_ed(first[3], last[4])

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


def py3diff_diff_files(fname_in, fname_new, fname_out, ignore_case=False, ignore_whitespaces=False):
    oldfname = os.path.expanduser(fname_in)
    newfname = os.path.expanduser(fname_new)
    outfname = os.path.expandvars(fname_out)
    with open(oldfname, encoding='utf-8', errors='surrogateescape') as oldf, open(newfname, encoding='utf-8', errors='surrogateescape') as newf:
        oldlines, newlines = list(oldf), list(newf)
    diff = Py3Diff(ignore_case, ignore_whitespaces)
    ed = diff.ed_diff(oldlines, newlines)
    with open(outfname, mode='w', encoding='utf-8', errors='surrogateescape') as outf:
        outf.writelines(ed)
