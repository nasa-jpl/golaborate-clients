function andorSetExposureTime(s, tSec)
    s2 = struct();
    s2.f64 = tSec;
    options = weboptions('MediaType', 'application/json');
    url = strcat(s.CameraURL, "/exposure-time");
    webwrite(url, s2, options)
end
