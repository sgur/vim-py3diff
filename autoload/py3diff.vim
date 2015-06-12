scriptencoding utf-8

let s:save_cpo = &cpo
set cpo&vim

python3 import vim
execute 'py3file' expand("<sfile>:p:r") . '.py'

function! py3diff#diffexpr()
  python3 diff_files(vim.eval("v:fname_in"), vim.eval("v:fname_new"), vim.eval("v:fname_out")
        \ , vim.eval("&diffopt =~# 'icase'")==1, vim.eval("&diffopt =~# 'iwhite'")==1)
endfunction


let &cpo = s:save_cpo
unlet s:save_cpo
