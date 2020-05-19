function open = andorGetShutter(s)
%t = andorGetShutter(s)
%   Returns 1 if the shutter is open

    structure = webread([s.CameraURL,'/shutter']);
    open = structure.bool;
end
