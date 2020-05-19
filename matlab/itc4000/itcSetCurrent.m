function itcSetCurrent(s, mA)
    url = strcat(s.ControllerURL, "/current");
    opts = weboptions("MediaType", "application/json");
    s = struct();
    s.f64 = mA;
    webwrite(url, s, opts); 
end