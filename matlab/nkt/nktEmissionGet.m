function bool = nktEmissionGet(NKTs)
    path = strcat(NKTs.NKTSuperKRoot, "/emission");
    resp = webread(path);
    bool = resp.bool;
end