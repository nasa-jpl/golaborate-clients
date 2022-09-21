function bool = motionHomed(s)
    url = strcat(s.ControllerURL, "/axis/", s.Axis, "/home");
    resp = webread(url);
    bool = resp.bool;
end
