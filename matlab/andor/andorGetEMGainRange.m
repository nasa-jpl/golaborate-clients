function minMaxStruct = andorGetEMGain(s)
%minMaxStruct = andorGetEMGain(s)
%   Returns the EM gain range, a struct with fields "min" and "max"

    minMaxStruct = webread([s.CameraURL,'/em-gain-range']);
end
