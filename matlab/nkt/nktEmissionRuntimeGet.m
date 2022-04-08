function secs = nktEmissionRuntimeGet(NKTs)
    path = strcat(NKTs.NKTSuperKRoot, "/emission-runtime");
    resp = webread(path);
    secs = resp.f64;
end