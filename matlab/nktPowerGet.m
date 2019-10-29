function pct = nktPowerGet(NKTs)
    path = strcat(NKTs.NKTSuperKRoot, "/power");
    resp = webread(path);
    pct = resp.f64;
end