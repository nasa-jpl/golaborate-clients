function nktNDSet(NKTs, ndPct)
    path = strcat(NKTs.NKTSuperKRoot, "/nd");
    s = struct();
    s.f64 = ndPct;
    options = weboptions('MediaType', 'application/json');
    webwrite(path, s, options);
end