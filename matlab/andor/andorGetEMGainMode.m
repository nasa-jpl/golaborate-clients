function mode = andorGetEMGainMode(s)
%mode = andorGetEMGain(s)
%   Returns the EM gain mode, which controls the meaning of the EM gain factor

    structure = webread([s.CameraURL,'/em-gain-mode']);
    g = structure.str;
end
