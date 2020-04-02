function pct = nktNDGet(NKTs)
    path = strcat(NKTs.NKTSuperKRoot, "/nd");
    resp = webread(path);
    pct = resp.f64;
end