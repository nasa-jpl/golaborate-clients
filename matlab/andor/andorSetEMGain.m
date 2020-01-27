function andorSetEMGain(s, fctr)
%andorSetEMGain(s, fctr)
%   Sets the EM multiplication gain, an integer factor

    s2 = struct();
    s2.int = fctr;
    options = weboptions('MediaType', 'application/json');
    url = [s.CameraURL,'/em-gain'];
    webwrite(url, s2, options)
end
