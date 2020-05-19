function itcOn(s)
    url = strcat(s.ControllerURL, "/emission");
    s = struct();
    opts = weboptions("MediaType", "application/json");
    s.bool = true;
    webwrite(url, s, opts); 
end