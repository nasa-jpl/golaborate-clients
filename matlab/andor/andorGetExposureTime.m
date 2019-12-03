function f64 = andorGetExposureTime(s)
    url = strcat(s.CameraURL, "/exposure-time");
    structure = webread(url);
    f64 = structure.f64;
end
