function f64 = itcGetCurrent(s)
    url = strcat(s.ControllerURL, "/current");
    s = webread(url);
    f64 = s.f64;
end