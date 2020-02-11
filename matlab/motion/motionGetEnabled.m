function bool = motionGetEnabled(s)
    url = strcat(s.ControllerURL, "/axis/", s.Axis, "/enabled");
    resp = webread(url);
    bool = resp.bool;
end
