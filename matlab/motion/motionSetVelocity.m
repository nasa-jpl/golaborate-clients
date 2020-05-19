function motionSetVelocity(s, vel)
    url = strcat(s.ControllerURL, "/axis/", s.Axis, "/velocity");
    opts = weboptions('MediaType', 'application/json');
    payload = struct();
    payload.f64 = vel;
    webwrite(url, payload, opts);
end
