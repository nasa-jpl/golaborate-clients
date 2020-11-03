function andorSetShutter(s, open)
%andorSetShutter(s, open)
%   Sets the state of the camera's shutter.  if open = true, shutter is open.

    s2 = struct();
    s2.bool = open;
    options = weboptions('MediaType', 'application/json');
    url = [s.CameraURL,'/shutter'];
    webwrite(url, s2, options);
end
