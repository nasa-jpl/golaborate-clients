function g = andorGetEMGain(s)
%t = andorGetEMGain(s)
%   Returns the EM gain, an integer factor

    structure = webread([s.CameraURL,'/em-gain']);
    g = structure.int;
end
