function boolV = andorGetRecorderEnabled(s)
%t = andorGetRecorderPrefix(s)
%   Returns the prefix of auto-written files, files look like
%   {prefix}xxxxxx.fits
    structure = webread(strcat(s.CameraURL, "/autowrite/enabled"));
    boolV = structure.bool;
end
