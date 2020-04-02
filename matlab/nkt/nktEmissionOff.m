function nktEmissionOff(NKTs)
    path = strcat(NKTs.NKTSuperKRoot, "/emission/off");
    webread(path);
end