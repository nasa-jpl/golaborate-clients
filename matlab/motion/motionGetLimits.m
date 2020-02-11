function minMax = motionGetLimits(s)
    url = strcat(s.ControllerURL, "/axis/", s.Axis, "/limits");
    minMax = webread(url);
end
