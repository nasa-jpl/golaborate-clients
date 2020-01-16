function path = andorGetRecorderRoot(s)
%t = andorGetRecorderRoot(s)
%   Returns the root path (on the server, not your local machine) of the
%   autorecorder
    structure = webread(strcat(s.CameraURL, "/autowrite/root"));
    path = structure.str;
end
