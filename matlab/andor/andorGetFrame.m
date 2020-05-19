function ary = andorGetFrame(s, fileName)
    opts = weboptions('Timeout', Inf);
    websave(fileName, strcat(s.CameraURL, '/image'), 'fmt', 'fits', opts);
    ary = fitsread(fileName);
end

%{
This function does not include all of the features the andor-http server
provides.  /image also allows an exposure time query parameter, which
we do not expose to the user here.  It also allows for jpg/png formats,
but they are 8 bit per pixel while fits is 16.
%}
