function andorSetExposureTime(s, tSec)
%andorSetExposureTime(s, tSec)
%   Sets the exposure time to tSec (time in seconds)
    s2 = struct();
    s2.f64 = tSec;
    options = weboptions('MediaType', 'application/json');
    url = [s.CameraURL,'/exposure-time'];
    webwrite(url, s2, options);
end
