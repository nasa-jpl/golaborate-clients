function andorSetEMGainMode(s, modeStr)
%andorSetEMGain(s, modeStr)
%   Sets the EM gain mode

    s2 = struct();
    s2.str = modeStr;
    options = weboptions('MediaType', 'application/json');
    url = [s.CameraURL,'/em-gain-mode'];
    webwrite(url, s2, options)
end
