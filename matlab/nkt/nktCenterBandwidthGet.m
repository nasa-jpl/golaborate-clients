function s = nktCenterBandwidthGet(NKTs)
    path = strcat(NKTs.NKTSuperKRoot, "/wl-center-bandwidth");
    s = webread(path);
end