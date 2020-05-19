function prefix = andorGetRecorderPrefix(s)
%t = andorGetRecorderPrefix(s)
%   Returns the prefix of auto-written files, files look like
%   {prefix}nnnnnn.fits
    structure = webread(strcat(s.CameraURL, "/autowrite/prefix"));
    prefix = structure.str;
end
