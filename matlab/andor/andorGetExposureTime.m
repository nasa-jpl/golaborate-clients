function t = andorGetExposureTime(s)
%t = andorGetExposureTime(s)
%   Returns the exposure time in seconds

    structure = webread([s.CameraURL,'/exposure-time']);
    t = structure.f64;
end
