function motionSetEnabled(s, bool)
    url = strcat(s.ControllerURL, "/axis/", s.Axis, "enabled");
    opts = weboptions('MediaType', 'application/json');
    payload = struct();
    payload.bool = bool;
    webwrite(url, payload, opts);
end
