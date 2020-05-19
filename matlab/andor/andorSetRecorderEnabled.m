function andorSetRecorderEnabled(s, boolV)
%andorSetRecorderEnabled(s, tSec)
%   enable or disable the auto-writing recorder on the andor-http server

     s2 = struct();
     s2.bool = boolV;
     options = weboptions('MediaType', 'application/json');
     url = strcat(s.CameraURL, '/autowrite/enabled');
     webwrite(url, s2, options)
end
