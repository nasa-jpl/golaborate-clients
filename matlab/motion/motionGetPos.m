function f64 = motionGetPos(s)
    url = strcat(s.ControllerURL, "/axis/", s.Axis, "/pos");
    resp = webread(url);
    f64 = resp.f64;
end
