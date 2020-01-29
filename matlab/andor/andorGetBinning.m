function fctr = andorGetBinning(s)
%t = andorGetEMGain(s)
%   Returns the binning, an integer factor

    structure = webread([s.CameraURL,'/binning']);
    fctr = structure.h;
end
