function andorSetExposureTime(s, tSec)
    s = struct();
    s.f64 = tSec;
    options = weboptions('MediaType', 'application/json');
    url = strcat(s.CameraURL, "/exposure-time");
    webwrite(strcat(url, s, options))
end
