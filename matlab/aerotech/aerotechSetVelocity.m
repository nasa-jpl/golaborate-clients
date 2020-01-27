function aerotechSetVelocity(s, vel)
    url = strcat(s.ControllerURL, "/axis/", s.Axis, "/vel");
    opts = weboptions('MediaType', 'application/json');
    payload = struct();
    payload.f64 = pos;
    webwrite(url, payload, opts);
end
