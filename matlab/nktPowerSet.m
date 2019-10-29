function nktPowerSet(NKTs, ndPct)
    path = strcat(NKTs.NKTSuperKRoot, "/power");
    s = struct();
    s.f64 = ndPct;
    options = weboptions('MediaType', 'application/json');
    webwrite(path, s, options);
end