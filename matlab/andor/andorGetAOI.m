function ret = andorGetAOI(s)
    ret = webread(strcat(s.CameraURL, '/aoi'));
end