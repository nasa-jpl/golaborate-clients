function nktCenterBandwidthSet(NKTs, center, bandwidth)
    path = strcat(NKTs.NKTSuperKRoot, "/wl-center-bandwidth");
    s = struct();
    s.center = center;
    s.bandwidth = bandwidth;
    options = weboptions('MediaType', 'application/json');
    webwrite(path, s, options);
end