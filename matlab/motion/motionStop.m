function motionStop(s)
    url = strcat(s.ControllerURL, "/axis/", s.Axis, "/stop");
    dummy = struct(); % need this to satisfy matlab
    opts = weboptions('timeout', 60);
    webwrite(url, dummy, opts);
end
