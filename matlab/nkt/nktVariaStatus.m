function s = nktVariaStatus(NKTs)
     path = strcat(NKTs.NKTSuperKRoot, "/varia-status");
     s = webread(path);
end