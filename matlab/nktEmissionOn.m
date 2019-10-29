function nktEmissionOn(NKTs)
    path = strcat(NKTs.NKTSuperKRoot, "/emission/on");
    webread(path);
end